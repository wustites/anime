# Animated storybook source

`build.py` owns the shared SVG illustrations and scene composition. `motion.js`
owns the articulated GSAP choreography. Build the three standalone projects with:

```bash
python3 storybook/build.py
```

The generated `index.html` files embed the illustration and choreography so each
project can be rendered independently by the release workflow. Edit this source,
then regenerate; manual edits to generated HTML will be replaced.

Four shots per story preserve the existing 18/23/25-second narration schedules.
The subtitles read the same `narration.json` as the audio pipeline. Background,
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
