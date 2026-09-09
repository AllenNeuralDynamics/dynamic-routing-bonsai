import os

from aind_behavior_curriculum import Stage, TrainerState
import aind_behavior_services.task.distributions as distributions
import aind_behavior_services.task.distributions_utils as dist_utils

from aind_behavior_dynamic_routing_bonsai.task_logic import (
    AindBehaviorDynamicRoutingBonsaiTaskLogic,
    AindBehaviorDynamicRoutingBonsaiTaskParameters,
    AudioStimulus,
    Block,
    GratingStimulus,
    PresentationParameters,
    QuadStimulus,
    Trial,
    TrialSet,
)

target_grating1 = GratingStimulus(
    stimulus_type="grating", angle=0, aperture=0, extent_x=50, extent_y=50, spatial_frequency=0.04, temporal_frequency=-2, phase=0
)
target_grating2 = GratingStimulus(
    stimulus_type="grating", angle=0, aperture=0, extent_x=50, extent_y=50, spatial_frequency=0.04, temporal_frequency=-2, phase=90
)
non_target_grating1 = GratingStimulus(
    stimulus_type="grating", angle=90, aperture=0, extent_x=50, extent_y=50, spatial_frequency=0.04, temporal_frequency=2, phase=0
)
non_target_grating2 = GratingStimulus(
    stimulus_type="grating", angle=90, aperture=0, extent_x=50, extent_y=50, spatial_frequency=0.04, temporal_frequency=2, phase=90
)
null_stim = QuadStimulus(
    stimulus_type="quad", extent_x=0, extent_y=0, position_x=0, position_y=0, color_r=1, color_g=0, color_b=0, color_a=0
)
non_contingent_presentation = PresentationParameters(
    stimulus_start_time=1.5,
    stimulus_duration=0.5,
    response_window_start_time=1.6,
    response_window_duration=0.9,
    rewarded=True,
    non_contingent_reward=True,
    timeout_duration=0,
    timeout_stimulus=null_stim,
    post_response_time=3.0
)
unrewarded_presentation = PresentationParameters(
    stimulus_start_time=1.5,
    stimulus_duration=0.5,
    response_window_start_time=1.6,
    response_window_duration=0.9,
    rewarded=False,
    non_contingent_reward=False,
    timeout_duration=0,
    timeout_stimulus=null_stim,
    post_response_time=3.0
)

pre_stimulus_distribution = distributions.ExponentialDistribution(
    distribution_parameters=distributions.ExponentialDistributionParameters(
        rate=1
    ),
    truncation_parameters=distributions.TruncationParameters(
        min=0.5,
        max=6
    )
)

task_logic = AindBehaviorDynamicRoutingBonsaiTaskLogic(
    task_parameters=AindBehaviorDynamicRoutingBonsaiTaskParameters(
        task_blocks=[
            Block(
                maximum_block_time=600,
                trial_sets=[
                    TrialSet(
                        repeats=1,
                        available_trials=[
                            Trial(stimulus=target_grating1, presentation_parameters=non_contingent_presentation),
                            Trial(stimulus=target_grating2, presentation_parameters=non_contingent_presentation),
                            Trial(stimulus=non_target_grating1, presentation_parameters=unrewarded_presentation),
                            Trial(stimulus=non_target_grating2, presentation_parameters=unrewarded_presentation)
                        ] * 37
                    ),
                ],
            )
        ],
        pre_stimulus_time_distribution=pre_stimulus_distribution
    )
)


def main(path_seed: str = "./local/stage0_{schema}.json"):
    example_task_logic = task_logic
    example_trainer_state = TrainerState(
        stage=Stage(name="example_stage", task=example_task_logic), curriculum=None, is_on_curriculum=False
    )
    os.makedirs(os.path.dirname(path_seed), exist_ok=True)
    models = [example_task_logic, example_trainer_state]

    for model in models:
        with open(path_seed.format(schema=model.__class__.__name__), "w", encoding="utf-8") as f:
            f.write(model.model_dump_json(indent=2))


if __name__ == "__main__":
    main()