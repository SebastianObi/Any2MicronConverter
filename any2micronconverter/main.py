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


##############################################################################################################
# Include


#### System ####
import sys
import os
import time
import argparse
import shutil

if sys.platform.startswith("win"):
    #### Version ####
    from _version import __version__, __version_variant__, __copyright_short__, __title__, __description__, __config__

    #### Converter ####
    from converter import Converter

    #### Commands  - dokuwiki ####
    from dokuwiki.code import *
    from dokuwiki.comments import *
    from dokuwiki.emoji import *
    from dokuwiki.headers import *
    from dokuwiki.images import *
    from dokuwiki.links import *
    from dokuwiki.lists import *
    from dokuwiki.simplestyle import *
    from dokuwiki.todo import *
    from dokuwiki.z_cleanup import *
else:
    #### Version ####
    from ._version import __version__, __version_variant__, __copyright_short__, __title__, __description__, __config__

    #### Converter ####
    from .converter import Converter

    #### Commands  - dokuwiki ####
    from .dokuwiki.code import *
    from .dokuwiki.comments import *
    from .dokuwiki.emoji import *
    from .dokuwiki.headers import *
    from .dokuwiki.images import *
    from .dokuwiki.links import *
    from .dokuwiki.lists import *
    from .dokuwiki.simplestyle import *
    from .dokuwiki.todo import *
    from .dokuwiki.z_cleanup import *


##############################################################################################################
# Globals


PATH = os.path.expanduser("~") + "/." + os.path.splitext(os.path.basename(__file__))[0]


##############################################################################################################
# Log


LOG_FORCE    = -1
LOG_CRITICAL = 0
LOG_ERROR    = 1
LOG_WARNING  = 2
LOG_NOTICE   = 3
LOG_INFO     = 4
LOG_VERBOSE  = 5
LOG_DEBUG    = 6
LOG_EXTREME  = 7

LOG_LEVEL         = LOG_NOTICE
LOG_LEVEL_SERVICE = LOG_NOTICE
LOG_TIMEFMT       = "%Y-%m-%d %H:%M:%S"
LOG_MAXSIZE       = 5*1024*1024
LOG_PREFIX        = ""
LOG_SUFFIX        = ""
LOG_FILE          = ""


def log(text, level=3, file=None):
    if not LOG_LEVEL:
        return

    if LOG_LEVEL >= level:
        name = "Unknown"
        if (level == LOG_FORCE):
            name = ""
        if (level == LOG_CRITICAL):
            name = "Critical"
        if (level == LOG_ERROR):
            name = "Error"
        if (level == LOG_WARNING):
            name = "Warning"
        if (level == LOG_NOTICE):
            name = "Notice"
        if (level == LOG_INFO):
            name = "Info"
        if (level == LOG_VERBOSE):
            name = "Verbose"
        if (level == LOG_DEBUG):
            name = "Debug"
        if (level == LOG_EXTREME):
            name = "Extra"

        if not isinstance(text, str):
            text = str(text)

        text = "[" + time.strftime(LOG_TIMEFMT, time.localtime(time.time())) +"] [" + name + "] " + LOG_PREFIX + text + LOG_SUFFIX

        if file == None and LOG_FILE != "":
            file = LOG_FILE

        if file == None:
            print(text)
        else:
            try:
                file_handle = open(file, "a")
                file_handle.write(text + "\n")
                file_handle.close()

                if os.path.getsize(file) > LOG_MAXSIZE:
                    file_prev = file + ".1"
                    if os.path.isfile(file_prev):
                        os.unlink(file_prev)
                    os.rename(file, file_prev)
            except:
                return


##############################################################################################################
# System


#### Panic #####
def panic():
    sys.exit(255)


#### Exit #####
def exit():
    sys.exit(0)


##############################################################################################################
# Setup/Start


