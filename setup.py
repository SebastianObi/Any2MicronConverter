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
import os
import re
import setuptools
from pathlib import Path


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
with open("README.md", "r") as fh:
    long_description = fh.read()

version_file = os.path.join(os.path.dirname(__file__), "any2micronconverter", "_version.py")

def glob_converter():
    out_files = []
    src_path = os.path.join(os.path.dirname(__file__), "any2micronconverter")
    for root, dirs, files in os.walk(src_path):
        for file in files:
            filepath = os.path.join(str(Path(*Path(root).parts[1:])), file)
            print(filepath)
            out_files.append(filepath.split(f"any2micronconverter{os.sep}")[1])
    return out_files

package_data = {
"": [
    "assets/*",
    *glob_converter()
    ]
}

print("Packaging "+get_var(version_file, "__title__")+" "+get_var(version_file, "__version__")+" "+get_var(version_file, "__version_variant__"))

setuptools.setup(
    name=get_var(version_file, "__package_name__"),
    version=get_var(version_file, "__version__"),
    author=get_var(version_file, "__author__"),
    author_email=get_var(version_file, "__author_email__"),
    description=get_var(version_file, "__description__"),
    long_description=long_description,
    long_description_content_type="text/markdown",
    url=get_var(version_file, "__copyright_url__"),
    packages=setuptools.find_packages(),
    package_data=package_data,
    include_package_data=True,
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: Other/Proprietary License",
        "Operating System :: OS Independent",
    ],
    entry_points= {
        'console_scripts': [
             get_var(version_file, "__package_name__")+'=any2micronconverter.main:main',
        ]
    },
    install_requires=[],
    extras_require={
        "macos": ["pyobjus"],
    },
    python_requires='>=3.6',
)
