import os
import re
from sys import platform

if platform.startswith("win"):
    from converter import Converter
else:
    from ..converter import Converter


@Converter.register
class OrderedList:
    pattern = re.compile('(^(\s*)-\s)(.*)', re.MULTILINE)


    def __init__(self):
        self.mode = os.path.basename((os.path.dirname(__file__)))


    def convert(self, text, config={}):
        lines = text.split('\n')
        last_used_linenrs = []
        index = 0
        result = text

        def deeper_depth(depth):
            return list(filter(lambda x: x[0] > depth, last_used_linenrs))

        def drop_in_depth_detected(depth):
            return len(deeper_depth(depth)) > 0

        def remove_deeper_depths(depth):
            for itm in deeper_depth(depth):
                last_used_linenrs.remove(itm)

        def last_used_by_depth(depth):
            return list(filter(lambda x: x[0] == depth, last_used_linenrs))

        def last_used_index(depth):
            return last_used_by_depth(depth)[0][2]

        def last_used_linenr(depth):
            linenr_result = last_used_by_depth(depth)
            if len(linenr_result) == 0:
                return 0
            return linenr_result[0][1]

        def set_last_used_linenr(depth, linenr, the_index):
            last_used_result = list(filter(lambda x: x[0] == depth, last_used_linenrs))
            if len(last_used_result) > 0:
                last_used_linenrs.remove(last_used_result[0])
            last_used_linenrs.append((depth, linenr, the_index))

        for match in OrderedList.pattern.findall(text):
            current_line = (match[0] + match[2]).replace('\n', '')
            current_depth = len(match[1].replace('\n', ''))
            current_linenr = lines.index(current_line)

            if last_used_linenr(current_depth) + 1 is current_linenr:
                index += 1
            elif drop_in_depth_detected(current_depth):
                index = last_used_index(current_depth) + 1
                remove_deeper_depths(current_depth)
            else:
                index = 1
            set_last_used_linenr(current_depth, current_linenr, index)

            result = result.replace(current_line, match[1].replace('\n', '') + str(index) + '. ' + match[2])

        return result
