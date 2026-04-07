"""
sidecar.py — 4-Stem entry point. Started by Electron at launch.
Prints SIDECAR_PORT:<port> to stdout then starts Flask.
"""

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# ── Make sure ffmpeg is in PATH (PyInstaller bundle or dev) ──────────────────
if getattr(sys, "frozen", False):
    # Packaged: ffmpeg binary is in the same dir as the executable
    _bundle_dir = getattr(sys, "_MEIPASS", os.path.dirname(sys.executable))
    os.environ["PATH"] = _bundle_dir + os.pathsep + os.environ.get("PATH", "")
else:
    # Dev: try imageio_ffmpeg fallback
    try:
        import imageio_ffmpeg
        _ffmpeg_dir = os.path.dirname(imageio_ffmpeg.get_ffmpeg_exe())
        os.environ["PATH"] = _ffmpeg_dir + os.pathsep + os.environ.get("PATH", "")
    except Exception:
        pass

from server import start_server

if __name__ == "__main__":
    start_server()
