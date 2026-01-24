import typing as t

from pydantic import Field, RootModel
from pydantic_settings import BaseSettings, CliApp, CliSubCommand

from aind_behavior_dynamic_routing_bonsai import __semver__, regenerate
from aind_behavior_dynamic_routing_bonsai.data_mappers import DataMapperCli
from aind_behavior_dynamic_routing_bonsai.data_qc import DataQcCli
from aind_behavior_dynamic_routing_bonsai.launcher import ClabeCli


class VersionCli(RootModel):
    root: t.Any

    def cli_cmd(self) -> None:
        print(__semver__)


class DslRegenerateCli(RootModel):
    root: t.Any

    def cli_cmd(self) -> None:
        regenerate.main()


class DynamicRoutingBonsai(BaseSettings, cli_prog_name="dynamic-routing-bonsai", cli_kebab_case=True):
    data_mapper: CliSubCommand[DataMapperCli] = Field(description="Generate metadata for aind-data-schema.")
    data_qc: CliSubCommand[DataQcCli] = Field(description="Run data quality checks.")
    version: CliSubCommand[VersionCli] = Field(
        description="Print the version of the dynamic-routing-bonsai package.",
    )
    regenerate: CliSubCommand[DslRegenerateCli] = Field(
        description="Regenerate the dynamic-routing-bonsai dsl dependencies.",
    )
    clabe: CliSubCommand[ClabeCli] = Field(
        description="Run the Clabe CLI.",
    )

    def cli_cmd(self):
        return CliApp().run_subcommand(self)


def main():
    CliApp().run(DynamicRoutingBonsai)


if __name__ == "__main__":
    main()
