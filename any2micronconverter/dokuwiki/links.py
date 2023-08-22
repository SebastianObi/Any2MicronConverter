import os
import re
from os import walk
from sys import platform
from pathlib import Path

if platform.startswith("win"):
    from converter import Converter
else:
    from ..converter import Converter


@Converter.register
class Links:
    pattern = re.compile('(\[\[)(.*?)(\]\])')


    def __init__(self):
        self.mode = os.path.basename((os.path.dirname(__file__)))


    def convert(self, text, config={}):
        result = text

        def starts_with_space(match):
            return match[1][0] == " "

        for regex_link in Links.pattern.findall(text):
            if starts_with_space(regex_link):
                continue

            origlink = "".join(regex_link)
            convertedlink = ""
            if "http" in origlink or "www" in origlink:
                convertedlink = self.convert_as_external_link(origlink)
            elif ">" in origlink and not "<" in origlink:
                convertedlink = self.convert_as_interwiki_link(origlink)
            else:
                convertedlink = self.convert_as_internal_link(origlink, config["file_replace"], config["link_root"])
            result = result.replace(origlink, convertedlink)
        return result


    def parse_url(self, text):
        return text[2:text.index('|')]


    def parse_title(self, text):
        return text[text.index('|') + 1: text.index(']]')]


    def convert_as_interwiki_link(self, text):
        interwiki_shortcode = text[2:text.index('>')]
        #self.assert_interwiki_is_known(interwiki_shortcode)
        interwiki_urlpart = text[text.index(">") + 1: len(text) - 2]

        return """`[%s`%s]""" % (interwiki_shortcode, interwiki_urlpart)

    def convert_as_internal_link(self, text, file_replace, link_root):
        url = ""
        title = ""
        if "|" not in text:
            url = text[2:len(text) - 2].replace(":", "/")
            title = text[2:len(text) - 2].replace(":", "/")
        else:
            url = self.parse_url(text).replace(":", "/")
            title = self.parse_title(text)

        if "." not in url:
            url = url + ".mu"

        for key, value in file_replace.items():
            url = url.replace(key, value)

        if not url.endswith(".mu"):
            url += ".mu"
        if not url.startswith("/"):
            url = "/"+url

        return """`[%s`%s%s]""" % (title, link_root, url.replace(' ', '_'))


    def convert_as_external_link(self, text):
        if "|" in text:
            url = self.parse_url(text)
            title = self.parse_title(text)
            return "`[" + title + "`" + url + "]"
        url = text.replace('[', '').replace(']', '')
        return "`[" + url + "`" + url + "]"


    def assert_interwiki_is_known(self, shortcode):
        shortcodes = []
        shortcodes_path = Path(__file__).parents[2].joinpath('layouts/shortcodes')
        for (dirpath, dirnames, filenames) in walk(shortcodes_path):
            shortcodes.extend(filenames)
            break
        if not (shortcode in map(lambda x: x.replace(".html", ""), shortcodes)):
            raise ValueError("Unknown Interwiki code " + shortcode + " - please add a shortcode in the layouts dir!")
