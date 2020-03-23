import random
import json
import sc2
from sc2 import Race
from sc2.ids.unit_typeid import UnitTypeId
from sc2.ids.upgrade_id import UpgradeId

class buildtreeNode(sc2.BotAI):
    def __init__(self, contents, utype, utime, conditions, children, gameData, enemy_race):
        self.nodeContents = contents
        self.nodeType = utype # 0 is a unit, 1 is a building, and -1 is research
        self.reqTime = utime
        self.conditions = conditions
        self.children = children
        self.executed = False
        self.race = Race.Protoss
        self.enemyRace = enemy_race
        self._game_data = gameData
        self.minerals = 0
        self.vespene = 0
        self.supply_left = 0
        self.state = 0
    
    def executeContents(self):
        return [self.nodeContents, self.nodeType]

    def choosePath(self):
        for child in self.children:
            if child.checkConditions(False):
                return child
        return None

    def checkConditions(self, executing):
        if executing:
            if not self.can_afford(self.nodeContents):
                return False
            if self.time < self.reqTime:
                return False
        for condition in self.conditions:
            if condition[0] == "race":
                if Race(condition[1]) != self.enemyRace and self.enemyRace != Race.Random:
                    return False
        return True

class buildOrder(sc2.BotAI):
    def __init__(self, gameData, enemy_race):
        self.tree = self.constructTree(gameData, enemy_race)
        self.curr = self.tree
    
    def constructTree(self, gameData, enemy_race):
        with open('buildOrder.json', 'r') as f:
            treeJSON = json.load(f)["buildOrder"]
            root = self.constructNode(treeJSON, treeJSON["l0"], gameData, enemy_race)
        return root
        
    def constructNode(self, treeJSON, nodeJSON, gameData, enemy_race):
        children = []
        for child in nodeJSON["children"]:
            children.append(self.constructNode(treeJSON, treeJSON[child], gameData, enemy_race))
        if nodeJSON["type"] == -1:
            return buildtreeNode(UpgradeId(nodeJSON["contents"]), nodeJSON["type"], nodeJSON["time"], nodeJSON["conditions"], children, gameData, enemy_race)
        return buildtreeNode(UnitTypeId(nodeJSON["contents"]), nodeJSON["type"], nodeJSON["time"], nodeJSON["conditions"], children, gameData, enemy_race)

    def stepDown(self, minerals, vespene, supply_left, state):
        result = None
        self.curr.minerals = minerals
        self.curr.vespene = vespene
        self.curr.supply_left = supply_left
        self.curr.state = state
        if self.curr.executed == False and self.curr.checkConditions(True) == True:
            result = self.curr.executeContents()
        next = self.curr.choosePath()
        if next != None and self.curr.executed == True:
            self.curr = next
        return result