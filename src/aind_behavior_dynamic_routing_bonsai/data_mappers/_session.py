import datetime
import logging
import os
from pathlib import Path
from typing import Dict, Optional, Union

import git
import pydantic
from aind_behavior_services.session import Session
from aind_data_schema.core import acquisition
from clabe.apps import CurriculumSuggestion
from clabe.data_mapper import aind_data_schema as ads

from aind_behavior_dynamic_routing_bonsai.rig import AindBehaviorDynamicRoutingBonsaiRig
from aind_behavior_dynamic_routing_bonsai.task_logic import AindBehaviorDynamicRoutingBonsaiTaskLogic

logger = logging.getLogger(__name__)


class AindSessionDataMapper(ads.AindDataSchemaSessionDataMapper):
    """Maps the task-specific session model to the aind-data-schema Acquisition model."""

    def __init__(
        self,
        session_model: Session,
        rig_model: AindBehaviorDynamicRoutingBonsaiRig,
        task_logic_model: AindBehaviorDynamicRoutingBonsaiTaskLogic,
        repository: Union[os.PathLike, git.Repo] = Path("."),
        script_path: os.PathLike = Path("./src/main.bonsai"),
        session_end_time: Optional[datetime.datetime] = None,
        curriculum_suggestion: Optional[CurriculumSuggestion] = None,
        output_parameters: Optional[Dict] = None,
    ):
        self.session_model = session_model
        self.rig_model = rig_model
        self.task_logic_model = task_logic_model
        self.repository = repository
        if isinstance(self.repository, os.PathLike | str):
            self.repository = git.Repo(Path(self.repository))
        self.script_path = script_path
        self._session_end_time = session_end_time
        self.output_parameters = output_parameters
        self._mapped: Optional[acquisition.Acquisition] = None
        self.curriculum = curriculum_suggestion

    @property
    def session_end_time(self) -> datetime.datetime:
        if self._session_end_time is None:
            raise ValueError("Session end time is not set.")
        return self._session_end_time

    def session_schema(self):
        return self.mapped

    @property
    def session_name(self) -> str:
        if self.session_model.session_name is None:
            raise ValueError("Session name is not set in the session model.")
        return self.session_model.session_name

    @property
    def mapped(self) -> acquisition.Acquisition:
        if self._mapped is None:
            raise ValueError("Data has not been mapped yet.")
        return self._mapped

    def is_mapped(self) -> bool:
        return self._mapped is not None

    def map(self) -> Optional[acquisition.Acquisition]:
        logger.info("Mapping aind-data-schema Session.")
        try:
            self._mapped = self._map()
        except (pydantic.ValidationError, ValueError, IOError) as e:
            logger.error("Failed to map to aind-data-schema Session. %s", e)
            raise e
        else:
            return self._mapped

    def _map(self) -> acquisition.Acquisition:
        # TODO: Implement session mapping to aind-data-schema Acquisition
        # See VrForaging implementation for reference:
        # https://github.com/AllenNeuralDynamics/Aind.Behavior.VrForaging/blob/main/src/aind_behavior_vr_foraging/data_mappers/_session.py
        raise NotImplementedError("Session mapping not implemented yet.")
