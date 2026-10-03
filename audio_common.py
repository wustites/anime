"""Shared narration configuration and safe media file operations."""

import json
import math
import os
from pathlib import Path
import shutil
import subprocess
import tempfile

BASE = Path(__file__).resolve().parent


def load_narration(path=BASE / "narration.json"):
    projects = json.loads(Path(path).read_text(encoding="utf-8"))
    if not isinstance(projects, dict) or not projects:
        raise ValueError("Narration must contain projects")
    for project, cues in projects.items():
        if (Path(project).name != project or project in {".", ".."}
                or not isinstance(cues, list) or not cues):
            raise ValueError(f"Invalid project: {project}")
        names = set()
        previous = -1
        for cue in cues:
            if not isinstance(cue, dict) or not {"name", "text", "start"} <= cue.keys():
                raise ValueError(f"Cue must contain name, text, and start: {project}")
            name = cue["name"]
            start = cue["start"]
            if (not isinstance(name, str) or Path(name).name != name
                    or name in {".", ".."} or name in names):
                raise ValueError(f"Invalid or duplicate cue name: {name}")
            if not isinstance(cue["text"], str) or not cue["text"].strip():
                raise ValueError(f"Empty narration: {name}")
            if (isinstance(start, bool) or not isinstance(start, (int, float))
                    or not math.isfinite(start) or start < 0 or start <= previous):
                raise ValueError(f"Cue times must be finite and increasing: {name}")
            names.add(name)
            previous = start
    return projects


def require_tools():
    for tool in ("ffmpeg", "ffprobe"):
        if shutil.which(tool) is None:
            raise RuntimeError(f"Required executable not found: {tool}")


def probe_duration(path, *, video=False):
    command = ["ffprobe", "-v", "error"]
    if video:
        command += ["-select_streams", "v:0", "-show_entries", "stream=duration"]
    else:
        command += ["-show_entries", "format=duration"]
    result = subprocess.run(
        [*command, "-of", "default=noprint_wrappers=1:nokey=1", str(path)],
        check=True, capture_output=True, text=True, timeout=30,
    )
    duration = float(result.stdout.strip())
    if not math.isfinite(duration) or duration <= 0:
        raise ValueError(f"Invalid media duration: {path}")
    return duration


def temporary_output(destination):
    """Create an output beside its destination so os.replace stays atomic."""
    destination = Path(destination)
    destination.parent.mkdir(parents=True, exist_ok=True)
    fd, name = tempfile.mkstemp(
        prefix=f".{destination.stem}-", suffix=destination.suffix,
        dir=destination.parent,
    )
    os.close(fd)
    return Path(name)
