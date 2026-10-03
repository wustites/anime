"""Generate narration with bounded concurrency and atomic output files."""

import argparse
import asyncio
import os
from pathlib import Path
import subprocess
import sys

from audio_common import load_narration, probe_duration, require_tools, temporary_output

VOICE = "zh-CN-XiaoxiaoNeural"
BASE = Path(__file__).resolve().parent


async def gen_audio(filename, text, output_dir, voice=VOICE):
    # Import only when generating, so CLI help and tests work without edge-tts.
    import edge_tts

    destination = Path(output_dir) / f"{filename}.mp3"
    temporary = temporary_output(destination)
    try:
        # Write chunks as they arrive instead of repeatedly copying an audio buffer.
        with temporary.open("wb") as output:
            async for chunk in edge_tts.Communicate(text, voice).stream():
                if chunk["type"] == "audio":
                    output.write(chunk["data"])
        if temporary.stat().st_size == 0:
            raise RuntimeError(f"{filename}: no audio data received")
        duration = await asyncio.to_thread(probe_duration, temporary)
        os.replace(temporary, destination)
        print(f"  OK: {destination.name} ({duration:.1f}s)")
    finally:
        temporary.unlink(missing_ok=True)


async def generate(projects, *, base=BASE, jobs=3, voice=VOICE):
    semaphore = asyncio.Semaphore(jobs)

    async def run(project, cue):
        async with semaphore:
            try:
                await gen_audio(cue["name"], cue["text"], base / project / "audio", voice)
            except Exception as error:
                raise RuntimeError(f"{project}/{cue['name']}: {error}") from error

    results = await asyncio.gather(
        *(run(project, cue) for project, cues in projects.items() for cue in cues),
        return_exceptions=True,
    )
    failures = [str(result) for result in results if isinstance(result, BaseException)]
    if failures:
        raise RuntimeError("Narration generation failed:\n" + "\n".join(failures))


def main(argv=None):
    projects = load_narration()
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("project", nargs="?", choices=projects, help="Omit to generate all projects")
    parser.add_argument("--jobs", type=int, default=3, help="Concurrent requests (default: 3)")
    parser.add_argument("--voice", default=VOICE)
    args = parser.parse_args(argv)
    if args.jobs < 1:
        parser.error("--jobs must be positive")
    try:
        require_tools()
        selected = {args.project: projects[args.project]} if args.project else projects
        asyncio.run(generate(selected, jobs=args.jobs, voice=args.voice))
    except (RuntimeError, ImportError, ValueError, OSError, subprocess.SubprocessError) as error:
        print(f"ERROR: {error}", file=sys.stderr)
        return 1
    print("Done!")
    return 0


if __name__ == "__main__":
    sys.exit(main())
