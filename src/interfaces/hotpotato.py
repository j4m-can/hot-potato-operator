# Copyright 2022 Canonical Ltd.
# See LICENSE file for licensing details.
#
# Learn more at: https://juju.is/docs/sdk

"""Hot potato interface.
"""


from hpctlib.interface import interface_registry
from hpctlib.interface.checker import FloatRange, IntegerRange
from hpctlib.interface.relation import (
    AppBucketInterface,
    RelationSuperInterface,
    UnitBucketInterface,
)
from hpctlib.interface.value import Boolean, Float, Integer, String


class HotPotatoRelationSuperInterface(RelationSuperInterface):
    """Hot potato relation super interface."""

    class AppInterface(AppBucketInterface):

        initialized = Boolean(False)
        delay = Float(1.0, FloatRange(0, None))
        max_passes = Integer(10, IntegerRange(0, None))
        owner = String("")
        run = Boolean(False)
        total_passes = Integer(0, IntegerRange(0, None))

    class UnitInterface(UnitBucketInterface):

        next_owner = String("")
        next_total_passes = Integer(0, IntegerRange(0, None))
        npasses = Integer(0, IntegerRange(0, None))

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.interface_classes[("peer", "app")] = self.AppInterface
        self.interface_classes[("peer", "unit")] = self.UnitInterface


interface_registry.register("relation-hot-potato", HotPotatoRelationSuperInterface)