#### Setup #####
def setup(mode=None, src=None, dst=None, loglevel=None, test=False, link_root=None, header=None, footer=None):
    global LOG_LEVEL

    config = __config__

    if loglevel is not None:
        LOG_LEVEL = loglevel

    log("...............................................................................", LOG_INFO)
    log("        Name: " + __title__ + " - " + __description__, LOG_INFO)
    log("Program File: " + __file__, LOG_INFO)
    log("     Version: " + __version__ + " " + __version_variant__, LOG_INFO)
    log("   Copyright: " + __copyright_short__, LOG_INFO)
    log("...............................................................................", LOG_INFO)

    if src == None or dst == None:
        log("Missing parameters", LOG_ERROR)
        return

    if src.endswith("/"):
        src = src[:-1]

    if dst.endswith("/"):
        dst = dst[:-1]

    if test:
        log("   Test mode: YES", LOG_NOTICE)

    log("        Mode: " + str(mode), LOG_NOTICE)
    log(" Source path: " + src, LOG_NOTICE)
    log("   Dest path: " + dst, LOG_NOTICE)

    if link_root:
        config["link_root"] = link_root
    if config["link_root"].endswith("/"):
        config["link_root"] = config["link_root"][:-1]

    if header:
        config["header"] = header
    config["header"] = config["header"].replace("\\n", '\n')

    if footer:
        config["footer"] = footer
    config["footer"] = config["footer"].replace("\\n", '\n')

    if os.path.exists(dst):
        log("Deleting dest directory "+dst, LOG_DEBUG)
        if not test:
            shutil.rmtree(dst)
    if not test:
        os.makedirs(dst)

    for root, subFolders, files in os.walk(src):
        dst_dir = dst+root.replace(src, "", 1)
        if dst_dir.endswith("/"):
            dst_dir = dst_dir[:-1]
        files = [f for f in files if not f[0] == '.']
        for file in files:
            try:
                src_file = root+"/"+file

                if file in config["file_replace"]:
                    dst_file = config["file_replace"][file]
                else:
                    dst_file = os.path.splitext(file)[0] + ".mu"

                log("Converting "+dst_dir+"/"+dst_file+" ("+str(mode)+")", LOG_DEBUG)

                if not os.path.exists(dst_dir):
                    os.makedirs(dst_dir)

                output = Converter(src_file, config, mode).convert()
            except Exception as e:
                log("Failed to convert "+file+": "+str(e), LOG_ERROR)
                output = "Failed to convert: "+str(e)

            try:
                output = config["header"] + output + config["footer"]
                if not test:
                    with open(dst_dir+"/"+dst_file, "w", newline="\n") as fh:
                        fh.write(output)
            except Exception as e:
                log("Failed to write "+file+": "+str(e), LOG_ERROR)


#### Start ####
def main():
    try:
        description = __title__ + " - " + __description__
        parser = argparse.ArgumentParser(description=description)

        parser.add_argument("-m", "--mode", action="store", type=str, default=None, help="Mode or type of source data for conversion (Folder name with the command files)")
        parser.add_argument("-s", "--src", action="store", type=str, default=None, help="Path to source directory (All subfolders are included)")
        parser.add_argument("-d", "--dst", action="store", type=str, default=None, help="Path to destination directory (Folder is overwritten/deleted)")
        parser.add_argument("-l", "--loglevel", action="store", type=int, default=LOG_LEVEL)
        parser.add_argument("-t", "--test", action="store_true", default=False, help="Running in test mode (No files are deleted or overwritten)")
        parser.add_argument("--link_root", action="store", type=str, default=None, help="Root path of the links (Internal links in the documents)")
        parser.add_argument("--header", action="store", type=str, default=None, help="Header string which will be added on all pages")
        parser.add_argument("--footer", action="store", type=str, default=None, help="Footer string which will be added on all pages")

        params = parser.parse_args()

        setup(mode=params.mode, src=params.src, dst=params.dst, loglevel=params.loglevel, test=params.test, link_root=params.link_root, header=params.header, footer=params.footer)

    except KeyboardInterrupt:
        print("Terminated by CTRL-C")
        exit()


##############################################################################################################
# Init


if __name__ == "__main__":
    main()