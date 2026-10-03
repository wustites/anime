import asyncio
import json
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import types
import unittest
from unittest.mock import patch

from audio_common import load_narration, probe_duration
from gen_audio import gen_audio, generate
from mix_audio import main, mix


class ConfigurationTests(unittest.TestCase):
    def test_project_cues_are_valid(self):
        projects = load_narration()
        self.assertEqual(len(projects), 3)
        self.assertEqual(sum(map(len, projects.values())), 19)

    def test_rejects_unsafe_names_and_invalid_times(self):
        with tempfile.TemporaryDirectory() as directory:
            config = Path(directory) / 'narration.json'
            for name, start in [('one', -1), ('one', float('nan')), ('../one', 0), ('one', True)]:
                config.write_text(json.dumps({'project': [{'name': name, 'text': 'hello', 'start': start}]}))
                with self.subTest(name=name, start=start), self.assertRaises(ValueError):
                    load_narration(config)
            config.write_text(json.dumps({'project': [
                {'name': 'one', 'text': 'hello', 'start': 1},
                {'name': 'two', 'text': 'hello', 'start': 1},
            ]}))
            with self.assertRaises(ValueError):
                load_narration(config)

    def test_unknown_project_and_missing_inputs_fail(self):
        with self.assertRaises(SystemExit) as error:
            main(['unknown-project'])
        self.assertEqual(error.exception.code, 2)
        with patch('mix_audio.require_tools'), patch('mix_audio.mix', side_effect=FileNotFoundError('missing')):
            self.assertEqual(main(['crow-water']), 1)


class GenerationTests(unittest.IsolatedAsyncioTestCase):
    async def test_bounded_concurrency_and_failures(self):
        active = peak = 0
        completed = []

        async def fake_generate(name, *_):
            nonlocal active, peak
            active += 1
            peak = max(peak, active)
            try:
                await asyncio.sleep(0.01)
                completed.append(name)
                if name == 'bad':
                    raise RuntimeError('service failed')
            finally:
                active -= 1

        cues = [{'name': name, 'text': 'hello', 'start': index}
                for index, name in enumerate(['one', 'bad', 'three', 'four'])]
        with patch('gen_audio.gen_audio', side_effect=fake_generate):
            with self.assertRaisesRegex(RuntimeError, 'project/bad'):
                await generate({'project': cues}, jobs=2)
        self.assertEqual(peak, 2)
        self.assertEqual(len(completed), 4)

    async def test_stream_failure_preserves_existing_audio(self):
        class BrokenCommunicate:
            def __init__(self, *_):
                pass

            async def stream(self):
                yield {'type': 'audio', 'data': b'partial'}
                raise RuntimeError('stream failed')

        with tempfile.TemporaryDirectory() as directory:
            destination = Path(directory) / 'cue.mp3'
            destination.write_bytes(b'original')
            with patch.dict(sys.modules, edge_tts=types.SimpleNamespace(Communicate=BrokenCommunicate)):
                with self.assertRaisesRegex(RuntimeError, 'stream failed'):
                    await gen_audio('cue', 'hello', directory)
            self.assertEqual(destination.read_bytes(), b'original')
            self.assertEqual(list(Path(directory).iterdir()), [destination])

    async def test_empty_stream_fails(self):
        class EmptyCommunicate:
            def __init__(self, *_):
                pass

            async def stream(self):
                yield {'type': 'WordBoundary', 'text': 'hello'}

        with tempfile.TemporaryDirectory() as directory:
            with patch.dict(sys.modules, edge_tts=types.SimpleNamespace(Communicate=EmptyCommunicate)):
                with self.assertRaisesRegex(RuntimeError, 'no audio data'):
                    await gen_audio('cue', 'hello', directory)
            self.assertEqual(list(Path(directory).iterdir()), [])


