# -*- mode: python ; coding: utf-8 -*-
import sys

block_cipher = None


a = Analysis(['main.py'],
             pathex=['/Users/viktor/Development/vending-machine'],
             binaries=[],
             datas=[],
             hiddenimports=[],
             hookspath=[],
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher,
             noarchive=False)

a.datas += [('package/assets/products/cola.jpeg', 'package/assets/products/cola.jpeg', 'DATA'),
            ('package/assets/products/kawa.jpg', 'package/assets/products/kawa.jpg', 'DATA'),
            ('package/assets/products/kitkat.png', 'package/assets/products/kitkat.png', 'DATA'),
            ('package/assets/products/lays.jpeg', 'package/assets/products/lays.jpeg', 'DATA'),
            ('package/assets/products/snickers.jpeg', 'package/assets/products/snickers.jpeg', 'DATA'),
            ('package/assets/products/sok.jpg', 'package/assets/products/sok.jpg', 'DATA'),
            ('package/assets/products/tea.jpg', 'package/assets/products/tea.jpg', 'DATA'),
            ('package/assets/products/twix.png', 'package/assets/products/twix.png', 'DATA'),
            ('package/assets/products/water.jpeg', 'package/assets/products/water.jpeg', 'DATA'),
            ('package/assets/utilities/card-payment.png', 'package/assets/utilities/card-payment.png', 'DATA'),]

pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)

exe = EXE(pyz,
          a.scripts,
          a.binaries,
          a.zipfiles,
          a.datas,
          [],
          name='vending-machine-console',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          upx_exclude=[],
          runtime_tmpdir=None,
          console=False )


app = BUNDLE(exe,
             name='vending-machine.app',
             info_plist={
                  'NSHighResolutionCapable': 'True'
             },
             icon=None,
             bundle_identifier=None)

exe = EXE(pyz,
        a.scripts,
        a.binaries,
        a.zipfiles,
        a.datas,
        name='vending-machine',
        debug=False,
        strip=False,
        upx=True,
        runtime_tmpdir=None,
        console=False,
     )