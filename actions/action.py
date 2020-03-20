

class Action:
    def  __init__(self):
        self.cost = 1
        self.gameObject = None
        self.preconditions = {}
        self.effects = {}

    def doReset(self):
        self.target = None
        self.reset()

    # override this method in each action
    def reset(self):
        raise NotImplementedError

    def checkProceduralPrecondition(self, agent):
        raise NotImplementedError

    def isDone(self):
        raise NotImplementedError

    def perform(self, firstAction):
        raise NotImplementedError

    # def addPrecondition(preconditionName, value):
    #     self.preconditions[preconditionName] = value

    # def removePrecondition(preconditionName):
    #     del self.preconditions[preconditionName]

    # def addEffect(effectName, value)
