from actions.action import Action

class RetreatAction(Action):
	def __init__(self):
		super().__init__()
		self.cost = 1
		self.retreatLocation = None

		# self.preconditions["attackingArea"] = False
		self.preconditions["canAttack"] = False
		self.effects["retreating"] = True
		self.effects["canAttack"] = True
		self.effects["attacking"] = False

	def __repr__(self):
		return "Retreat Action Class"

	# def calcCost(self):
	# 	# determine the cost for this action
	# 	# will be used during planning

	def reset(self):
		self.retreatLocation = None

	def checkProceduralPrecondition(self, gameObject, agent):
		unit = agent.getUnit(gameObject)

		weapon_cooldown = unit.weapon_cooldown
		# unit can't be able to attack
		if weapon_cooldown =< 0:
			return False

		speed = unit.movement_speed

		distance_to_travel = speed * weapon_cooldown

		weapon_cooldown
		closest_enemy = gameObject.enemy_units().closest_to(unit)

		e_x = closest_enemy.position[0]
		e_y = closest_enemy.position[1]

		u_x = unit.position[0]
		u_y = unit.position[1]

		slope = (u_y - e_y)/(u_x - e_y)

		line_equation = lambda x: slope * (x - u_x) + u_y



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
