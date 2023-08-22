##############################################################################################################
#
# Copyright (c) 2023 Sebastian Obele  /  obele.eu
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
#
# This software uses the following software-parts:
# dokuwiki-to-hugo  /  Copyright (c) 2017 Wouter Groeneveld  /  https://git.brainbaking.com/wgroeneveld/dokuwiki-to-hugo  /  MIT License
#
##############################################################################################################


#### Import ####
import sys
import os
import re
from pathlib import Path

import pyinstaller_versionfile
#from kivy_deps import sdl2, glew
#from kivymd import hooks_path as kivymd_hooks_path


#### Get Var ####
def get_var(file, var) -> str:
    content = open(file, "rt", encoding="utf-8").read()
    try:
        regex = r"(?<=^"+var+" = ['\"])[^'\"]+(?=['\"]$)"
        value = re.findall(regex, content, re.M)[0]
        return value
    except IndexError:
        raise ValueError(f"Unable to find string {var} in {file}.")
        return ""


#### Build ####
path = os.path.abspath(".")

version_file = "_version.py"
main_file = "main.py"

pyinstaller_versionfile.create_versionfile(
    output_file="version.rc",
    version=get_var(version_file, "__version__")+".0",
    company_name=get_var(version_file, "__author__"),
    file_description=get_var(version_file, "__description__"),
    internal_name=get_var(version_file, "__title__"),
    legal_copyright=get_var(version_file, "__copyright_short__"),
    original_filename=get_var(version_file, "__title__")+".exe",
    product_name=get_var(version_file, "__title__")
)

added_files = [
#    ("assets", "assets"),
]

a = Analysis(
    [main_file],
    pathex=[path],
    #hiddenimports=["plyer.platforms.win.storagepath"],
    #hookspath=[kivymd_hooks_path],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=None,
    noarchive=False,
    datas=added_files,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=None)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    #*[Tree(p) for p in (sdl2.dep_bins + glew.dep_bins)],
    debug=False,
    strip=False,
    upx=True,
    name=get_var(version_file, "__package_name__")+"-"+get_var(version_file, "__version__"),
    #icon="assets\icon.ico",
    console=True,
    version="version.rc",
)