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


#################################################
# General version information                   #
#################################################


__version__ = "0.0.1"
__version_variant__ = "beta"
__version_date_time__ = "2023-08-21 00:00"
__copyright_short__ = "Copyright (c) 2023 Sebastian Obele  /  obele.eu  /  MIT License"
__copyright_url__ = "https://www.obele.eu"
__title__ = "Any2MicronConverter"
__description__ = "Convert any text/makrup document to micron format"
__author__ = "Sebastian Obele"
__author_email__ = "info@obele.eu"
__package_name__ = "any2micronconverter"


#################################################
# Configuration                                 #
#################################################


__config__ = {}

__config__["file_extensions_auto"] = {"html": "html2mu", "txt": "dw2mu"}
__config__["file_replace"] = {"home.txt": "index.mu", "home.md": "index.mu"}

__config__["link_root"] = ":/pages"

__config__["header"] = ""
__config__["footer"] = ""