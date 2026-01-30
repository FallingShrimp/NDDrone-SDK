# -*- mode: python ; coding: utf-8 -*-
import shutil

a = Analysis(
    ["src\\index.py"],
    pathex=[],
    binaries=[],
    datas=[
        ("assets", "assets"),
        ("venv\\Lib\\site-packages\\rich\\_unicode_data", "rich\\_unicode_data"),
    ],
    hiddenimports=[
        "psychopy.visual.backends.pygletbackend",
        "psychopy.visual.backends.pygamebackend",
        "psychopy.visual.backends.glfwbackend",
        "psychopy.visual.line",
        "psychopy.iohub.devices.display",
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
    optimize=0,
)
pyz = PYZ(a.pure)
shutil.copytree("assets", "dist\\assets", dirs_exist_ok=True)
shutil.copy("config.ini", "dist\\config.ini")
exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [],
    name="NDDrone",
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=True,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)
