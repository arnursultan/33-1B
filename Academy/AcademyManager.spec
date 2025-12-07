import os
from PyInstaller.utils.hooks import collect_submodules

block_cipher = None

hidden = [
    "PyQt6.QtGui",
    "PyQt6.QtWidgets",
    "PyQt6.QtCore",
    "psycopg2",
    "psycopg2._psycopg",
] + collect_submodules("PyQt6")

a = Analysis(
    ["run.py"],
    pathex=[os.getcwd()],
    binaries=[],
    datas=[
        ("app", "app"),
        ("core", "core"),
        ("config", "config"),
    ],
    hiddenimports=hidden,
    hookspath=[],
    runtime_hooks=[],
    excludes=[],
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    name="AcademyManager",
    console=False,
    icon="icon.ico",
)
