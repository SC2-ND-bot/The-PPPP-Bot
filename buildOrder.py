import random
import sc2
from sc2.ids.unit_typeid import UnitTypeId
from sc2 import Race

class buildtreeNode(sc2.BotAI):
    def __init__(self, contents, utype, utime, conditions, children, gameData):
        self.nodeContents = contents
        self.nodeType = utype # 0 is a unit, 1 is a building, and -1 is research
        self.reqTime = utime
        self.conditions = conditions
        self.children = children
        self.executed = False
        self.race = Race.Protoss
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
            if not condition:
                return False
        return True

class buildOrder(sc2.BotAI):
    def __init__(self, gameData):
        self.l12 = buildtreeNode(UnitTypeId.ZEALOT, 0, 0, [True], [], gameData)
        self.l11 = buildtreeNode(UnitTypeId.ZEALOT, 0, 0, [True], [self.l12], gameData)
        self.l10 = buildtreeNode(UnitTypeId.ZEALOT, 0, 0, [True], [self.l11], gameData)
        self.l9 = buildtreeNode(UnitTypeId.ZEALOT, 0, 0, [True], [self.l10], gameData)
        self.l8_2 = buildtreeNode(UnitTypeId.GATEWAY, 1, 0, [True], [self.l9], gameData)
        self.l8_1 = buildtreeNode(UnitTypeId.ZEALOT, 0, 0, [False], [self.l9], gameData)
        self.l7 = buildtreeNode(UnitTypeId.ZEALOT, 0, 0, [True], [self.l8_1, self.l8_2], gameData) # See here for tree branching example
        self.l6 = buildtreeNode(UnitTypeId.GATEWAY, 1, 0, [True], [self.l7], gameData)
        self.l5 = buildtreeNode(UnitTypeId.PYLON, 1, 0, [True], [self.l6], gameData)
        self.l4 = buildtreeNode(UnitTypeId.PYLON, 1, 0, [True], [self.l5], gameData)
        self.l3 = buildtreeNode(UnitTypeId.PROBE, 0, 0, [True], [self.l4], gameData)
        self.l2 = buildtreeNode(UnitTypeId.PROBE, 0, 0, [True], [self.l3], gameData)
        self.l1 = buildtreeNode(UnitTypeId.PROBE, 0, 0, [True], [self.l2], gameData)
        self.curr = self.l1

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