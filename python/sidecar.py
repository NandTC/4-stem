"""
sidecar.py — 4-Stem entry point. Started by Electron at launch.
Prints SIDECAR_PORT:<port> to stdout then starts Flask.
"""

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# ── Bundle ffmpeg into PATH (works both in dev and PyInstaller) ───────────────
try:
    import imageio_ffmpeg
    _ffmpeg_dir = os.path.dirname(imageio_ffmpeg.get_ffmpeg_exe())
    os.environ["PATH"] = _ffmpeg_dir + os.pathsep + os.environ.get("PATH", "")
except Exception as e:
    print(f"[sidecar] Warning: could not set ffmpeg path: {e}", flush=True)

from server import start_server

if __name__ == "__main__":
    start_server()
