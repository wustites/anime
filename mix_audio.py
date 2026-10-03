"""Mix complete narration into a rendered video, bounded by cue/video duration."""

import argparse
import os
from pathlib import Path
import subprocess
import sys

from audio_common import load_narration, probe_duration, require_tools, temporary_output

BASE = Path(__file__).resolve().parent


def mix(project, *, base=BASE, cues=None, video=None):
    if cues is None:
        cues = load_narration()[project]
    audio_dir = base / project / "audio"
    if video is None:
        # Ignore temporary and legacy intermediate outputs from interrupted runs.
        videos = [path for path in (base / project / "renders").glob("*.mp4")
                  if not path.name.startswith(".") and not path.stem.endswith("_voiced")]
        if not videos:
            raise FileNotFoundError(f"{project}: no rendered MP4 found")
        video = max(videos, key=lambda path: (path.stat().st_mtime_ns, path.name))
    video = Path(video)
    missing = [audio_dir / f"{cue['name']}.mp3" for cue in cues
               if not (audio_dir / f"{cue['name']}.mp3").is_file()]
    if missing:
        raise FileNotFoundError("Missing narration: " + ", ".join(map(str, missing)))
    duration = probe_duration(video, video=True)
    if cues[-1]["start"] >= duration:
        raise ValueError(f"{project}: narration starts beyond video duration ({duration}s)")

    inputs = ["-i", str(video)]
    filters = []
    for index, cue in enumerate(cues, start=1):
        audio = audio_dir / f"{cue['name']}.mp3"
        end = cues[index]["start"] if index < len(cues) else duration
        end = min(end, cue.get("end", end))
        window = end - cue["start"]
        audio_duration = probe_duration(audio)
        if "end" in cue and audio_duration > window + .02:
            raise ValueError(f"{project}/{cue['name']}: complete narration needs {audio_duration:.2f}s, "
                             f"but its window is {window:.2f}s; run storybook/fit_voice.py and rebuild")
        if audio_duration > window:
            print(f"  Trimming {cue['name']}: {audio_duration:.2f}s to {window:.2f}s")
        inputs.extend(["-i", str(audio)])
        delay = round(cue["start"] * 1000)
        filters.append(
            f"[{index}:a]atrim=duration={window:.6f},asetpts=PTS-STARTPTS,"
            f"adelay={delay}:all=1[a{index}]"
        )
    # Delays produce silence too. Disable normalization to preserve voice gain
    # regardless of how many pending or completed cues are in the mix.
    labels = "".join(f"[a{index}]" for index in range(1, len(cues) + 1))
    filters.append(
        f"{labels}amix=inputs={len(cues)}:duration=longest:normalize=0,"
        f"apad,atrim=duration={duration:.6f}[outa]"
    )
    temporary = temporary_output(video)
    try:
        subprocess.run([
            "ffmpeg", "-y", "-v", "error", *inputs,
            "-filter_complex", ";".join(filters),
            "-map", "0:v:0", "-map", "[outa]", "-c:v", "copy",
            "-c:a", "aac", "-ar", "44100", "-ac", "2",
            "-t", str(duration), str(temporary),
        ], check=True, capture_output=True, text=True, timeout=300)
        probe_duration(temporary, video=True)
        os.replace(temporary, video)
    finally:
        temporary.unlink(missing_ok=True)
    print(f"  Done! Output: {video}")
    return video


def main(argv=None):
    projects = load_narration()
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("project", nargs="?", choices=projects, help="Omit to mix all projects")
    parser.add_argument("--video", type=Path, help="Use this rendered MP4 instead of the latest")
    args = parser.parse_args(argv)
    if args.video and not args.project:
        parser.error("--video requires a project")
    try:
        require_tools()
    except RuntimeError as error:
        print(f"ERROR: {error}", file=sys.stderr)
        return 1
    failed = False
    for project in [args.project] if args.project else projects:
        try:
            mix(project, cues=projects[project], video=args.video)
        except (OSError, ValueError, subprocess.SubprocessError) as error:
            detail = error.stderr if isinstance(error, subprocess.CalledProcessError) else str(error)
            print(f"ERROR: {project}: {detail}", file=sys.stderr)
            failed = True
    return int(failed)


if __name__ == "__main__":
    sys.exit(main())
