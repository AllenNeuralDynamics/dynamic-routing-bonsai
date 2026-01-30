import os

import aind_behavior_services.task_logic.distributions as distributions
from aind_behavior_curriculum import Stage, TrainerState

from aind_behavior_dynamic_routing_bonsai.task_logic import (
    AindBehaviorDynamicRoutingBonsaiTaskLogic,
    AindBehaviorDynamicRoutingBonsaiTaskParameters,
    Block,
    TrialSet,
    Trial,
    PresentationParameters,
    BlankStimulus, AudioStimulus, GratingStimulus, QuadStimulus
)

grating1 = GratingStimulus(stimulus_type="grating", angle=0, aperture=1, extent_x=2, extent_y=2, spatial_frequency=10, temporal_frequency=2)
grating2 = GratingStimulus(stimulus_type="grating", angle=90, aperture=1, extent_x=2, extent_y=2, spatial_frequency=10, temporal_frequency=2)
timeout_stim = QuadStimulus(stimulus_type="quad", extent_x=1, extent_y=1, position_x=0, position_y=0, color_r=1, color_g=0, color_b=0, color_a=1)

non_contingent_presentation = PresentationParameters(stimulus_start_time=1.5, stimulus_duration=0.5, response_window_start_time=1.6, response_window_duration=0.9, rewarded=True, non_contingent_reward=True, timeout_duration=0, timeout_stimulus=timeout_stim)
rewarded_presentation = PresentationParameters(stimulus_start_time=1.5, stimulus_duration=0.5, response_window_start_time=1.6, response_window_duration=0.9, rewarded=True, non_contingent_reward=False, timeout_duration=0, timeout_stimulus=timeout_stim)
unrewarded_presentation = PresentationParameters(stimulus_start_time=1.5, stimulus_duration=0.5, response_window_start_time=1.6, response_window_duration=0.9, rewarded=False, non_contingent_reward=False, timeout_duration=4.5, timeout_stimulus=timeout_stim)

task_logic = AindBehaviorDynamicRoutingBonsaiTaskLogic(
    task_parameters=AindBehaviorDynamicRoutingBonsaiTaskParameters(
        task_blocks = [
            Block(maxmimum_block_time=600,
                  trial_sets=[
                      TrialSet(
                          repeats=5,
                          available_trials=[Trial(stimulus=grating1, presentation_parameters=non_contingent_presentation)]
                      ),
                      TrialSet(
                          repeats=10,
                          available_trials=[
                              Trial(stimulus=grating1, presentation_parameters=rewarded_presentation),
                              Trial(stimulus=grating2, presentation_parameters=unrewarded_presentation)
                          ]
                      )
                  ]                
            ),
            Block(maxmimum_block_time=600,
                  trial_sets=[
                      TrialSet(
                          repeats=10,
                          available_trials=[
                              Trial(stimulus=AudioStimulus(stimulus_type="audio", frequency=120), presentation_parameters=rewarded_presentation),
                              Trial(stimulus=AudioStimulus(stimulus_type="audio", frequency=700), presentation_parameters=unrewarded_presentation)
                          ]
                      )
                  ]                
            )
        ]
    ),
)


def main(path_seed: str = "./local/example_{schema}.json"):
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
