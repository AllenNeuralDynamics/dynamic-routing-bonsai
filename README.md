# aind-behavior-dynamic-routing-bonsai

![CI](https://github.com/AllenNeuralDynamics/Aind.Behavior.DynamicRoutingBonsai/actions/workflows/aind-behavior-dynamic-routing-bonsai-cicd.yml/badge.svg)
[![License](https://img.shields.io/badge/license-MIT-brightgreen)](LICENSE)
[![ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json)](https://github.com/astral-sh/ruff)
[![uv](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/uv/main/assets/badge/v0.json)](https://github.com/astral-sh/uv)

A library that defines AIND data schema for a behavior experiment.

---

## General instructions

This repository follows the project structure laid out in the [Aind.Behavior.Services repository](https://github.com/AllenNeuralDynamics/Aind.Behavior.Services).

---

## Prerequisites

[Pre-requisites for running the project can be found here](https://allenneuraldynamics.github.io/Aind.Behavior.Services/articles/requirements.html).

---

## Deployment

For convenience, once third-party dependencies are installed, `Bonsai` and `python` virtual environments can be bootstrapped by running:

```powershell
./scripts/deploy.ps1
```

from the root of the repository.

## Generating settings files

The task is instantiated by a set of three settings files that strictly follow a DSL schema. These files are:

- `task_logic.json`
- `rig.json`
- `session.json`

Examples on how to generate these files can be found in the `./examples` directory of the repository. Once generated, these are the only required inputs to run the Bonsai workflow in `./src/main.bonsai`.

The workflow can thus be executed using the [Bonsai CLI](https://bonsai-rx.org/docs/articles/cli.html):

```powershell
./bonsai/bonsai.exe ./src/main.bonsai -p SessionPath=<path-to-session.json> -p RigPath=<path-to-rig.json> -p TaskLogicPath=<path-to-task_logic.json>
```

Since some parameters are generated per-experiment (e.g. data of experiment session), it can be useful to use a launcher to generate settings files and initiate the workflow in a single step, for example:

```
$scriptPath = Split-Path -Parent $MyInvocation.MyCommand.Path
Set-Location -Path (Split-Path -Parent $scriptPath)
uv run ./examples/rig.py
uv run ./examples/session.py
uv run ./examples/task_logic_stage0.py
./bonsai/bonsai.exe ./src/main.bonsai -p SessionPath=../local/Session.json -p RigPath=../local/AindBehaviorDynamicRoutingBonsaiRig.json -p TaskLogicPath=../local/stage0_AindBehaviorDynamicRoutingBonsaiTaskLogic.json
```

would generate all three settings files based on the current generation scripts in `examples` and launch the workflow with these settings. An example is given in `scripts/launcher.ps1`.

## Primary data quality-control (not yet implemented)

Once an experiment is collected, the primary data quality-control script can be run to check the data for issues. This script can be launched using:

```powershell
uv run dynamic-routing-bonsai data-qc <path-to-data-dir>
```

## Mapping to aind-data-schema (not yet implemented)

Once an experiment is collected, data can be mapped to aind-data-schema using the `data-mapper` sub-command:

```powershell
uv run dynamic-routing-bonsai data-mapper --data-path <path-to-data-dir>
```

## Regenerating schemas

DSL schemas can be modified in `./src/aind_behavior_dynamic_routing_bonsai/rig.py` (or `(...)/task_logic.py`).

Once modified, changes to the DSL must be propagated to `json-schema` and `csharp` API. This can be done by running:

```powershell
uv run dynamic-routing-bonsai regenerate
```
