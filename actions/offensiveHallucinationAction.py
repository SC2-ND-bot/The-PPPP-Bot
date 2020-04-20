from actions.action import Action
from sc2.position import Point2, Point3

import time
import math

class OffensiveHallucinationAction(Action):
	def __init__(self):
		super().__init__()
		self.cost = 3.0
        self.hallucinationId = None

		self.preconditions["attacking"] = True
		self.effects["lastHallucinations"] = None

	def __repr__(self):
		return "Hallucination Action Class"

	def reset(self):
        self.hallucinationId = None

	def checkProceduralPrecondition(self, gameObject, agent):
		unit = agent.getUnit(gameObject)
        energy = unit.energy

        if unit.energy < 75 or unit.type_id != UnitTypeId.SENTRY:
			return False

        self.hallucinationId = AbilityId.HALLUCINATION_COLOSSUS

		return self.hallucinationId is not None

	def perform(self, gameObject, agent, firstAction):
        unit = agent.getUnit(gameObject)
        gameObject.do(unit(self.hallucinationId))
