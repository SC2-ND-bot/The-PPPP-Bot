from actions.action import Action
from sc2.ids.unit_typeid import UnitTypeId

class FindEnemyAction(Action):
	def __init__(self):
		super().__init__()
		self.cost = 2
		self.attackLocation = None

		self.effects["attacking"] = True
		self.effects["retreating"] = False
		self.effects["defendBase"] = False
		self.effects["surveillance"] = True

	def __repr__(self):
		return "Find Enemy Action Class"

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

		if len(gameObject.enemy_structures(UnitTypeId.HATCHERY)) > 0:
			self.attackLocation = gameObject.enemy_structures(UnitTypeId.HATCHERY)[0]
		else:
			attackLocation = gameObject.enemy_start_locations[0]
			self.attackLocation = attackLocation

		return self.attackLocation is not None

	def perform(self, gameObject, agent, firstAction):
		unit = agent.getUnit(gameObject)
		gameObject.do(unit.attack(self.attackLocation, not firstAction))
