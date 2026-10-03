# Animated storybook source

`story_plan.json` owns story order, shot timing, titles and narration. `scenes.py`
composes each beat using the shared SVG characters and scenery in `build.py`.
`motion.js` owns the articulated GSAP choreography, scheduled within each shot.
Build the three standalone projects with:

```bash
python3 storybook/build.py
```

The generated `index.html` files embed the illustration and choreography so each
project can be rendered independently by the release workflow. Edit this source,
then regenerate; manual edits to generated HTML will be replaced.

The complete stories have 10 / 10 / 12 shots, lasting approximately 92 / 95 / 106
seconds. `build.py` generates `narration.json` from the plan, so captions, voice
and scene boundaries share one schedule. Edit source files and regenerate;
do not edit generated narration or HTML directly.

After changing narration:

```bash
python3 storybook/build.py
python3 gen_audio.py
python3 storybook/fit_voice.py
python3 storybook/build.py
# Check and render each project, then mix the finished render:
python3 mix_audio.py
```

`fit_voice.py` probes all generated MP3s, keeps the minimum shot lengths and adds
room for every complete line plus pauses. It is idempotent for the same audio.
Captions end shortly after their line rather than lingering across shot changes.
Explicit cue end times make mixing fail if narration would be cut off. Always
rebuild after fitting; the release workflow consumes the committed schedule.

Background,
foreground, character placement, limbs, and camera transforms use separate SVG
wrappers so seeking and rendering do not depend on playback history.

Run `npm run check` in **each** project after regenerating. Local GSAP 3.14.2 and
subset Noto Serif SC fonts live in each `assets/` directory. Noto's OFL license is
included beside the fonts. The font subsets cover the current Chinese narration,
scene copy, Latin characters, and digits. If you add characters, rebuild the fonts:

```bash
pip install fonttools brotli
python3 storybook/build.py --font-regular /path/to/NotoSerifSC-Regular.ttf \
  --font-bold /path/to/NotoSerifSC-Black.ttf
```

Download matching full fonts from Google Fonts before using those options; the
regular and black source URLs are recorded in `assets/SOURCES.md`. Default builds
use the checked-in subsets and require only the Python standard library.
