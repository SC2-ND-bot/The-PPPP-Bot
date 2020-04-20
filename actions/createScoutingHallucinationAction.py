from actions.action import Action
from sc2.ids.ability_id import AbilityId
from sc2.ids.unit_typeid import UnitTypeId

import time
import math

class CreateScoutingHallucinationAction(Action):
	def __init__(self):
		super().__init__()
		self.cost = 2.0
		self.hallucinationId = None
		self.effects["attacking"] = False
		self.effects["hallucinationCreated"] = True

	def __repr__(self):
		return "Create Scouting Hallucination Action Class"

	def reset(self):
		self.hallucinationId = None

	def checkProceduralPrecondition(self, gameObject, agent):
		unit = agent.getUnit(gameObject)

		if unit.energy < 75 or unit.type_id != UnitTypeId.SENTRY:
			return False

		self.hallucinationId = AbilityId.HALLUCINATION_PHOENIX

		return self.hallucinationId is not None


	def perform(self, gameObject, agent, firstAction):
		unit = agent.getUnit(gameObject)
		gameObject.do(unit(self.hallucinationId))
