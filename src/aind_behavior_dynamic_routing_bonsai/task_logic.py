import logging
from typing import Annotated, List, Literal, Optional, Self, Union

import aind_behavior_services.task.distributions as distributions
from aind_behavior_services.task import Task, TaskParameters
from pydantic import BaseModel, Field, model_validator

from aind_behavior_dynamic_routing_bonsai import (
    __semver__,
)

logger = logging.getLogger(__name__)

# ==================== MAIN TASK LOGIC CLASSES ====================


class StimulusBase(BaseModel):
    stimulus_type: str


class AudioStimulus(StimulusBase):
    stimulus_type: Literal["audio"]
    frequency: float = Field(description="The frequency of the sin modulation")
    phase: float = Field(description="The phase of the sin modulation")
    volume: float = Field(description="The target volume of the audio stimulus in dB")


class GratingStimulus(StimulusBase):
    stimulus_type: Literal["grating"]
    angle: float = Field(description="Stimulus angle in degrees")
    aperture: float = Field(description="Aperture size of grating stimulus")
    extent_x: float = Field(description="Horizontal extent of the stimulus relative to view size")
    extent_y: float = Field(description="Vertical extent of the stimulus relative to view size")
    spatial_frequency: float = Field(description="Spatial frequency of the stimulus relative to view size")
    temporal_frequency: float = Field(description="Temporal frequency of the stimulus relative to view size")
    phase: float = Field(description="Phase of the stimulus in degrees")


class QuadStimulus(StimulusBase):
    stimulus_type: Literal["quad"]
    extent_x: float = Field(description="Horizontal extent of the stimulus relative to view size")
    extent_y: float = Field(description="Vertical extent of the stimulus relative to view size")
    position_x: float = Field(description="Horizontal position of the stimulus relative to view size")
    position_y: float = Field(description="Horizontal position of the stimulus relative to view size")
    color_r: float = Field(description="Stimulus red channel value", ge=0, le=1)
    color_g: float = Field(description="Stimulus green channel value", ge=0, le=1)
    color_b: float = Field(description="Stimulus blue channel value", ge=0, le=1)
    color_a: float = Field(description="Stimulus alpha channel value", ge=0, le=1)


class BlankStimulus(StimulusBase):
    stimulus_type: Literal["blank"]


class PresentationParameters(BaseModel):
    stimulus_start_time: float = Field(description="Time (seconds) after trial start when stimulus should appear", ge=0)
    stimulus_duration: float = Field(description="Time (seconds) that stimulus should be presented for", ge=0)
    response_window_start_time: float = Field(description="Time (seconds) after trial start to begin the response window", ge=0)
    response_window_duration: float = Field(description="Duration (seconds) of response window", ge=0)
    rewarded: bool = Field(description="Whether this trial has a reward available")
    reward_amount: int = Field(default=10, description="The reward amount, in milliseconds open time.")
    non_contingent_reward: bool = Field(description="Whether this trial is rewarded regardless of subject response")
    timeout_duration: float = Field(description="Duration (seconds) of timeout if given")
    timeout_stimulus: Annotated[
        Union[AudioStimulus, GratingStimulus, QuadStimulus, BlankStimulus], Field(discriminator="stimulus_type")
    ] = Field(description="Definition of timeout stimulus")
    post_response_time: float = Field(description="Duration (seconds) of post-response period")


class Trial(BaseModel):
    stimulus: Annotated[
        Union[AudioStimulus, GratingStimulus, QuadStimulus, BlankStimulus], Field(discriminator="stimulus_type")
    ]
    presentation_parameters: PresentationParameters


class TrialSet(BaseModel):
    available_trials: List[Trial]
    repeats: int = Field(ge=1)
    max_consecutive_same_reward: Optional[int] = Field(
        default=None,
        ge=1,
        description="Maximum number of consecutive rewarded or unrewarded trials allowed when shuffling. If None, trials are shuffled without constraint.",
    )

    @model_validator(mode="after")
    def validate_max_consecutive_same_reward(self) -> Self:
        if self.max_consecutive_same_reward is None:
            return self
        n_rewarded = sum(trial.presentation_parameters.rewarded for trial in self.available_trials)
        n_unrewarded = len(self.available_trials) - n_rewarded
        larger, smaller = max(n_rewarded, n_unrewarded), min(n_rewarded, n_unrewarded)
        # The smaller group can split the larger group into at most (smaller + 1) runs
        if larger > self.max_consecutive_same_reward * (smaller + 1):
            raise ValueError(
                f"Cannot order {n_rewarded} rewarded and {n_unrewarded} unrewarded trials "
                f"with at most {self.max_consecutive_same_reward} consecutive trials of the same type."
            )
        return self


class Block(BaseModel):
    trial_sets: List[TrialSet]
    maximum_block_time: float = Field(ge=0)


class AindBehaviorDynamicRoutingBonsaiTaskParameters(TaskParameters):
    """
    Complete parameter specification for the dynamic-routing-bonsai task.
    """

    task_blocks: List[Block]
    pre_stimulus_time_distribution: distributions.ExponentialDistribution


class AindBehaviorDynamicRoutingBonsaiTaskLogic(Task):
    """
    Main task logic model for the dynamic-routing-bonsai task.
    """

    version: Literal[__semver__] = __semver__
    name: Literal["AindBehaviorDynamicRoutingBonsai"] = Field(
        default="AindBehaviorDynamicRoutingBonsai", description="Name of the task logic", frozen=True
    )
    task_parameters: AindBehaviorDynamicRoutingBonsaiTaskParameters = Field(description="Parameters of the task logic")
