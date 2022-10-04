# Copyright 2022 Canonical Ltd.
# See LICENSE file for licensing details.
#
# Learn more at: https://juju.is/docs/sdk

"""Hot potato interface.
"""


from hpctinterfaces import interface_registry
from hpctinterfaces.checker import FloatRange, IntegerRange
from hpctinterfaces.relation import (
    AppBucketInterface,
    RelationSuperInterface,
    UnitBucketInterface,
)
from hpctinterfaces.value import Boolean, NonNegativeFloat, NonNegativeInteger, String


class HotPotatoRelationSuperInterface(RelationSuperInterface):
    """Hot potato relation super interface."""

    class AppInterface(AppBucketInterface):

        initialized = Boolean(False)
        delay = NonNegativeFloat(1.0)
        max_passes = NonNegativeInteger(10)
        owner = String("")
        run = Boolean(False)
        total_passes = NonNegativeInteger(0)

    class UnitInterface(UnitBucketInterface):

        next_owner = String("")
        next_total_passes = NonNegativeInteger(0)
        npasses = NonNegativeInteger(0)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.interface_classes[("peer", "app")] = self.AppInterface
        self.interface_classes[("peer", "unit")] = self.UnitInterface


interface_registry.register("relation-hot-potato", HotPotatoRelationSuperInterface)
