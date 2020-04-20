from actions.action import Action
from sc2.position import Point2, Point3
import math

class FindChokePoint(Action):
	def __init__(self):
		super().__init__()
		self.cost = 1
		self.defensivePosition = None

		self.effects["defendBase"] = True
		self.effects["attacking"] = False

	def __repr__(self):
		return "Find Choke Point Class"

	def reset(self):
		self.defensivePosition = None

	def calc_defensive_position(self, nexus, enemy, d):
		e_x = enemy.position[0]
		e_y = enemy.position[1]

		u_x = nexus.position[0]
		u_y = nexus.position[1]

		d_prime = math.sqrt((u_x - e_x)**2 + (u_y - e_y)**2)

		x = u_x + (d/d_prime) * (e_x - u_x)
		y = u_y + (d/d_prime) * (e_y - u_y)

		return (x, y)


	def checkProceduralPrecondition(self, gameObject, agent):
		nearestNexus = gameObject.townhalls().closest_to(gameObject.enemy_start_locations[0])
		x, y = self.calc_defensive_position(nearestNexus, gameObject.enemy_start_locations[0], 11)

		self.defensivePosition = Point2((x, y))
		if agent.getUnit(gameObject).distance_to(self.defensivePosition) < 15:
			return False

		return self.defensivePosition is not None

	def perform(self, gameObject, agent, firstAction):
		unit = agent.getUnit(gameObject)
		gameObject.do(unit.move(self.defensivePosition, False))
		gameObject.do(unit.attack(self.defensivePosition, True))
