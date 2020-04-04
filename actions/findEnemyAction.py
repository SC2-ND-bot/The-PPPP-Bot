from actions.action import Action

class FindEnemyAction(Action):
	def __init__(self):
		super().__init__()
		self.cost = 2
		self.attackLocation = None

		self.effects["attacking"] = True
		self.effects["retreating"] = False

	def __repr__(self):
		return "Attack Move Action Class"

	# def calcCost(self):
	# 	# determine the cost for this action
	# 	# will be used during planning

	def reset(self):
		self.attackLocation = None

	def checkProceduralPrecondition(self, gameObject, agent):
		unit = agent.getUnit(gameObject)
		enemies = gameObject.enemy_units()
		enemies_unit_can_attack = enemies.in_attack_range_of(unit, 0)

		if enemies_unit_can_attack.amount > 0:
			return False

		attackLocation = gameObject.enemy_start_locations[0]
		self.attackLocation = attackLocation
		return self.attackLocation is not None

	def perform(self, gameObject, unit, firstAction):
		gameObject.do(unit.attack(self.attackLocation, not firstAction))
