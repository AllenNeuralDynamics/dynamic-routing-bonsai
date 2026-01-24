import logging
from typing import Literal

import aind_behavior_services.task_logic.distributions as distributions
from aind_behavior_services.task_logic import AindBehaviorTaskLogicModel, TaskParameters
from pydantic import Field

from aind_behavior_dynamic_routing_bonsai import (
    __semver__,
)

logger = logging.getLogger(__name__)

# ==================== MAIN TASK LOGIC CLASSES ====================


class AindBehaviorDynamicRoutingBonsaiTaskParameters(TaskParameters):
    """
    Complete parameter specification for the dynamic-routing-bonsai task.
    """
    ...

class AindBehaviorDynamicRoutingBonsaiTaskLogic(AindBehaviorTaskLogicModel):
    """
    Main task logic model for the dynamic-routing-bonsai task.
    """

    version: Literal[__semver__] = __semver__
    name: Literal["AindBehaviorDynamicRoutingBonsai"] = Field(default="AindBehaviorDynamicRoutingBonsai", description="Name of the task logic", frozen=True)
    task_parameters: AindBehaviorDynamicRoutingBonsaiTaskParameters = Field(description="Parameters of the task logic")
