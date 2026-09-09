import logging
from typing import Annotated, List, Literal, Union

import aind_behavior_services.task.distributions as distributions
from aind_behavior_services.task import Task, TaskParameters
from pydantic import BaseModel, Field

from aind_behavior_dynamic_routing_bonsai import (
    __semver__,
)

logger = logging.getLogger(__name__)

# ==================== MAIN TASK LOGIC CLASSES ====================


class StimulusBase(BaseModel):
    stimulus_type: str


class AudioStimulus(StimulusBase):
    stimulus_type: Literal["audio"]
    waveform_index: int
    attenuation: float


class GratingStimulus(StimulusBase):
    stimulus_type: Literal["grating"]
    angle: float
    aperture: float
    extent_x: float
    extent_y: float
    spatial_frequency: float
    temporal_frequency: float
    phase: float


class QuadStimulus(StimulusBase):
    stimulus_type: Literal["quad"]
    extent_x: float
    extent_y: float
    position_x: float
    position_y: float
    color_r: float
    color_g: float
    color_b: float
    color_a: float


class BlankStimulus(StimulusBase):
    stimulus_type: Literal["blank"]


class PresentationParameters(BaseModel):
    stimulus_start_time: float
    stimulus_duration: float
    response_window_start_time: float
    response_window_duration: float
    rewarded: bool
    reward_amount: int = Field(default=10, description="The reward amount, in milliseconds open time.")
    non_contingent_reward: bool
    timeout_duration: float
    timeout_stimulus: Annotated[
        Union[AudioStimulus, GratingStimulus, QuadStimulus, BlankStimulus], Field(discriminator="stimulus_type")
    ]
    post_response_time: float


class Trial(BaseModel):
    stimulus: Annotated[
        Union[AudioStimulus, GratingStimulus, QuadStimulus, BlankStimulus], Field(discriminator="stimulus_type")
    ]
    presentation_parameters: PresentationParameters


class TrialSet(BaseModel):
    available_trials: List[Trial]
    repeats: int


class Block(BaseModel):
    trial_sets: List[TrialSet]
    maximum_block_time: float


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