@unittest.skipUnless(shutil.which('ffmpeg') and shutil.which('ffprobe'), 'FFmpeg required')
class MixingTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.base = Path(self.temp.name)
        self.project = self.base / 'project'
        (self.project / 'renders').mkdir(parents=True)
        (self.project / 'audio').mkdir()
        self.video = self.project / 'renders' / 'story.mp4'
        self.ffmpeg('-f', 'lavfi', '-i', 'color=c=black:s=32x32:r=10:d=3',
                    '-an', '-c:v', 'libx264', str(self.video))
        for name in ('one', 'two'):
            self.ffmpeg('-f', 'lavfi', '-i', 'sine=frequency=440:duration=2',
                        '-c:a', 'libmp3lame', str(self.project / 'audio' / f'{name}.mp3'))
        self.cues = [
            {'name': 'one', 'text': 'first', 'start': 0.2},
            {'name': 'two', 'text': 'second', 'start': 1.2},
        ]

    def ffmpeg(self, *arguments):
        subprocess.run(['ffmpeg', '-y', '-v', 'error', *arguments], check=True, capture_output=True)

    def test_mix_trims_to_video_and_preserves_gain(self):
        import array
        import math

        original_duration = probe_duration(self.video, video=True)
        # A newer legacy output must not be selected as the render source.
        legacy = self.video.with_name('story_voiced.mp4')
        legacy.write_bytes(b'legacy')
        output = mix('project', base=self.base, cues=self.cues)
        self.assertEqual(output, self.video)
        self.assertEqual(legacy.read_bytes(), b'legacy')
        self.assertAlmostEqual(probe_duration(output), original_duration, delta=0.06)
        audio = subprocess.run([
            'ffmpeg', '-v', 'error', '-i', str(output), '-map', '0:a:0',
            '-f', 'f32le', '-ac', '1', '-ar', '8000', 'pipe:1',
        ], check=True, capture_output=True).stdout
        samples = array.array('f', audio)

        def rms(start, end):
            segment = samples[int(start * 8000):int(end * 8000)]
            return math.sqrt(sum(value * value for value in segment) / len(segment))

        self.assertLess(rms(0.02, 0.15), 0.001)
        # FFmpeg's sine amplitude is 1/8; MP3/AAC gives RMS about 0.084.
        # Both cues must retain that gain, including across the first cue's end.
        first, second = rms(0.5, 0.9), rms(1.5, 1.9)
        self.assertGreater(first, 0.05)
        self.assertAlmostEqual(first, second, delta=0.005)
        self.assertLess(second, 0.095)

    def test_failure_preserves_source_and_cleans_temporary_file(self):
        original = self.video.read_bytes()
        with patch('mix_audio.subprocess.run', side_effect=subprocess.CalledProcessError(1, 'ffmpeg', stderr='failed')), \
                patch('mix_audio.probe_duration', return_value=3):
            with self.assertRaises(subprocess.CalledProcessError):
                mix('project', base=self.base, cues=self.cues)
        self.assertEqual(self.video.read_bytes(), original)
        self.assertEqual(list(self.video.parent.iterdir()), [self.video])

    def test_missing_cue_fails_before_modifying_video(self):
        original = self.video.read_bytes()
        (self.project / 'audio' / 'two.mp3').unlink()
        with self.assertRaisesRegex(FileNotFoundError, 'two.mp3'):
            mix('project', base=self.base, cues=self.cues)
        self.assertEqual(self.video.read_bytes(), original)

    def test_generated_chunks_form_valid_mp3(self):
        audio = (self.project / 'audio' / 'one.mp3').read_bytes()

        class FakeCommunicate:
            def __init__(self, *_):
                pass

            async def stream(self):
                yield {'type': 'WordBoundary', 'text': 'hello'}
                for offset in range(0, len(audio), 1024):
                    yield {'type': 'audio', 'data': audio[offset:offset + 1024]}

        with patch.dict(sys.modules, edge_tts=types.SimpleNamespace(Communicate=FakeCommunicate)):
            asyncio.run(gen_audio('generated', 'hello', self.project / 'audio'))
        destination = self.project / 'audio' / 'generated.mp3'
        self.assertEqual(destination.read_bytes(), audio)
        self.assertGreater(probe_duration(destination), 1.9)
        self.assertEqual(list(destination.parent.glob('.*.mp3')), [])

    def test_cue_beyond_video_fails(self):
        self.cues[-1]['start'] = 4
        with self.assertRaisesRegex(ValueError, 'beyond video duration'):
            mix('project', base=self.base, cues=self.cues)


if __name__ == '__main__':
    unittest.main()
