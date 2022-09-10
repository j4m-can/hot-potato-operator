#! /usr/bin/env python3
#
# nsswitch_test.py

import json
import os.path
import pprint
import sys

sys.path.insert(0, os.path.realpath("../../lib"))

from hpctlib.editors.os.nsswitch import NSSwitchConfFileEditor


if __name__ == "__main__":
    sep = "----------"

    e = NSSwitchConfFileEditor()
    e.load("nsswitch.conf")

    print(e.render())

    print(sep)
    print(json.dumps(e.render_json(), indent=2, sort_keys=True))

    print(sep)
    e.remove_db("netgroup")
    print(e.render())

    print(sep)
    print(e.get_sourcesactions("passwd"))

    print(sep)
    e.upsert_record_by_text("abc: x y [NOTFOUND=return]")
    print(e.render())
