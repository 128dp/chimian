from PyInstaller.utils.hooks import collect_all, collect_submodules


streamlit_datas, streamlit_binaries, streamlit_hiddenimports = collect_all('streamlit')
streamlit_hiddenimports += collect_submodules('pdfplumber')
streamlit_hiddenimports += ['pyperclip']


analysis = Analysis(
    ['streamlit_launcher.py'],
    pathex=['.'],
    binaries=streamlit_binaries,
    datas=streamlit_datas + [
        ('streamlit_app.py', '.'),
        ('enhanced_extractor.py', '.'),
        ('excel_writer.py', '.'),
        ('unit_converter.py', '.'),
        ('config.py', '.'),
    ],
    hiddenimports=streamlit_hiddenimports,
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
)


pyz = PYZ(analysis.pure)


exe = EXE(
    pyz,
    analysis.scripts,
    analysis.binaries,
    analysis.datas,
    [],
    name='Chimian',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=False,
    console=True,
)