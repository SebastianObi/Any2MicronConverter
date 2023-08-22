import os
from sys import platform
from re import compile

if platform.startswith("win"):
    from converter import Converter
else:
    from ..converter import Converter


@Converter.register
class Todo:
    pattern = compile("(<todo(\s#)?>)(.*?)(</todo>)")
    todo = "- [ ] "
    done = "- [x] "


    def __init__(self):
        self.mode = os.path.basename((os.path.dirname(__file__)))


    def convert(self, text, config={}):
        result = text
        for match in Todo.pattern.findall(text):
            prefix = Todo.todo if match[1] == "" else Todo.done
            result = result.replace(match[0]+match[2]+match[3], prefix+match[2])
        return result
