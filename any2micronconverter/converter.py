#!/usr/bin/env python3
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


from pathlib import Path


class Converter:
    converters = []


    @classmethod
    def register(cls, converter_class):
        cls.converters.append(converter_class())
        return converter_class


    def __init__(self, file, config, mode):
        self.file = file
        self.config = config
        self.mode = mode


    def convert(self):
        text = Path(self.file).read_text()
        for converter in Converter.converters:
            if self.mode != None and self.mode != converter.mode:
                continue
            text = converter.convert(text, self.config)
        return text
