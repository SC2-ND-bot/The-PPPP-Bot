from actions.action import Action

class AttackEnemyAction(Action):
	def __init__(self):
		super().__init__()
		self.cost = 1
		self.enemy = None

		self.preconditions["canAttack"] = True
		self.effects["attacking"] = True
		self.effects["canAttack"] = False

	def __repr__(self):
		return "Attack Enemy Action Class"

	# def calcCost(self):
	# 	# determine the cost for this action
	# 	# will be used during planning

	def reset(self):
		self.enemy = None

	def checkProceduralPrecondition(self, gameObject, agent):
		unit = agent.getUnit(gameObject)

		# unit has to be able to attack
		if unit.weapon_cooldown != 0
			return False

		enemies = gameObject.enemy_units()
		enemies_unit_can_attack = enemies.in_attack_range_of(unit, 0)

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
