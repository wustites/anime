# anime

This repository contains animated stories based on Chinese fables and folklore.

## Projects

1. **crow-water** - The Crow Drinks Water (乌鸦喝水)
2. **turtle-rabbit** - The Tortoise and the Hare (龟兔赛跑)
3. **foolish-move-mountain** - The Foolish Old Man Moves Mountains (愚公移山)

## Preview and render

Install Node.js 22, Python 3.10+ and FFmpeg (including `ffprobe`). In a project
directory, run:

```bash
npm install
npm run dev       # long-running preview server
npm run check     # lint, validate, and inspect the composition
npm run render    # write the video to renders/
```

The three stories use layered SVG scenery and articulated character animation.
To change the shared illustrations or choreography, edit [storybook/](storybook/README.md)
and run `python3 storybook/build.py`, then run `npm run check` in all projects.
The runtime fonts and animation library are bundled locally.

## Narration pipeline

From the repository root:

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install edge-tts
python3 gen_audio.py crow-water --jobs 3
python3 mix_audio.py crow-water
```

Omit the project name to process all three stories. Generation requires network
access to the speech service; `--jobs` limits concurrent requests and `--voice`
selects the voice. Edit `narration.json` to change each cue's text and start time;
both scripts use this single configuration.

Mixing selects the latest rendered MP4, or a specific file with
`python3 mix_audio.py crow-water --video crow-water/renders/story.mp4`.
It replaces that video only after FFmpeg succeeds and the output passes probing.
Keep a copy of the original render if you need its original soundtrack: mixing
replaces the audio track. Missing or invalid narration causes a nonzero exit code.
Each cue is trimmed at the next cue or the end of the video; trimming is reported
so you can shorten the text or adjust cue times if words are cut off.

Generated audio, renders, and temporary files are excluded from Git.

## Tests

```bash
python3 -m unittest discover -s tests -v
```

Tests cover configuration, concurrent generation, failure recovery, and actual
FFmpeg mixing (duration, silence, and voice gain). FFmpeg integration tests skip
when its executables are unavailable; CI installs them and runs the full suite.
