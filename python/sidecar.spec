# -*- mode: python ; coding: utf-8 -*-
"""
PyInstaller spec for the 4-Stem Flask sidecar.
Run from the python/ directory:
    pyinstaller sidecar.spec
"""
import shutil
from PyInstaller.utils.hooks import collect_all, collect_submodules

datas_all   = []
binaries_all = []
hidden_all  = []

# Bundle the ffmpeg binary staged by CI into python/bin/
import sys as _sys
_ffmpeg_name = 'ffmpeg.exe' if _sys.platform == 'win32' else 'ffmpeg'
_ffmpeg_staged = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'bin', _ffmpeg_name)
if os.path.exists(_ffmpeg_staged):
    print(f"[spec] Bundling staged ffmpeg: {_ffmpeg_staged}")
    binaries_all += [(_ffmpeg_staged, '.')]
else:
    # Fallback: try system PATH
    _ffmpeg_sys = shutil.which('ffmpeg')
    if _ffmpeg_sys:
        print(f"[spec] Bundling system ffmpeg: {_ffmpeg_sys}")
        binaries_all += [(_ffmpeg_sys, '.')]
    else:
        print("[spec] WARNING: ffmpeg not found — separation will fail!")

# Collect all data / binaries / hidden imports from heavy ML packages
for pkg in ['torch', 'torchaudio', 'demucs', 'audio_separator', 'imageio_ffmpeg']:
    try:
        d, b, h = collect_all(pkg)
        datas_all   += d
        binaries_all += b
        hidden_all  += h
    except Exception as e:
        print(f"[spec] Warning: could not collect {pkg}: {e}")

hidden_all += [
    # Flask stack
    'flask', 'werkzeug', 'werkzeug.serving', 'werkzeug.debug',
    'click', 'jinja2', 'itsdangerous', 'markupsafe',
    # ML
    'onnxruntime', 'onnxruntime.capi', 'onnxruntime.capi.onnxruntime_pybind11_state',
    # Demucs deps
    'julius', 'einops', 'lameenc', 'openunmix', 'diffq', 'dora', 'treetable',
    # Audio
    'numpy', 'scipy', 'scipy.signal', 'soundfile', 'librosa',
    'audioread', 'resampy', 'samplerate',
    # App modules
    'separate', 'server',
]

a = Analysis(
    ['sidecar.py'],
    pathex=['.'],
    binaries=binaries_all,
    datas=datas_all,
    hiddenimports=hidden_all,
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[
        'matplotlib', 'IPython', 'jupyter', 'PIL',
        'cv2', 'sklearn', 'pandas', 'tkinter',
    ],
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=None)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name='sidecar',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=True,   # keep console for stdout (Electron reads SIDECAR_PORT from it)
)

coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='sidecar',
)
