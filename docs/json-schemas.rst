json-schema
-------------
The following json-schemas are used as the format definition of the input for this task. They are the result of the `Pydantic`` models defined in `src/aind_behavior_dynamic_routing_bonsai`, and are also used to generate `src/Extensions/AindBehaviorDynamicRoutingBonsai.cs` via `Bonsai.Sgen`.

`Download Schema <https://raw.githubusercontent.com/AllenNeuralDynamics/Aind.Behavior.DynamicRoutingBonsai/main/src/DataSchemas/aind_behavior_dynamic_routing_bonsai.json>`_

Task Logic Schema
~~~~~~~~~~~~~~~~~
.. jsonschema:: https://raw.githubusercontent.com/AllenNeuralDynamics/Aind.Behavior.DynamicRoutingBonsai/main/src/DataSchemas/aind_behavior_dynamic_routing_bonsai.json#/$defs/AindBehaviorDynamicRoutingBonsaiTaskLogic
   :lift_definitions:
   :auto_reference:


Rig Schema
~~~~~~~~~~~~~~
.. jsonschema:: https://raw.githubusercontent.com/AllenNeuralDynamics/Aind.Behavior.DynamicRoutingBonsai/main/src/DataSchemas/aind_behavior_dynamic_routing_bonsai.json#/$defs/AindBehaviorDynamicRoutingBonsaiRig
   :lift_definitions:
   :auto_reference:
