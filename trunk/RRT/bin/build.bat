PATH=%PATH%;..\..\pyinstaller-1.3
Build.py "RRT.spec"
del /Q /F /s buildRRT
del /Q /F /s warnRRT.txt
rd buildRRT
