# -*- mode: python ; coding: utf-8 -*-

import sys
from PyInstaller.utils.hooks import collect_submodules

project_name = "魔云腾令牌刷新工具"

# 包含静态资源
datas = [
    ('templates', 'templates'),
    ('static', 'static'),
    ('icon.ico', '.'),
]

# 自动收集子模块
hiddenimports = collect_submodules('your_project_module_if_needed')  # 可为空

a = Analysis(
    ['app.py'],  # 主入口脚本
    pathex=[],
    binaries=[],
    datas=datas,
    hiddenimports=hiddenimports,
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=None)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [],
    name=project_name,
    debug=False,
    bootloader_ignore_signals=False,
    uac_admin=True,
    strip=False,
    upx=True,
    console=True,          # ✅ 需要控制台日志设置 True
    icon='icon.ico',       # ✅ 设置你的图标
    win32_manifest='app.manifest',  # <-- 加这一行
)

