#! /usr/bin/env python3
#
# fstab_test.py

import json
import os.path
import pprint
import sys

sys.path.insert(0, os.path.realpath("../../lib"))

from hpctlib.editors.os.fstab import FstabFileEditor

if __name__ == "__main__":
    e = FstabFileEditor()
    e.load("fstab")
    print(e)
    print(e.root)
    print(e.render())
    pprint.pprint(e.render_json(), indent=2)

    print(json.dumps(e.render_json(), indent=2, sort_keys=True))
