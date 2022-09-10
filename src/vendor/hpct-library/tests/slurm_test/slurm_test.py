#! /usr/bin/env python3
#
# slurm_test.py

import json
import os.path
import pprint
import sys

sys.path.insert(0, os.path.realpath("../../lib"))

from hpctlib.editors.app.slurm import SlurmConfFileEditor


if __name__ == "__main__":
    sep = "----------"

    e = SlurmConfFileEditor()
    e.load("slurm.conf")

    print(e.render())

    print(sep)
    print(json.dumps(e.render_json(), indent=2, sort_keys=True))

    print(sep)
    print(e.render())

    print(sep)
    e.add_line("PartitionName=prod x=1 # added")
    print(e.render())
