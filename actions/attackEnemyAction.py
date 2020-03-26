from actions.action import Action

class AttackEnemyAction(Action):
	def __init__(self):
		super().__init__()
		self.cost = 1
		self.attackLocation = None

		# self.preconditions["attackingArea"] = False
		self.effects["attacking"] = True
		self.effects["movingTowardsEnemy"] = True

	def __repr__(self):
		return "Attack Enemey Action Class"

	# def calcCost(self):
	# 	# determine the cost for this action
	# 	# will be used during planning

	def reset(self):
		self.enemy = None
		self.attackLocation = None


	def checkProceduralPrecondition(self, gameObject, agent):
		# This should generate a valid attackLocation
		enemies = gameObject.enemy_units()
		unit = agent.getUnit(gameObject)
		enemies_unit_can_attack = enemies.in_attack_range_of(unit, 3)

		enemy_to_attack = None
		for enemy in enemies_unit_can_attack:
			if enemy_to_attack is None:
				enemy_to_attack = enemy
			else:
				if enemy_to_attack.shield_health_percentage > enemy.shield_health_percentage:
					enemy_to_attack = enemy

		self.enemy = enemy_to_attack

		return enemy_to_attack is not None

	def perform(self, gameObject, unit, firstAction):
		gameObject.do(unit.attack(self.enemy, not firstAction))
