# -*- mode: python ; coding: utf-8 -*-
"""
PyInstaller 配置文件 - 三国霸业游戏打包配置
"""
import os
import sys

block_cipher = None

# 获取项目根目录
PROJECT_ROOT = os.path.dirname(os.path.abspath(SPEC))

# 数据文件列表
datas = [
    ('data', 'data'),
]

# 如果assets目录存在，也包含进来
assets_dir = os.path.join(PROJECT_ROOT, 'assets')
if os.path.exists(assets_dir):
    datas.append(('assets', 'assets'))

a = Analysis(
    ['main.py'],
    pathex=[PROJECT_ROOT],
    binaries=[],
    datas=datas,
    hiddenimports=[
        'pygame',
        'pygame.font',
        'pygame.mixer',
        'pygame._sdl2',
    ],
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
    name='three_kingdoms',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,  # 不显示控制台窗口
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)