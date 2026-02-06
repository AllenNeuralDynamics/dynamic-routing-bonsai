import os

import aind_behavior_services.rig as rig

from aind_behavior_dynamic_routing_bonsai.rig import (
    AindBehaviorDynamicRoutingBonsaiRig,
)

frame_rate=60
video_writer = rig.cameras.VideoWriterFfmpeg(frame_rate=frame_rate, container_extension="mp4")

rig = AindBehaviorDynamicRoutingBonsaiRig(
    rig_name="test_rig",
    harp_behavior=rig.harp.HarpBehavior(port_name="COM14"),
    harp_sound_card=rig.harp.HarpSoundCard(port_name="COM4"),
    harp_lickety_split=rig.harp.HarpLicketySplit(port_name="COM15"),
    camera_controller=rig.cameras.CameraController(
        frame_rate=frame_rate,
        cameras={
            "Camera1": rig.cameras.SpinnakerCamera(
                serial_number="24228162",
                video_writer=video_writer
            ),
            "Camera2": rig.cameras.SpinnakerCamera(
                serial_number="24210983",
                video_writer=video_writer
            ),
            "Camera3": rig.cameras.SpinnakerCamera(
                serial_number="24233229",
                video_writer=video_writer
            ),
        }
    ),
    screen=rig.visual_stimulation.Screen(
        calibration=rig.visual_stimulation.DisplaysCalibration(
            center=rig.visual_stimulation.DisplayCalibration(
                intrinsics=rig.visual_stimulation.DisplayIntrinsics(),
                extrinsics=rig.visual_stimulation.DisplayExtrinsics(),
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
