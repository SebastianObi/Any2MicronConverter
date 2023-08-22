import os
from sys import platform
from re import compile

if platform.startswith("win"):
    from converter import Converter
else:
    from ..converter import Converter


@Converter.register
class Header:
    pattern = compile("(=+)(.*?)(=+)")
    head = "="
    config = {
        "======": 1,
        "=====": 2,
        "====": 3,
        "===": 3,
        "==": 3,
        "=": 3
    }


    def __init__(self):
        self.mode = os.path.basename((os.path.dirname(__file__)))


    def convert(self, text, config={}):
        result = text
        for regex_head in Header.pattern.findall(text):
            orig_header = "".join(regex_head)
            src_header = regex_head[0]
            if src_header in Header.config:
                new_header = (">" * Header.config[src_header]) + regex_head[1]
                result = result.replace(orig_header, new_header)
            else:
                new_header = (">" * 1) + regex_head[1]
                result = result.replace(orig_header, new_header)
        return result
