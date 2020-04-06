from actions.action import Action
from sc2.position import Point2, Point3
from sc2.ids.ability_id import AbilityId

import time
import math

class ScoutHallucinationAction(Action):
	def __init__(self):
		super().__init__()
		self.cost = 2.0
		self.hallucinationId = None
		self.effects["lastScoutTimestamp"] = None
		self.effects["hallucinationCreated"] = True

	def __repr__(self):
		return "Hallucination Action Class"

	def reset(self):
		self.hallucinationId = None

	def checkProceduralPrecondition(self, gameObject, agent):
		unit = agent.getUnit(gameObject)
		energy = unit.energy
		if unit.energy < 75:
			return False

		lastScout = agent.state["lastScoutTimestamp"]
		currentTimestamp = time.time()
		if lastScout is not None:
			if currentTimestamp - lastScout > 45:
				self.effects['lastScoutTimestamp'] = currentTimestamp
				self.hallucinationId = AbilityId.HALLUCINATION_PHOENIX
			else:
				agent.state['scouted'] = False
		else:
			self.effects['lastScoutTimestamp'] = currentTimestamp
			self.hallucinationId = AbilityId.HALLUCINATION_PHOENIX

		return self.hallucinationId is not None

	def perform(self, gameObject, agent, firstAction):
		unit = agent.getUnit(gameObject)
		gameObject.do(unit(self.hallucinationId))
