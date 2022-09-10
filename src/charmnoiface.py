#!/usr/bin/env python3
# Copyright 2022 Canonical Ltd.
# See LICENSE file for licensing details.
#
# Learn more at: https://juju.is/docs/sdk

"""Hot potato operator, non-interface implementation.
"""

import logging
import time

from hpctlib.misc import log_enter_exit

from ops.model import ActiveStatus, WaitingStatus

from charmbase import BaseHotPotatoCharm


logger = logging.getLogger(__name__)


class HotPotatoCharm(BaseHotPotatoCharm):

    """Hot potato charm without interfaces (standard way)."""

    def __init__(self, *args):
        super().__init__(*args)

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
                appdata = relation.data[self.app]
                if not bool(appdata.get("initialized", False)):
                    # initialize
                    appdata.update(
                        {
                            "initialized": "x",
                            "delay": str(1.0),
                            "max_passes": str(10),
                            "owner": "-",
                            "run": "",
                            "total_passes": str(0),
                        }
                    )
        finally:
            self.service_set_updated("leader-elected")
            self.service_update_status()

    #
    # relations
    #
    @log_enter_exit()
    def _on_hot_potato_relation_changed(self, event):
        def update_app_from_unit(appdata, unitdata, unit):
            """Update app from unit (which has changed)."""

            max_passes = int(appdata.get("max_passes", 0))
            total_passes = int(appdata.get("total_passes", 0))
            next_total_passes = int(unitdata.get("next_total_passes", 0))

            if next_total_passes > total_passes:
                total_passes = next_total_passes
                appdata.update(
                    {
                        "total_passes": str(next_total_passes),
                        "owner": unitdata.get("next_owner"),
                    }
                )

                if total_passes >= max_passes:
                    # stop passing
                    appdata.update({"run": ""})

        def update_unit_from_app(unit, unitdata, appdata):
            """Update unit from app iff unit is now owner."""

            if appdata.get("owner") == unit.name:
                unitdata.update(
                    {
                        "next_total_passes": str(int(appdata.get("total_passes", 0)) + 1),
                        "next_owner": self.determine_next_owner(),
                        "npasses": str(int(unitdata.get("npasses", 0)) + 1),
                    }
                )

        try:
            relation = self.model.get_relation("hot-potato")
            appdata = relation.data[self.app]

            if not bool(appdata.get("run")):
                return

            if self.unit.is_leader() and event.unit != None:
                # update app from unit
                unitdata = relation.data[event.unit]
                update_app_from_unit(appdata, unitdata, event.unit)
                delay = float(appdata.get("delay"))
                time.sleep(delay)
            else:
                # update unit from app (if for self)
                if event.unit != None:
                    # not an app update
                    return

                selfdata = relation.data[self.unit]
                update_unit_from_app(self.unit, selfdata, appdata)

                # SPECIAL: leader does not get self unit change evnet;
                # ensure leader can respond
                if self.unit.is_leader():
                    update_app_from_unit(appdata, selfdata, self.unit)

        finally:
            self.service_set_updated("hot-potator-relation-changed")
            self.service_update_status()

    #
    # actions
    #
    @log_enter_exit()
    def _on_configure_action(self, event):
        try:
            if self.unit.is_leader():
                appdata = self.model.get_relation("hot-potato").data[self.app]

                if "delay" in event.params:
                    appdata.update({"delay": str(event.params["delay"])})
                if "owner" in event.params:
                    appdata.update({"owner": event.params["owner"]})
                if "max-passes" in event.params:
                    appdata.update({"max_passes": str(event.params["max-passes"])})
        finally:
            self.service_set_updated("configure-action")
            self.service_update_status()

    @log_enter_exit()
    def _on_run_action(self, event):
        try:
            if self.unit.is_leader():
                appdata = self.model.get_relation("hot-potato").data[self.app]
                appdata.update({"run": event.params["run"] and "x" or ""})
        finally:
            self.service_set_updated("run-action")
            self.service_update_status()

    def service_update_status(self):
        relation = self.model.get_relation("hot-potato")
        if not relation:
            self.unit.status = WaitingStatus()
            return

        appdata = relation.data[self.app]
        if not appdata:
            self.unit.status = WaitingStatus()
            return

        selfdata = relation.data[self.unit]
        updated = tuple(self.service_get_updated())
        isowner = appdata.get("owner") == self.unit.name

        if self.unit.is_leader():
            # update app info
            self.unit.status = ActiveStatus(
                f"""updated ({updated})"""
                f""" id ({self.unit.name})"""
                f""" delay ({appdata.get("delay")})"""
                f""" max_passes ({appdata.get("max_passes")})"""
                f""" run ({bool(appdata.get("run"))})"""
                f""" isowner? ({isowner})"""
                f""" npasses ({selfdata.get("npasses")})"""
                f""" owner ({appdata.get("owner")})"""
                f""" total_passes ({appdata.get("total_passes")})"""
                f""" nunits ({len(relation.units)+1})"""
                f""" next_owner ({selfdata.get("next_owner")})"""
                f""" next_total_passes ({selfdata.get("next_total_passes")})"""
            )
        else:
            self.unit.status = ActiveStatus(
                f"""updated ({updated})"""
                f""" id ({self.unit.name})"""
                f""" isowner? ({isowner})"""
                f""" npasses ({selfdata.get("npasses")})"""
                f""" next_owner ({selfdata.get("next_owner")})"""
                f""" next_total_passes ({selfdata.get("next_total_passes")})"""
            )
