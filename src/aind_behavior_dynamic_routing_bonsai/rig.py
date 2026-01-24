# Import core types
from typing import Literal

import aind_behavior_services.rig as rig

from aind_behavior_dynamic_routing_bonsai import __semver__


class AindBehaviorDynamicRoutingBonsaiRig(rig.AindBehaviorRigModel):
    version: Literal[__semver__] = __semver__
    ...