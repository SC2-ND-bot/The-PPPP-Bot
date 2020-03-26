from actions.action import Action

class AttackMoveAction(Action):
	def __init__(self):
		super().__init__()
		self.cost = 2
		self.attackLocation = None

		# self.preconditions["attackingArea"] = False
		self.effects["attacking"] = True
		self.effects["movingTowardsEnemy"] = True

	def __repr__(self):
		return "Attack Move Action Class"

	# def calcCost(self):
	# 	# determine the cost for this action
	# 	# will be used during planning

	def reset(self):
		self.attackLocation = None

	def checkProceduralPrecondition(self, gameObject, agent):
		# This should generate a valid attackLocation
		attackLocation = gameObject.enemy_start_locations[0]
		self.attackLocation = attackLocation
		return True

	def perform(self, gameObject, unit, firstAction):
		gameObject.do(unit.attack(self.attackLocation, not firstAction))
