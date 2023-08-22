import os
from sys import platform

if platform.startswith("win"):
    from converter import Converter
else:
    from ..converter import Converter

@Converter.register
class Emoji:
    # http://www.webpagefx.com/tools/emoji-cheat-sheet/
    config = {
        "8-)": "sunglasses",
        "8-O": "flushed",
        ":-(": "worried",
        ":-)": "simple_smile",
        "=)": "simple_smile",
        ":-/": "confused",
        ":-\\": "confused",
        ":-?": "sweat",
        ":-D": "laughing",
        ":-P": "stuck_out_tongue",
        ":-O": "open_mouth",
        ":-X": "grimacing",
        ":-|": "expressionless",
        ";-)": "wink",
        "^_^": "smile",
        ":?:": "question",
        ":!:": "exclamation",
        "LOL": "laughing",
    }


    def __init__(self):
        self.mode = os.path.basename((os.path.dirname(__file__)))


    def convert(self, text, config={}):
        result = text
        for key, value in Emoji.config.items():
            result = result.replace(key, ":"+value+":")
        return result
