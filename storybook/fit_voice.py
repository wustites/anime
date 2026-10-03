"""Fit complete speech plus breathing room; never truncate a line to hit a target."""
import json
from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from audio_common import probe_duration

ROOT = Path(__file__).resolve().parents[1]


def fit():
    source = ROOT / 'storybook/story_plan.json'
    plans = json.loads(source.read_text())
    for project, plan in plans.items():
        cursor = 0.0
        for shot in plan['shots']:
            nominal = shot.setdefault('min_duration', shot['end'] - shot['start'])
            lengths = [probe_duration(ROOT / project / 'audio' / (cue['name'] + '.mp3')) for cue in shot['cues']]
            first = .5 if cursor == 0 else .45
            second = max(3 if cursor == 0 else nominal/2+.45, first + lengths[0] + .45)
            length = max(nominal, second + lengths[1] + .7)
            shot['start'] = round(cursor, 3)
            shot['end'] = round(cursor+length, 3)
            for cue, offset, audio_length in zip(shot['cues'], (first, second), lengths):
                cue['start'] = round(cursor+offset, 3)
                cue['end'] = round(cursor+offset+audio_length+.2, 3)
            cursor = shot['end']
        plan['duration'] = round(cursor, 3)
        print(f'{project}: {cursor:.2f}s, every line fits in full')
    source.write_text(json.dumps(plans, ensure_ascii=False, indent=2) + '\n')


if __name__ == '__main__':
    fit()
