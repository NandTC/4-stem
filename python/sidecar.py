"""
sidecar.py — 4-Stem entry point. Started by Electron at launch.
Prints SIDECAR_PORT:<port> to stdout then starts Flask.
"""

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# ── ffmpeg PATH setup ─────────────────────────────────────────────────────────
# In the packaged app, PyInstaller extracts all binaries to _MEIPASS.
# We staged ffmpeg there explicitly during the CI build, so just prepend it.
if getattr(sys, "frozen", False):
    _bundle_dir = getattr(sys, "_MEIPASS", os.path.dirname(sys.executable))
    os.environ["PATH"] = _bundle_dir + os.pathsep + os.environ.get("PATH", "")
    print(f"[sidecar] bundle dir in PATH: {_bundle_dir}", flush=True)
else:
    # Dev: use imageio_ffmpeg fallback
    try:
        import imageio_ffmpeg
        _ffmpeg_dir = os.path.dirname(imageio_ffmpeg.get_ffmpeg_exe())
        os.environ["PATH"] = _ffmpeg_dir + os.pathsep + os.environ.get("PATH", "")
    except Exception:
        pass

from server import start_server

if __name__ == "__main__":
    start_server()
