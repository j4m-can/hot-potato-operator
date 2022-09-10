#! /usr/bin/env python3
#
# exports_test.py

import json
import os.path
import pprint
import sys

sys.path.insert(0, os.path.realpath("../../lib"))

from hpctlib.editors.os.exports import ExportsFileEditor


if __name__ == "__main__":
    sep = "----------"

    e = ExportsFileEditor()
    e.load("exports")

    print(json.dumps(e.render_json(), indent=2))

    print(sep)
    print(e.render())

    print(sep)
    e.remove_by_path("/fs")
    print(e.render())

    print(sep)
    e.add_record_by_text("/abc host(rw)")
    print(json.dumps(e.render_json(), indent=2))
    print(e.render())
