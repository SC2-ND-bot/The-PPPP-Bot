from actions.action import Action
from sc2.ids.ability_id import AbilityId
from sc2.ids.unit_typeid import UnitTypeId

import time
import math

class CreateScoutingHallucinationAction(Action):
	def __init__(self):
		super().__init__()
		self.cost = 2
		self.abilityId = AbilityId.HALLUCINATION_PHOENIX
		self.effects["attacking"] = False
		self.effects["defendBase"] = False
		self.effects["hallucinationCreated"] = True

	def __repr__(self):
		return "Create Scouting Hallucination Action Class"

	def reset(self):
		return

	def checkProceduralPrecondition(self, gameObject, agent):
		#unit = agent.getUnit(gameObject)

		return self.abilityId in agent.available_abilities


	def perform(self, gameObject, agent, firstAction):
		unit = agent.getUnit(gameObject)
		gameObject.do(unit(self.abilityId))
