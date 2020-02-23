from agents.agent import Agent

from actions.attackEnemyAction import AttackEnemyAction
from actions.attackMoveAction import AttackMoveAction
from actions.retreatAction import RetreatAction

class AdeptAgent(Agent):

    def __init__(self, unit = None):
        super().__init__(unit=unit)

    def loadActions(self):
        self.availableActions.append(AttackEnemyAction())
        self.availableActions.append(RetreatAction())
        self.availableActions.append(AttackMoveAction())


