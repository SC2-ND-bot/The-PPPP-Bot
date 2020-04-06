from actions.action import Action
from sc2.position import Point2, Point3
import math

class RetreatAction(Action):
	def __init__(self):
		super().__init__()
		self.cost = -0.5
		self.retreatLocation = None

		self.effects["retreating"] = True
		self.effects["attacking"] = True

	def __repr__(self):
		return "Retreat Action Class"

	# def calcCost(self):
	# 	# determine the cost for this action
	# 	# will be used during planning

	def reset(self):
		self.retreatLocation = None

	def checkProceduralPrecondition(self, gameObject, agent):
		unit = agent.getUnit(gameObject)
		weapon_cooldown = min(unit.weapon_cooldown, 1.61)
		speed = unit.movement_speed
		distance_to_travel = (speed * weapon_cooldown)/2

		enemies = gameObject.enemy_units()

		if weapon_cooldown <= 0 and not agent.state['health_critical']:
			return False

		if enemies.amount <= 0:
			return False

		closest_enemy = enemies.closest_to(unit)

		x, y = self.calc_new_location(unit, closest_enemy, distance_to_travel)

		bound_x = gameObject._game_info.playable_area.x
		bound_y = gameObject._game_info.playable_area.y

		x = min(x, bound_x)
		y = min(y, bound_y)

		x = max(x, 0)
		y = max(y, 0)

		self.retreatLocation = Point2((x, y))
		return self.retreatLocation is not None

	def calc_new_location(self, unit, enemy, d):
		e_x = enemy.position[0]
		e_y = enemy.position[1]

		u_x = unit.position[0]
		u_y = unit.position[1]

		d_prime = math.sqrt((u_x - e_x)**2 + (u_y - e_y)**2)

		x = u_x - (d/d_prime) * (e_x - u_x)
		y = u_y - (d/d_prime) * (e_y- u_y)

		return (x, y)

	def perform(self, gameObject, agent, firstAction):
		unit = agent.getUnit(gameObject)
		gameObject.do(unit.move(self.retreatLocation, not firstAction))
