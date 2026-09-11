$scriptPath = Split-Path -Parent $MyInvocation.MyCommand.Path
Set-Location -Path (Split-Path -Parent $scriptPath)
uv run ./examples/rig.py
uv run ./examples/session.py
uv run ./examples/task_logic_stage0.py
./bonsai/bonsai.exe ./src/main_debug.bonsai -p SessionPath=../local/Session.json -p RigPath=../local/AindBehaviorDynamicRoutingBonsaiRig.json -p TaskLogicPath=../local/stage0_AindBehaviorDynamicRoutingBonsaiTaskLogic.json
