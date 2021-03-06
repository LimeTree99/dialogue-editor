import os
import PyInstaller.__main__


NAME = 'dialogue-editor'
VERSION = '0_0_1'

README = \
"""
Run Instructions:
-----------------
run app.exe in /app folder


Author:
---------
evhemsley
"""

PATH = f"./dist/{NAME}-{VERSION}"

#builds project
PyInstaller.__main__.run([
    'main.py',
    '--windowed',
    '--noconfirm',
    '--clean',
    '--icon=build/flower_corner_image.ico',
    '--distpath', PATH,
    '--name', 'app'
])

#adds a readme
with open(f"{PATH}/readme.txt", "w") as fh:
    fh.write(README)

#delete unused files
if os.path.exists("app.spec"):
    os.remove("app.spec")