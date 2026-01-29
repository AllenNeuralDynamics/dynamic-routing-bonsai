import logging
from typing import Literal, List, Annotated, Union
from enum import Enum

import aind_behavior_services.task_logic.distributions as distributions
from aind_behavior_services.task_logic import AindBehaviorTaskLogicModel, TaskParameters
from pydantic import Field, BaseModel

from aind_behavior_dynamic_routing_bonsai import (
    __semver__,
)

logger = logging.getLogger(__name__)

# ==================== MAIN TASK LOGIC CLASSES ====================

class StimulusBase(BaseModel):
    stimulus_type: str
    
class AudioStimulus(StimulusBase):
    stimulus_type: Literal["audio"]
    frequency: float
    
class GratingStimulus(StimulusBase):
    stimulus_type: Literal["grating"]
    angle: float
    aperture: float
    extent_x: float
    extent_y: float
    spatial_frequency: float
    temporal_frequency: float
    
class BlankStimulus(StimulusBase):
    stimulus_type: Literal["blank"]

class PresentationParameters(BaseModel):
    stimulus_start_time: float
    stimulus_duration: float
    response_window_start_time: float
    response_window_duration: float
    inter_trial_interval: float
    rewarded: bool
    non_contingent_reward: bool
    timeout: float
    
class Trial(BaseModel):
    stimulus: Annotated[Union[AudioStimulus, GratingStimulus, BlankStimulus], Field(discriminator="stimulus_type")]
    presentation_parameters: PresentationParameters

class TrialResultEnum(str, Enum):
    HIT = "Hit"
    FA = "FalseAlarm"
    CR = "CorrectRejection"
    MISS = "Miss"

class TrialResult(BaseModel):
    result: TrialResultEnum

class TrialSet(BaseModel):
    available_trials: List[Trial]
    repeats: int
 
class Block(BaseModel):
    trial_sets: List[TrialSet]
    maxmimum_block_time: float

class AindBehaviorDynamicRoutingBonsaiTaskParameters(TaskParameters):
    """
    Complete parameter specification for the dynamic-routing-bonsai task.
    """
    task_blocks: List[Block]

class AindBehaviorDynamicRoutingBonsaiTaskLogic(AindBehaviorTaskLogicModel):
    """
    Main task logic model for the dynamic-routing-bonsai task.
    """

    version: Literal[__semver__] = __semver__
    name: Literal["AindBehaviorDynamicRoutingBonsai"] = Field(default="AindBehaviorDynamicRoutingBonsai", description="Name of the task logic", frozen=True)
    task_parameters: AindBehaviorDynamicRoutingBonsaiTaskParameters = Field(description="Parameters of the task logic")
