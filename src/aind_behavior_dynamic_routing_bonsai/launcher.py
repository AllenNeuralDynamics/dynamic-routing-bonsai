import datetime
import logging
from pathlib import Path

from aind_behavior_curriculum import TrainerState
from aind_behavior_services.session import Session
from aind_behavior_services.utils import utcnow
from clabe import resource_monitor, ui
from clabe.apps import AindBehaviorServicesBonsaiApp, CurriculumApp, CurriculumSettings, CurriculumSuggestion
from clabe.data_transfer.aind_watchdog import WatchdogDataTransferService, WatchdogSettings
from clabe.launcher import Launcher, LauncherCliArgs, experiment
from clabe.session import SessionBuilder
from clabe.stores import Kind, LocalFileStore, Store
from pydantic_settings import CliApp

from .data_mappers import AindRigDataMapper, AindSessionDataMapper
from .rig import AindBehaviorDynamicRoutingBonsaiRig
from .task_logic import AindBehaviorDynamicRoutingBonsaiTaskLogic

logger = logging.getLogger(__name__)

_CONFIG_LIBRARY = Path(r"\\allen\aind\scratch\AindBehavior.db\AindBehaviorDynamicRoutingBonsai")
_RIG = Kind.from_rig(AindBehaviorDynamicRoutingBonsaiRig)
_TASK_LOGIC = Kind.from_task(AindBehaviorDynamicRoutingBonsaiTaskLogic)
_TRAINER_STATE = Kind.from_trainer_state()


@experiment(name="dynamic-routing-bonsai")
async def dynamic_routing_bonsai_experiment(launcher: Launcher) -> None:
    # Get user input
    session = SessionBuilder(launcher).build()
    store = LocalFileStore(_CONFIG_LIBRARY).scoped(subject=session.subject)
    trainer_state = _resolve_trainer_state(store)
    if trainer_state is not None and trainer_state.stage is not None:
        task_logic = AindBehaviorDynamicRoutingBonsaiTaskLogic.model_validate_json(
            trainer_state.stage.task.model_dump_json()
        )
    else:
        task_logic = store.resolve(_TASK_LOGIC)
    rig = store.resolve(_RIG)

    launcher.register_session(session, rig.data_directory)

    # Check resources
    resource_monitor.ResourceMonitor(
        constrains=[
            resource_monitor.available_storage_constraint_factory(rig.data_directory, 2e11),
        ]
    ).run()

    # Run the task via Bonsai
    bonsai_app = AindBehaviorServicesBonsaiApp(
        workflow=Path(r"./src/main.bonsai"),
        temp_directory=launcher.temp_dir,
        rig=rig,
        session=session,
        task=task_logic,
    )
    await bonsai_app.run_async()
    session_end_time = utcnow()

    # Curriculum
    suggestion = await _run_curriculum_if_applicable(launcher, store, trainer_state)

    # Mappers
    _run_data_mappers(launcher, session, rig, task_logic, session_end_time, suggestion)

    # Watchdog
    launcher.copy_logs()
    WatchdogDataTransferService(
        source=launcher.session_directory,
        settings=WatchdogSettings(),  # type: ignore[call-arg]
        session=session,
    ).transfer()


def _resolve_trainer_state(store: Store) -> TrainerState | None:
    try:
        return store.resolve(_TRAINER_STATE)
    except LookupError:
        logger.info("No trainer state found for subject. Falling back to picking a task logic.")
        return None


async def _run_curriculum_if_applicable(
    launcher: Launcher, store: Store, trainer_state: TrainerState | None
) -> CurriculumSuggestion | None:
    if trainer_state is None or trainer_state.is_on_curriculum is False or trainer_state.stage is None:
        return None
    logs_directory = launcher.session_directory / "Behavior" / "Logs"
    logs_directory.mkdir(parents=True, exist_ok=True)
    input_trainer_state_path = logs_directory / "trainer_state.json"
    input_trainer_state_path.write_text(trainer_state.model_dump_json(indent=2), encoding="utf-8")

    curriculum_app = CurriculumApp(
        settings=CurriculumSettings(
            input_trainer_state=input_trainer_state_path.resolve(),
            data_directory=launcher.session_directory,
        )
    )
    await curriculum_app.run_async()
    suggestion = curriculum_app.process_suggestion()
    (logs_directory / "suggestion.json").write_text(suggestion.model_dump_json(indent=2), encoding="utf-8")
    store.write(_TRAINER_STATE, suggestion.trainer_state)
    return suggestion


def _run_data_mappers(
    launcher: Launcher,
    session: Session,
    rig: AindBehaviorDynamicRoutingBonsaiRig,
    task_logic: AindBehaviorDynamicRoutingBonsaiTaskLogic,
    session_end_time: datetime.datetime,
    suggestion: CurriculumSuggestion | None,
) -> None:
    try:
        session_mapped = AindSessionDataMapper(
            session_model=session,
            rig_model=rig,
            task_logic_model=task_logic,
            repository=launcher.repository,
            session_end_time=session_end_time,
            curriculum_suggestion=suggestion,
        ).map()
        rig_mapped = AindRigDataMapper(rig_model=rig).map()
        assert session_mapped is not None
        session_mapped.instrument_id = rig_mapped.instrument_id
        session_mapped.write_standard_file(output_directory=launcher.session_directory)
        rig_mapped.write_standard_file(output_directory=launcher.session_directory)
    except Exception as e:  # mapping failures must not discard completed session data
        logger.error("Failed to map session metadata: %s", e)
        ui.notify(f"Failed to map session metadata: {e}", ui.MessageLevel.ERROR)


class ClabeCli(LauncherCliArgs):
    def cli_cmd(self):
        launcher = Launcher(settings=self)
        launcher.run_experiment(dynamic_routing_bonsai_experiment)
        return None


def main() -> None:
    CliApp().run(ClabeCli)


if __name__ == "__main__":
    main()
