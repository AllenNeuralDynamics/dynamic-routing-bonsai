# Import core types
from typing import Literal

import aind_behavior_services.calibration.water_valve as wvc
import aind_behavior_services.rig as rig
from pydantic import BaseModel, Field

from aind_behavior_dynamic_routing_bonsai import __semver__


class RigCalibration(BaseModel):
    water_valve: wvc.WaterValveCalibration = Field(..., description="Water valve calibration")


class AindBehaviorDynamicRoutingBonsaiRig(rig.AindBehaviorRigModel):
    version: Literal[__semver__] = __semver__
    harp_behavior: rig.harp.HarpBehavior = Field(..., description="Harp behavior")
    harp_sound_card: rig.harp.HarpSoundCard = Field(..., description="Harp sound card")
    harp_lickety_split: rig.harp.HarpLicketySplit = Field(..., description="Harp lickometer")
    screen: rig.visual_stimulation.Screen = Field(
        default=rig.visual_stimulation.Screen(), description="Screen settings"
    )
    camera_controller: rig.cameras.CameraController[rig.cameras.SpinnakerCamera]
    calibrations: RigCalibration = Field(default=RigCalibration(water_valve=wvc.WaterValveCalibration(
        input=wvc.WaterValveCalibrationInput(),
        output=wvc.WaterValveCalibrationOutput(slope=1, offset=0)
    )))
