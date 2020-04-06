from actions.action import Action
from sc2.position import Point2, Point3

import time
import math

class Scout(Action):
	def __init__(self):
		super().__init__()
		self.cost = 2.0
		self.scoutLocations = None

		self.preconditions["hallucinationCreated"] = True
		self.effects["scouted"] = True

	def __repr__(self):
		return "Hallucination Action Class"

	def reset(self):
		self.scoutLocations = None

	def checkProceduralPrecondition(self, gameObject, agent):
		unit = agent.getUnit(gameObject)

		if not unit.is_hallucination:
			return False

		self.scoutLocations = [gameObject.enemy_start_locations[0]]

		return self.scoutLocations is not None

	def perform(self, gameObject, agent, firstAction):
		unit = agent.getUnit(gameObject)
		for index, location in enumerate(self.scoutLocations):
			gameObject.do(unit.move(location, index != 0))
