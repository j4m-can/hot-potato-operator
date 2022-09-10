# Copyright 2022 Canonical Ltd.
# See LICENSE file for licensing details.
#
# Learn more at: https://juju.is/docs/sdk

"""Hot potato interface.
"""


from hpctlib.interface import codec, checker
from hpctlib.interface import interface_registry
from hpctlib.interface.base import Value
from hpctlib.interface.relation import (
    AppBucketInterface,
    RelationSuperInterface,
    UnitBucketInterface,
)


class HotPotatoRelationSuperInterface(RelationSuperInterface):
    """Hot potato relation super interface."""

    class AppInterface(AppBucketInterface):

        initialized = Value(codec.Boolean(), False)
        delay = Value(codec.Float(), 1.0, checker.FloatRange(0, None))
        max_passes = Value(codec.Integer(), 10, checker.IntegerRange(0, None))
        owner = Value(codec.String(), "")
        run = Value(codec.Boolean(), False)
        total_passes = Value(codec.Integer(), 0, checker.IntegerRange(0, None))

    class UnitInterface(UnitBucketInterface):

        next_owner = Value(codec.String(), "")
        next_total_passes = Value(codec.Integer(), 0, checker.IntegerRange(0, None))
        npasses = Value(codec.Integer(), 0, checker.IntegerRange(0, None))

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.interface_classes[("peer", "app")] = self.AppInterface
        self.interface_classes[("peer", "unit")] = self.UnitInterface


interface_registry.register("relation-hot-potato", HotPotatoRelationSuperInterface)
