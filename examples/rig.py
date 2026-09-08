import os

import aind_behavior_services.rig as rig
import aind_behavior_services.rig.cameras as cameras
import aind_behavior_services.rig.harp as harp
import aind_behavior_services.rig.visual_stimulation as visual_stimulation
from aind_behavior_services.common import Vector3

from aind_behavior_dynamic_routing_bonsai.rig import (
    AindBehaviorDynamicRoutingBonsaiRig,
)

from pathlib import Path

frame_rate=60
video_writer = cameras.VideoWriterFfmpeg(frame_rate=frame_rate, container_extension="mp4")

rig = AindBehaviorDynamicRoutingBonsaiRig(
    computer_name="",
    data_directory=Path("C:/Users/neurogears/source/repos/AllenNeuralDynamics/dynamic-routing-bonsai/temp_data"),
    rig_name="test_rig",
    harp_behavior=harp.HarpBehavior(port_name="COM14"),
    harp_sound_card=harp.HarpSoundCard(port_name="COM4"),
    harp_lickety_split=harp.HarpLicketySplit(port_name="COM15"),
    camera_controller=cameras.CameraController(
        frame_rate=frame_rate,
        cameras={
            "Camera1": cameras.SpinnakerCamera(
                serial_number="24228162",
                video_writer=video_writer
            ),
            "Camera2": cameras.SpinnakerCamera(
                serial_number="24210983",
                video_writer=video_writer
            ),
            "Camera3": cameras.SpinnakerCamera(
                serial_number="24233229",
                video_writer=video_writer
            ),
        }
    ),
    screen=visual_stimulation.ScreenAssembly(
        calibration=visual_stimulation.ScreenAssemblyCalibration(
            center=visual_stimulation.DisplayCalibration(
                intrinsics=visual_stimulation.DisplayIntrinsics(
                    frame_width=1000,
                    frame_height=1000,
                    display_height=20,
                    display_width=30
                ),
                extrinsics=visual_stimulation.DisplayExtrinsics(
                    rotation=Vector3(x=0, y=0, z=0),
                    translation=Vector3(x=0, y=0, z=-20)
                ),
            )
        )
    ),
)


def main(path_seed: str = "./local/{schema}.json"):
    os.makedirs(os.path.dirname(path_seed), exist_ok=True)
    models = [rig]

    for model in models:
        with open(path_seed.format(schema=model.__class__.__name__), "w", encoding="utf-8") as f:
            f.write(model.model_dump_json(indent=2))


if __name__ == "__main__":
    main()
