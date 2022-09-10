#!/usr/bin/env python3
# Copyright 2022 Canonical Ltd.
# See LICENSE file for licensing details.
#
# Learn more at: https://juju.is/docs/sdk

"""Hot potato operator.

See README.md for details.
"""


import logging

from ops.main import main


USE_IFACE = False
logger = logging.getLogger(__name__)


if __name__ == "__main__":
    if USE_IFACE:
        import charmiface

        HotPotatoCharm = charmiface.HotPotatoCharm
    else:
        import charmnoiface

        HotPotatoCharm = charmnoiface.HotPotatoCharm

    main(HotPotatoCharm)
