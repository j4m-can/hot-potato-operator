#!/usr/bin/env python3
# Copyright 2022 Canonical Ltd.
# See LICENSE file for licensing details.
#
# Learn more at: https://juju.is/docs/sdk

"""Hot potato operator, interface implementation.
"""

import logging
import time

from hpctlib.interface import interface_registry
from hpctlib.misc import log_enter_exit

from ops.model import ActiveStatus, WaitingStatus

from charmbase import BaseHotPotatoCharm
import interfaces.hotpotato


logger = logging.getLogger(__name__)


class HotPotatoCharm(BaseHotPotatoCharm):

    """Hot potato charm with interfaces."""

    def __init__(self, *args):
        super().__init__(*args)

        # superinterface
        self.hpsiface = interface_registry.load("relation-hot-potato", self, "hot-potato")

        self.framework.observe(self.on.leader_elected, self._on_leader_elected)

        self.framework.observe(
            self.on.hot_potato_relation_changed, self._on_hot_potato_relation_changed
        )

        self.framework.observe(self.on.configure_action, self._on_configure_action)
        self.framework.observe(self.on.run_action, self._on_run_action)

    @log_enter_exit()
    def _on_leader_elected(self, event):
        try:
            relation = self.model.get_relation("hot-potato")
            if relation:
                appiface = self.hpsiface.select(self.app)
                if not appiface.initialized:
                    # initialize
                    appiface.initialized = True
                    appiface.delay = 1.0
                    appiface.max_passes = 10
                    appiface.owner = "-"
                    appiface.run = False
                    appiface.total_passes = 0
        finally:
            self.service_set_updated("leader-elected")
            self.service_update_status()

    #
    # relations
    #
    @log_enter_exit()
    def _on_hot_potato_relation_changed(self, event):
        """'hot-potato-relation-changed' handler."""

        def update_app_from_unit(appiface, unitiface, unit):
            """Update app from unit (which has changed)"""

            if unitiface.next_total_passes > appiface.total_passes:
                appiface.total_passes = unitiface.next_total_passes
                appiface.owner = unitiface.next_owner

                if appiface.total_passes >= appiface.max_passes:
                    # stop passing
                    appiface.run = False

        def update_unit_from_app(unit, unitiface, appiface):
            """Update unit from app iff unit is now owner."""

            if appiface.owner == unit.name:
                unitiface.next_total_passes = appiface.total_passes + 1
                unitiface.next_owner = self.determine_next_owner()
                unitiface.npasses += 1

        try:
            appiface = self.hpsiface.select(self.app)

            if not appiface.run:
                return

            # run
            if self.unit.is_leader() and event.unit != None:
                # update app from unit
                unitiface = self.hpsiface.select(event.unit)
                update_app_from_unit(appiface, unitiface, event.unit)
                time.sleep(appiface.delay)
            else:
                # update unit from app (if for self)
                if event.unit != None:
                    # not an app update
                    return

                selfiface = self.hpsiface.select(self.unit)
                update_unit_from_app(self.unit, selfiface, appiface)

                # SPECIAL: leader will not get self unit change event
                # ensure leader can respond
                if self.unit.is_leader():
                    update_app_from_unit(appiface, selfiface, self.unit)

        finally:
            self.service_set_updated("hot-potato-relation-changed")
            self.service_update_status()

    #
    # actions
    #
    @log_enter_exit()
    def _on_configure_action(self, event):
        try:
            if self.unit.is_leader():
                appiface = self.hpsiface.select(self.app)

                if "delay" in event.params:
                    appiface.delay = event.params["delay"]
                if "owner" in event.params:
                    appiface.owner = event.params["owner"]
                if "max-passes" in event.params:
                    appiface.max_passes = event.params["max-passes"]
                if "run" in event.params:
                    appiface.run = event.params["run"]

                self.service_update_status()
        finally:
            self.service_set_updated("configure-action")
            self.service_update_status()

    @log_enter_exit()
    def _on_run_action(self, event):
        try:
            if self.unit.is_leader():
                appiface = self.hpsiface.select(self.app)
                appiface.run = event.params["run"]

                self.service_update_status()
        finally:
            self.service_set_updated("run-action")
            self.service_update_status()

    @log_enter_exit()
    def service_update_status(self):
        relation = self.model.get_relation("hot-potato")
        if not relation:
            self.unit.status = WaitingStatus()
            return

        appiface = self.hpsiface.select(self.app)
        if not appiface:
            self.unit.status = WaitingStatus()
            return

        isowner = appiface.owner == self.unit.name
        selfiface = self.hpsiface.select(self.unit)
        updated = tuple(self.service_get_updated())

        if self.unit.is_leader():
            # update app info
            appstatus = (
                f"APP"
                f" delay ({appiface.delay})"
                f" max_passes ({appiface.max_passes})"
                f" nunits ({len(relation.units)+1})"
                f" owner ({appiface.owner})"
                f" run ({appiface.run})"
                f" total_passes ({appiface.total_passes})"
                f" :: "
            )
        else:
            appstatus = ""

        unitstatus = (
            f"UNIT"
            f" id ({self.unit.name})"
            f" isowner? ({isowner})"
            f" npasses ({selfiface.npasses})"
            f" next_owner ({selfiface.next_owner})"
            f" next_total_passes ({selfiface.next_total_passes})"
        )

        self.unit.status = ActiveStatus(f"{updated} :: {appstatus}{unitstatus}")
