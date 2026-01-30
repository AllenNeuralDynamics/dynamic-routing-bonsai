# Import core types
from typing import Literal
from pydantic import BaseModel, Field

import aind_behavior_services.rig as rig
import aind_behavior_services.calibration.water_valve as wvc

from aind_behavior_dynamic_routing_bonsai import __semver__


class RigCalibration(BaseModel):
    water_valve: wvc.WaterValveCalibration = Field(..., description="Water valve calibration")


class AindBehaviorDynamicRoutingBonsaiRig(rig.AindBehaviorRigModel):
    version: Literal[__semver__] = __semver__
    harp_behavior: rig.harp.HarpBehavior = Field(..., description="Harp behavior")
    harp_sound_card: rig.harp.HarpSoundCard = Field(..., description="Harp sound card")
    screen: rig.visual_stimulation.Screen = Field(
        default=rig.visual_stimulation.Screen(), description="Screen settings"
    )
