# Import core types
from typing import Literal

import aind_behavior_services.rig.water_valve as wvc
import aind_behavior_services.rig.harp as harp
import aind_behavior_services.rig.visual_stimulation as visual_stimulation
import aind_behavior_services.rig.cameras as cameras
import aind_behavior_services.rig as rig
from pydantic import BaseModel, Field

from aind_behavior_dynamic_routing_bonsai import __semver__


class RigCalibration(BaseModel):
    water_valve: wvc.WaterValveCalibration = Field(..., description="Water valve calibration")


class AindBehaviorDynamicRoutingBonsaiRig(rig.Rig):
    version: Literal[__semver__] = __semver__
    harp_behavior: harp.HarpBehavior = Field(..., description="Harp behavior")
    harp_sound_card: harp.HarpSoundCard = Field(..., description="Harp sound card")
    harp_lickety_split: harp.HarpLicketySplit = Field(..., description="Harp lickometer")
    screen: visual_stimulation.ScreenAssembly = Field(
        default=visual_stimulation.ScreenAssembly(), description="Screen settings"
    )
    camera_controller: cameras.CameraController[cameras.SpinnakerCamera]
    calibrations: RigCalibration = Field(default=RigCalibration(water_valve=wvc.WaterValveCalibration(
        slope=1,
        offset=0
    )))
