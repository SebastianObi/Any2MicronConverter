import os
import re
from sys import platform

if platform.startswith("win"):
    from converter import Converter
else:
    from ..converter import Converter


@Converter.register
class Cleanup:
    def __init__(self):
        self.mode = os.path.basename((os.path.dirname(__file__)))


    def convert(self, text, config={}):
        result = text
        result = re.sub(r"^>+", "#", result, flags=re.MULTILINE)
        return result
