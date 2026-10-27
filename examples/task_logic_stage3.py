import os

import aind_behavior_services.task.distributions as distributions
from aind_behavior_curriculum import Stage, TrainerState

from aind_behavior_dynamic_routing_bonsai.task_logic import (
    AindBehaviorDynamicRoutingBonsaiTaskLogic,
    AindBehaviorDynamicRoutingBonsaiTaskParameters,
    AudioStimulus,
    Block,
    GratingStimulus,
    PresentationParameters,
    QuadStimulus,
    AudioStimulus,
    Trial,
    TrialSet,
)

# Example generation of task logic settings for a stage3 experiment

# Here we generate the available stimuli for this experiment, both auditory and visual stimuli.
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
target_audio1 = AudioStimulus(
    stimulus_type="audio", frequency=12.0, phase=0.0, volume=68.0
)
target_audio2 = AudioStimulus(
    stimulus_type="audio", frequency=12.0, phase=90.0, volume=68.0
)
non_target_audio1 = AudioStimulus(
    stimulus_type="audio", frequency=70.0, phase=0.0, volume=68.0
)
non_target_audio2 = AudioStimulus(
    stimulus_type="audio", frequency=70.0, phase=90.0, volume=68.0
)
null_stim = QuadStimulus(
    stimulus_type="quad", extent_x=0, extent_y=0, position_x=0, position_y=0, color_r=1, color_g=0, color_b=0, color_a=0
)

# Trials are a combination of stimulus (defined above) and presentation parameters that set durations, reward valence etc.
non_contingent_presentation = PresentationParameters(
    stimulus_start_time=1.5,
    stimulus_duration=0.5,
    response_window_start_time=1.6,
    response_window_duration=0.9,
    rewarded=True,
    non_contingent_reward=False,
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
    timeout_duration=3.0,
    timeout_stimulus=null_stim,
    post_response_time=3.0
)

# We also define a distribution that Bonsai will sample to determine the pre stimulus time of each trial
# We define the parameters of an exponential distribution here to sample at runtime when the workflow is run.
pre_stimulus_distribution = distributions.ExponentialDistribution(
    distribution_parameters=distributions.ExponentialDistributionParameters(
        rate=1
    ),
    truncation_parameters=distributions.TruncationParameters(
        min=0.5,
        max=6
    )
)

# Finally we build the full task logic definition here. A full experiment is composed of Blocks, TrialSets and Trials.
# In this example we have two blocks of 1 minute, starting with rewarded visual stimuli, and then rewarded auditory stimuli.
task_logic = AindBehaviorDynamicRoutingBonsaiTaskLogic(
    task_parameters=AindBehaviorDynamicRoutingBonsaiTaskParameters(
        task_blocks=[
            Block(
                maximum_block_time=60,
                trial_sets=[
                    TrialSet(
                        repeats=1,
                        max_consecutive_same_reward=3,
                        available_trials=[
                            Trial(stimulus=target_grating1, presentation_parameters=non_contingent_presentation),
                            Trial(stimulus=target_grating2, presentation_parameters=non_contingent_presentation),
                            Trial(stimulus=non_target_grating1, presentation_parameters=unrewarded_presentation),
                            Trial(stimulus=non_target_grating2, presentation_parameters=unrewarded_presentation),
                            Trial(stimulus=target_audio1, presentation_parameters=unrewarded_presentation),
                            Trial(stimulus=target_audio2, presentation_parameters=unrewarded_presentation),
                            Trial(stimulus=non_target_audio1, presentation_parameters=unrewarded_presentation),
                            Trial(stimulus=non_target_audio2, presentation_parameters=unrewarded_presentation)
                        ] * 37
                    ),
                ],
            ),
            Block(
                maximum_block_time=60,
                trial_sets=[
                    TrialSet(
                        repeats=1,
                        max_consecutive_same_reward=3,
                        available_trials=[
                            Trial(stimulus=target_grating1, presentation_parameters=unrewarded_presentation),
                            Trial(stimulus=target_grating2, presentation_parameters=unrewarded_presentation),
                            Trial(stimulus=non_target_grating1, presentation_parameters=unrewarded_presentation),
                            Trial(stimulus=non_target_grating2, presentation_parameters=unrewarded_presentation),
                            Trial(stimulus=target_audio1, presentation_parameters=non_contingent_presentation),
                            Trial(stimulus=target_audio2, presentation_parameters=non_contingent_presentation),
                            Trial(stimulus=non_target_audio1, presentation_parameters=unrewarded_presentation),
                            Trial(stimulus=non_target_audio2, presentation_parameters=unrewarded_presentation)
                        ] * 37
                    ),
                ],
            )
        ],
        pre_stimulus_time_distribution=pre_stimulus_distribution
    )
)

# The last step is to compile our task logic definition into a named .json file that can be used to define task parameters in Bonsai.
def main(path_seed: str = "./local/stage3_{schema}.json"):
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