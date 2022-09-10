#! /usr/bin/env python3
#
# freedesktop_test.py

import json
import os.path
import pprint
import sys

sys.path.insert(0, os.path.realpath("../../lib"))

from hpctlib.editors.os.freedesktop import FreeDesktopConfFileEditor


if __name__ == "__main__":
    sep = "----------"

    e = FreeDesktopConfFileEditor()
    e.load("freedesktop.conf")

    print(e.render())

    print(sep)
    print(json.dumps(e.render_json(), indent=2, sort_keys=True))

    print(sep)
    e.remove_group("b")
    print(e.render())

    print(sep)
    print(e.get_groups())
