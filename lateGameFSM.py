import json
import sc2
from sc2 import Race
from sc2.ids.unit_typeid import UnitTypeId
from sc2.ids.upgrade_id import UpgradeId

class lateGameFSM:
    def __init__(self, enemy_race):
        self.enemyRace = enemy_race
        self.counterDict = self.buildCounterDict()

    def buildCounterDict(self):
        if self.enemyRace == Race.Zerg:
            with open('lateGameCounters.json', 'r') as f:
                counters = json.load(f)["zerg"]
                return counters
        return {}
    
    def analyze_friendly_buildings(self, friendlyBuildings):
        friendlyBuildings = [building.type_id for building in friendlyBuildings]
        buildingsNeeded = [62, 63, 64, 65, 67, 68, 69, 70, 71, 72]
        buildingsToBuild = []
        for structure in buildingsNeeded:
            if UnitTypeId(structure) not in friendlyBuildings:
                buildingsToBuild.append((UnitTypeId(structure), "building"))
        return buildingsToBuild

    def analyze_enemy_counters(self, enemyUnits, enemyBuildings):
        unitsToBuild = []
        for unit in set(enemyUnits):
            unitsToBuild.append((UnitTypeId(self.counterDict.get(str(unit.type_id.value), 0)), "unit"))
        for building in enemyBuildings:
            unitsToBuild.append((UnitTypeId(self.counterDict.get(str(building.type_id.value), 0)), "unit"))
        return unitsToBuild

    def getInstructions(self, friendlyBuildings, enemyUnits, enemyBuildings):
        return set(self.analyze_enemy_counters(enemyUnits, enemyBuildings) + self.analyze_friendly_buildings(friendlyBuildings)) 
        