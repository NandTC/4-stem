"""
sidecar.py — 4-Stem entry point. Started by Electron at launch.
Prints SIDECAR_PORT:<port> to stdout then starts Flask.
"""

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# ── ffmpeg: use imageio_ffmpeg's bundled static binary ────────────────────────
# imageio_ffmpeg ships a pre-built static ffmpeg for each platform —
# no reliance on system brew/choco or PATH. Works both in dev and frozen.
try:
    import imageio_ffmpeg
    _ffmpeg_exe = imageio_ffmpeg.get_ffmpeg_exe()
    _ffmpeg_dir = os.path.dirname(_ffmpeg_exe)
    os.environ["PATH"] = _ffmpeg_dir + os.pathsep + os.environ.get("PATH", "")
    os.environ["FFMPEG_BINARY"] = _ffmpeg_exe
    print(f"[sidecar] ffmpeg: {_ffmpeg_exe}", flush=True)
except Exception as e:
    print(f"[sidecar] imageio_ffmpeg unavailable: {e}", flush=True)
    # Last resort: check PyInstaller bundle dir
    if getattr(sys, "frozen", False):
        _bundle_dir = getattr(sys, "_MEIPASS", os.path.dirname(sys.executable))
        os.environ["PATH"] = _bundle_dir + os.pathsep + os.environ.get("PATH", "")

from server import start_server

if __name__ == "__main__":
    start_server()
