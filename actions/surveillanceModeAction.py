from actions.action import Action
from sc2.ids.ability_id import AbilityId

import time
import math

class SurveillanceModeAction(Action):
	def __init__(self):
		super().__init__()
		self.cost = 1
		self.abilityId = AbilityId.MORPH_SURVEILLANCEMODE
		self.effects["attacking"] = False
		self.effects["surveillance"] = True

	def __repr__(self):
		return "Create Surveillance Mode Action Class"

	def reset(self):
		return

	def checkProceduralPrecondition(self, gameObject, agent):
		unit = agent.getUnit(gameObject)
		
		if unit.distance_to(gameObject.enemy_start_locations[0]) > 3.0:
			return False

		return self.abilityId in agent.available_abilities


	def perform(self, gameObject, agent, firstAction):
		unit = agent.getUnit(gameObject)
		gameObject.do(unit(self.abilityId))