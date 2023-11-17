import os
from sys import platform
from re import compile
from abc import ABC

if platform.startswith("win"):
    from converter import Converter
else:
    from ..converter import Converter


class NopStyle(ABC):
    def convert(self, text, config={}):
        return text


class SimpleReplacementStyle(ABC):
    def __init__(self, dst_style, src_style):
        self.mode = os.path.basename((os.path.dirname(__file__)))
        self.dst_style = dst_style
        self.src_style = src_style

    def convert(self, text, config={}):
        return text.replace(self.src_style, self.dst_style)


class SimpleStyleBetweenTags(ABC):
    def __init__(self, dst_style, src_style_begin, src_style_end=None):
        self.mode = os.path.basename((os.path.dirname(__file__)))
        if src_style_end is None:
            src_style_end = src_style_begin
        self.pattern = compile("("+src_style_begin+")(.*?)("+src_style_end+")")
        self.dst_style = dst_style

    def convert(self, text, config={}):
        result = text
        for regex_head in self.pattern.findall(text):
            orig_header = "".join(regex_head)
            new_header = self.dst_style + regex_head[1] + self.dst_style
            result = result.replace(orig_header, new_header)
        return result


@Converter.register
class LineBreak(SimpleStyleBetweenTags):
    def __init__(self):
        super().__init__("\n", "\\\\ ?")


@Converter.register
class Bold(SimpleStyleBetweenTags):
    def __init__(self):
        super().__init__("`!", "\*\*")


@Converter.register
class Italic(SimpleStyleBetweenTags):
    def __init__(self):
        super().__init__("`*", "//")


@Converter.register
class Underline(SimpleStyleBetweenTags):
    def __init__(self):
        super().__init__("`_", "__")


@Converter.register
class StrikeThrough(SimpleStyleBetweenTags):
    def __init__(self):
        super().__init__("~", "<del>", "</del>")


@Converter.register
class Subscript(SimpleStyleBetweenTags):
    def __init__(self):
        super().__init__("", "<sub>", "</sub>")


@Converter.register
class Superscript(SimpleStyleBetweenTags):
    def __init__(self):
        super().__init__("", "<sup>", "</sup>")


@Converter.register
class InlineCode(SimpleStyleBetweenTags):
    def __init__(self):
        super().__init__("", "''", "''")


@Converter.register
class InlineHtml:
    def __init__(self):
        self.mode = os.path.basename((os.path.dirname(__file__)))

    def convert(self, text, config={}):
        return text.replace("<html>", "").replace("</html>", "")


@Converter.register
class Color:
    pattern = compile("(<color\s+#([a-fA-F0-9]{6})>([^<]+)<\/color>)")

    def __init__(self):
        self.mode = os.path.basename((os.path.dirname(__file__)))

    def convert(self, text, config={}):
        result = text
        for regex_color in Color.pattern.findall(text):
            orig_color = regex_color[0]
            color = regex_color[1]
            if len(color) == 6:
                color = str(color[1:2])+str(color[2:3])+str(color[4:5])
            new_color = "`F" + color + regex_color[2] + "`"
            result = result.replace(orig_color, new_color)
        return result
