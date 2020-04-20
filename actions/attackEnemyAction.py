from actions.action import Action

class AttackEnemyAction(Action):
	def __init__(self):
		super().__init__()
		self.cost = 1
		self.enemy = None

		self.effects["attacking"] = True
		self.effects["retreating"] = False

	def __repr__(self):
		return "Attack Enemy Action Class"

	# def calcCost(self):
	# 	# determine the cost for this action
	# 	# will be used during planning

	def reset(self):
		self.enemy = None
		self.cost = 1

	def checkProceduralPrecondition(self, gameObject, agent):
		unit = agent.getUnit(gameObject)

		if unit.weapon_cooldown > 0:
			return False

		enemies = gameObject.enemy_units()
		unit_attack_range = max(unit.ground_range, unit.air_range)
		
		enemies_unit_can_attack = enemies.in_attack_range_of(unit, (unit.sight_range - unit_attack_range))

		enemy_to_attack = None
		for enemy in enemies_unit_can_attack:
			if enemy_to_attack is None:
				enemy_to_attack = enemy
			elif enemy_to_attack.is_structure and not enemy.is_structure:
				enemy_to_attack = enemy
			else:
				if enemy_to_attack.shield_health_percentage > enemy.shield_health_percentage and not enemy.is_structure:
					enemy_to_attack = enemy

		self.enemy = enemy_to_attack

		return self.enemy is not None

	def perform(self, gameObject, agent, firstAction):
		unit = agent.getUnit(gameObject)
		gameObject.do(unit.attack(self.enemy, not firstAction))
