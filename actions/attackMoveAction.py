from actions.action import Action

class AttackMoveAction(Action):
    def __init__(self, agent, gameObject):
        # add preconditions
        # add effects

        self.agent = agent
        self.gameObject = gameObject

        self.cost = calcCost()

        self.attackLocation = None
        self.moving = False

    def calcCost(self):
        # determine the cost for this action
        # will be used during planning

    def reset(self):
        self.attackLocation = None
        self.moving = False

    def canBeInterrupted(self):
        return True

    def checkProceduralPrecondition(self):
        # This should generate a valid attackLocation

        attackLocation = self.gameObject.enemy_start_locations[0]

        self.attackLocation = attackLocation

    def isDone(self):
        return self.moving

    def perform(self):
        self.gameObject.do(self.agent.attack(self.attackLocation))
