# -*- mode: python ; coding: utf-8 -*-


block_cipher = None


static_dir = 'domain/static/'
images = [
    (static_dir + 'bomb.jpg', '.'),
    (static_dir + 'diamond.jpg', '.'),
    (static_dir + 'money_sign.jpg', '.'),
    (static_dir + 'square.jpg', '.'),
    (static_dir + 'comecar_jogo.jpg', '.'),
    (static_dir + 'retirar.jpg', '.')
]

a = Analysis(
    ['blaze_mines_bot.py'],
    pathex=[],
    binaries=[],
    datas=images,
    hiddenimports=[],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)
pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='blaze_mines_bot',
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
