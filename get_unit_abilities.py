import json
from sc2.constants import *
from sc2.game_data import GameData
from collections import OrderedDict
from typing import Dict, Set, List, Union, Optional

class OrderedDict2(OrderedDict):
    def __repr__(self):
        if not self:
            return "{}"
        return (
            "{"
            + ", ".join(f"{repr(key)}: {repr(value)}" for key, value in sorted(self.items(), key=lambda u: u[0].name))
            + "}"
        )


class OrderedSet2(set):
    def __repr__(self):
        if not self:
            return "set()"
        return "{" + ", ".join(repr(item) for item in sorted(self, key=lambda u: u.name)) + "}"


with open("data.json") as f:
    data = json.load(f)

ability_data = data["Ability"]
unit_data = data["Unit"]
upgrade_data = data["Upgrade"]

all_unit_abilities: Dict[UnitTypeId, Set[AbilityId]] = OrderedDict2()
entry: dict
for entry in unit_data:
	entry_unit_abilities = entry.get("abilities", [])
	unit_type = UnitTypeId(entry["id"])
	current_collected_unit_abilities: Set[AbilityId] = OrderedSet2()
	for ability_info in entry_unit_abilities:
		ability_id_value: int = ability_info.get("ability", 0)
		if ability_id_value:
			ability_id: AbilityId = AbilityId(ability_id_value)
			current_collected_unit_abilities.add(ability_id)
	
	if entry["race"] == "Protoss":
		print(unit_type, current_collected_unit_abilities)
		print("")
	if current_collected_unit_abilities:
		all_unit_abilities[unit_type] = current_collected_unit_abilities
