#!/usr/bin/env python3
# -*- coding: utf-8 -*-


#   Copyright (C) 2018 Christoph Fink, University of Helsinki
#
#   This program is free software; you can redistribute it and/or
#   modify it under the terms of the GNU General Public License
#   as published by the Free Software Foundation; either version 3
#   of the License, or (at your option) any later version.
#
#   This program is distributed in the hope that it will be useful,
#   but WITHOUT ANY WARRANTY; without even the implied warranty of
#   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#   GNU General Public License for more details.
#
#   You should have received a copy of the GNU General Public License
#   along with this program; if not, see <http://www.gnu.org/licenses/>.


"""
Downloads the latest list of UTF emoji characters from
unicode.org and returns them as a concatenated str
(like string.letters)
"""

import datetime
import os
import os.path
import re
import requests
import string
import sys


__all__ = ["emojis"]
__name__ = "emojis"


class CacheExpiredException(BaseException):
    pass


def getEmojiUnicodeValues():
    emojiUnicodeValues = []

    rePattern = re.compile(
        "^(?P<minVal>[0-9A-F]{4,5})(?:..(?P<maxVal>[0-9A-F]{4,5}))?"
    )

    for line in downloadEmojiList().splitlines():
        reMatch = rePattern.match(line)

        if reMatch:
            minVal = int(reMatch["minVal"], 16)
            try:
                maxVal = int(reMatch["maxVal"], 16)
            except TypeError:
                maxVal = None

            if minVal > 128:  # unicode also lists 0…9 as emojis
                if maxVal is None:
                    emojiUnicodeValues.append(minVal)
                else:
                    emojiUnicodeValues += \
                            [v for v in range(minVal, maxVal + 1)]

    emojiUnicodeValues = set(emojiUnicodeValues)
    return emojiUnicodeValues


def downloadEmojiList():
    """
        Check local cache whether we have a recent (<1 week old) version
        of unicode.org’s list of emojis, otherwise download it

        Args:
            none

        Returns:
            content of emoji-data.txt (str)
    """
    cacheFileName = os.path.join(
        (
            os.environ.get('LOCALAPPDATA') or
            os.environ.get('XDG_CACHE_HOME') or
            os.path.join(os.environ['HOME'], '.cache')
        ),
        __name__,
        "emoji-data.txt"
    )

    try:
        cacheAge = \
            datetime.datetime.now().timestamp() \
            - os.stat(cacheFileName).st_mtime

        if cacheAge > (60 * 60 * 24 * 7):
            raise CacheExpiredException

        with open(cacheFileName) as f:
            emojiDataTxt = f.read()

    except (
        FileNotFoundError,
        CacheExpiredException
    ):
        try:
            emojiDataTxt = requests.get(
                "https://unicode.org/Public/emoji/latest/emoji-data.txt"
            ).text
        except requests.exceptions.RequestException:
            emojiDataTxt = requests.get(
                "https://web.archive.org/web/20200215125120/https://unicode.org/Public/emoji/latest/emoji-data.txt"  # noqa: E501
            ).text

        os.makedirs(
            os.path.dirname(cacheFileName),
            exist_ok=True
        )
        with open(cacheFileName, "w") as f:
            f.write(emojiDataTxt)

    return emojiDataTxt


emojis = "".join([chr(char) for char in getEmojiUnicodeValues()])

string.emojis = emojis
sys.modules.update({"string": string})

if __name__ == "__main__":
    pass
