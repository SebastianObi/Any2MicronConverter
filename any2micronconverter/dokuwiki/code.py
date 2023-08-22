import os
from sys import platform
from re import compile
from abc import ABC

if platform.startswith("win"):
    from converter import Converter
else:
    from ..converter import Converter


def strip_lang(language):
    if language == "":
        return language

    lang = language[1:len(language)]
    if " " in lang:
        lang = lang[0:lang.index(" ")]
    return lang


class BaseCode(ABC):
    dest = "```"


    def __init__(self, tag):
        self.mode = os.path.basename((os.path.dirname(__file__)))
        self.tag = tag
        self.pattern = compile("(<"+tag+"(.*?)>)")


    def convert(self, text, config={}):
        result = text
        for match in self.pattern.findall(text):
            language = strip_lang(match[1])
            result = result.replace(match[0], BaseCode.dest + language)
        return result.replace("</"+self.tag+">", BaseCode.dest)


@Converter.register
class File(BaseCode):
    def __init__(self):
        super().__init__("file")


@Converter.register
class Code(BaseCode):
    def __init__(self):
        super().__init__("code")

