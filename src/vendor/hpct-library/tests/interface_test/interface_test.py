#! /usr/bin/env python3
#
# interface_test.py


import json
import os.path
import logging
import sys

sys.path.insert(0, os.path.realpath("../../lib"))

from hpctlib.interface.base import Interface, Value, test
from hpctlib.interface import codec, checker


logger = logging.getLogger(__name__)


class TestInterface(Interface):
    xboolean = Value(codec.Boolean(), False)
    xfloat = Value(codec.Float(), 0.0)
    xfloatrange = Value(codec.Float(), 0.0, checker.FloatRange(-100.3, 20.93))
    xinteger = Value(codec.Integer(), 0)
    xintegerrange = Value(codec.Integer(), 0, checker.IntegerRange(100, 204))
    ipaddress = Value(codec.IPAddress())
    ipnetwork = Value(codec.IPNetwork())


if __name__ == "__main__":
    iface = TestInterface()

    test(iface, "xboolean", True)
    test(iface, "xboolean", "hello")
    test(iface, "xboolean", 123)

    test(iface, "xinteger", 123)
    test(iface, "xintegerrange", 123)

    test(iface, "xfloat", 12.3)
    test(iface, "xfloatrange", 123.23)
    test(iface, "xfloatrange", -23.3)

    print(json.dumps(iface.get_doc(), indent=2))
