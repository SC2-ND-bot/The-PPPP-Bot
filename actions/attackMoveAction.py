from actions.action import Action

class AttackMoveAction(Action):
	def __init__(self, agent, gameObject):
		super().__init__()

		self.agent = agent
		self.gameObject = gameObject
		self.cost = 1
		self.attackLocation = None

		# self.preconditions["attackingArea"] = False
		self.effects["attackingArea"] = True
		self.effects["movingTowardsEnemy"] = True

	def __repr__(self):
		return "Attack Move Action Class"

	# def calcCost(self):
	# 	# determine the cost for this action
	# 	# will be used during planning

	def reset(self):
		self.attackLocation = None

	def checkProceduralPrecondition(self, agent):
		# This should generate a valid attackLocation
		attackLocation = self.gameObject.enemy_start_locations[0]
		self.attackLocation = attackLocation
		return True

	def perform(self, firstAction):
		self.gameObject.do(self.agent.unit.attack(self.attackLocation, not firstAction))
