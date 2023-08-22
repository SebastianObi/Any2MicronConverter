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

        # Lines with spaces and tabs only
        result = re.sub(r"^[ \t]+$", "", result, flags=re.MULTILINE)

        # Lines with tabs and spaces at the end
        result = re.sub(r"[ \t]+$", "", result, flags=re.MULTILINE)

        # Replace more than two consecutive empty lines
        result = re.sub(r"\n\s*\n\s*\n+", "\n\n\n", result, flags=re.MULTILINE)

        return result
