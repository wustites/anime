"""
Mix edge-tts audio files into the rendered video for a project.
Each cue is (filename, start_seconds). Cue times are aligned to the
composition timeline so narration never overlaps and never overruns
the video duration. Run with the project name as the first argument.
"""
import subprocess
import os
import glob
import sys

BASE = os.path.dirname(os.path.abspath(__file__))

# Cues: (audio basename, start_seconds)
CUES = {
    "crow-water": [
        ("crow_title", 0.3),
        ("crow_find", 2.2),
        ("crow_idea", 6.4),
        ("crow_drop1", 8.3),
        ("crow_water_up", 10.7),
        ("crow_moral", 13.3),
    ],
    "turtle-rabbit": [
        ("turtle_title", 0.3),
        ("turtle_start", 2.2),
        ("turtle_rabbit_fast", 4.1),
        ("turtle_sleep", 7.2),
        ("turtle_tortoise_walk", 10.4),
        ("turtle_wakeup", 14.2),
        ("turtle_win", 17.7),
        ("turtle_moral", 19.8),
    ],
    "foolish-move-mountain": [
        ("foolish_title", 0.5),
        ("foolish_obstacle", 2.5),
        ("foolish_pick", 8.2),
        ("foolish_persist", 11.3),
        ("foolish_moral", 18.2),
    ],
}


def main():
    project = sys.argv[1] if len(sys.argv) > 1 else None
    projects = CUES if project is None else [project]

    for proj in projects:
        print(f"\n=== {proj} ===")
        mix(proj)


def mix(project):
    if project not in CUES:
        print(f"Unknown project: {project}")
        return

    render_dir = os.path.join(BASE, project, "renders")
    audio_dir = os.path.join(BASE, project, "audio")

    mp4s = glob.glob(os.path.join(render_dir, "*.mp4"))
    if not mp4s:
        print("  No rendered MP4 found!")
        return
    video_path = max(mp4s, key=os.path.getmtime)
    print(f"  Video: {video_path}")

    dur_str = subprocess.check_output([
        "ffprobe", "-v", "error", "-show_entries", "format=duration",
        "-of", "default=noprint_wrappers=1:nokey=1", video_path
    ]).decode().strip()
    video_dur = float(dur_str)
    print(f"  Video duration: {video_dur}s")

    # Build ffmpeg command: a silent base track the length of the video,
    # then each voice clip delayed to its cue time on top.
    inputs = ["-i", video_path]
    filter_parts = []

    for fname, start_sec in CUES[project]:
        audio_file = os.path.join(audio_dir, f"{fname}.mp3")
        if not os.path.exists(audio_file):
            print(f"  SKIP missing: {audio_file}")
            continue
        idx = len(inputs) // 2  # next input index
        inputs.extend(["-i", audio_file])
        delay_ms = int(start_sec * 1000)
        filter_parts.append(f"[{idx}:a]adelay={delay_ms}:all=1[a{idx}]")
        print(f"  {fname}: delay={delay_ms}ms")

    if not filter_parts:
        print("  No audio files to mix!")
        return

    audio_count = len(filter_parts)

    # With normalize=1, amix scales active inputs; including the silent base
    # halves each voice, so volume=2 restores unity.
    amix_inputs = "".join(f"[a{i+1}]" for i in range(audio_count))
    filter_expr = (
        f"anullsrc=channel_layout=stereo:sample_rate=44100:duration={video_dur}[silence];"
        + ";".join(filter_parts) + ";"
        + f"[silence]{amix_inputs}amix=inputs={audio_count + 1}:duration=longest:dropout_transition=0,volume=2[outa]"
    )

    output_path = video_path.replace(".mp4", "_voiced.mp4")

    cmd = [
        "ffmpeg", "-y", "-v", "error",
        *inputs,
        "-filter_complex", filter_expr,
        "-map", "0:v",
        "-map", "[outa]",
        "-c:v", "copy",
        "-c:a", "aac",
        output_path
    ]

    print(f"  Mixing {audio_count} audio tracks...")
    result = subprocess.run(cmd, capture_output=True)
    if result.returncode != 0:
        print(f"  FFmpeg error:\n{result.stderr.decode()[-500:]}")
        return

    os.replace(output_path, video_path)
    print(f"  Done! Output: {video_path}")


main()
