import logging
import os
from pathlib import Path
from typing import Optional

import pydantic
import pydantic_settings
from aind_behavior_services.session import AindBehaviorSessionModel
from aind_behavior_services.utils import model_from_json_file
from git import Repo

from aind_behavior_dynamic_routing_bonsai.rig import AindBehaviorDynamicRoutingBonsaiRig
from aind_behavior_dynamic_routing_bonsai.task_logic import AindBehaviorDynamicRoutingBonsaiTaskLogic

from ._rig import AindRigDataMapper
from ._session import AindSessionDataMapper
from ._utils import TrackedDevices, coerce_to_aind_data_schema, write_ads_mappers

__all__ = [
    "AindRigDataMapper",
    "AindSessionDataMapper",
    "DataMapperCli",
    "TrackedDevices",
    "coerce_to_aind_data_schema",
    "write_ads_mappers",
]

logger = logging.getLogger(__name__)


class DataMapperCli(pydantic_settings.BaseSettings, cli_kebab_case=True):
    """CLI for mapping session data to aind-data-schema format."""

    data_path: os.PathLike = pydantic.Field(description="Path to the session data directory.")
    repo_path: os.PathLike = pydantic.Field(
        default=Path("."), description="Path to the repository. By default it will use the current directory."
    )
    suffix: Optional[str] = pydantic.Field(
        default="dynamic-routing-bonsai", description="Suffix to append to output filenames."
    )

    def cli_cmd(self):
        logger.info("Mapping metadata directly from dataset.")
        abs_schemas_path = Path(self.data_path) / "Behavior" / "Logs"
        session = model_from_json_file(abs_schemas_path / "session_input.json", AindBehaviorSessionModel)
        rig = model_from_json_file(abs_schemas_path / "rig_input.json", AindBehaviorDynamicRoutingBonsaiRig)
        task_logic = model_from_json_file(
            abs_schemas_path / "tasklogic_input.json", AindBehaviorDynamicRoutingBonsaiTaskLogic
        )
        repo = Repo(self.repo_path)

        session_mapped = AindSessionDataMapper(
            session_model=session,
            rig_model=rig,
            task_logic_model=task_logic,
            repository=repo,
            script_path=Path("./src/main.bonsai"),
        ).map()

        rig_mapped = AindRigDataMapper(rig_model=rig).map()

        assert session.session_name is not None
        assert session_mapped is not None
        assert rig_mapped is not None

        session_mapped.instrument_id = rig_mapped.instrument_id
        session_mapped.write_standard_file(output_directory=Path(self.data_path), filename_suffix=self.suffix)
        rig_mapped.write_standard_file(output_directory=Path(self.data_path), filename_suffix=self.suffix)
        logger.info(
            "Mapping completed! Saved acquisition.json and instrument.json to %s",
            self.data_path,
        )


if __name__ == "__main__":
    pydantic_settings.CliApp().run(DataMapperCli)
