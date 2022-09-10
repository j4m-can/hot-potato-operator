#!/usr/bin/env python3
# Copyright 2022 Canonical Ltd.
# See LICENSE file for licensing details.
#
# Learn more at: https://juju.is/docs/sdk

"""Base Hot Potato operator.
"""


import logging
import random
import sys

sys.path.insert(1, sys.path[0] + "/vendor")

from hpctlib.misc import get_methodname, log_enter_exit
from hpctlib.ops.charm.service import ServiceCharm


logger = logging.getLogger(__name__)


if 1:
    # interpose DebuggerCharm
    from hpctlib.ops.charm import set_base_charm

    set_base_charm(ServiceCharm)
    from hpctlib.ops.charm.debugger import DebuggerCharm as ServiceCharm


class BaseHotPotatoCharm(ServiceCharm):
    """Hot potato operator."""

    # _stored already available

    def __init__(self, *args):
        super().__init__(*args)

        # standard handlers registered

        self.framework.observe(self.on.config_changed, self._on_config_changed)
        self.framework.observe(
            self.on.hot_potato_relation_joined, self._on_hot_potato_relation_joined
        )
        self.framework.observe(
            self.on.hot_potato_relation_departed, self._on_hot_potato_relation_departed
        )

    @log_enter_exit()
    def _on_config_changed(self, event):
        logger.debug(f"CONFIG CHANGED")
        self.service_update_status()

    @log_enter_exit()
    def _on_hot_potato_relation_departed(self, event):
        """'hot-potato-relation-departed' handler."""

        try:
            logger.debug("DEPARTED")
        except Exception as e:
            logger.debug(f"[{get_methodname(self)} e ({e})")

        self.service_update_status()

    @log_enter_exit()
    def _on_hot_potato_relation_joined(self, event):
        """'hot-potato-relation-joined' handler."""

        try:
            logger.debug("JOINED")
        except Exception as e:
            logger.debug(f"[{get_methodname(self)} e ({e})")

        self.service_update_status()

    @log_enter_exit()
    def determine_next_owner(self):
        # relation.units does not include self.unit!
        relation = self.model.get_relation("hot-potato")
        names = sorted([self.unit.name] + [unit.name for unit in relation.units])
        logger.debug(f"*** names ({names})")
        if names:
            i = random.randint(0, len(names) - 1)
            name = names[i]
        else:
            name = ""
        return name
