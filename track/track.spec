a = Analysis([os.path.join(HOMEPATH,'support\\_mountzlib.py'), os.path.join(HOMEPATH,'support\\useUnicode.py'), 'C:\\Documents and Settings\\fabriciols\\Desktop\\python\\track\\correios.py'],
             pathex=['C:\\Python25\\Lib\\site-packages\\pyinstaller-1.3'])
pyz = PYZ(a.pure)
exe = EXE(pyz,
          a.scripts,
          exclude_binaries=1,
          name='track.exe',
          debug=False,
#			 hiddenimports = [ 'win32api' ],
          strip=False,
          upx=False,
          console=True )
coll = COLLECT( exe,
               a.binaries,
               strip=False,
               upx=False,
               name='trackBin')
