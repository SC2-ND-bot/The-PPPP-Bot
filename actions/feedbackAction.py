from actions.action import Action
from sc2.ids.ability_id import AbilityId
from sc2.ids.unit_typeid import UnitTypeId


class FeedbackAction(Action):
	def __init__(self):
		super().__init__()
		self.cost = 2.0
		self.target = None
		self.abilityId = AbilityId.FEEDBACK_FEEDBACK

		self.effects['attacking'] = True

		susceptible_targets = {
			'Protoss': [HIGHTEMPLAR, SENTRY, PHOENIX, ORACLE, MOTHERSHIP, MOTHERSHIPCORE],
			'Terran': [GHOST, THOR, BANSHEE, MEDIVAC, BATTLECRUISER, RAVEN, POINTDEFENSEDRONE],
			'Zerg': [INFESTOR, OVERSEER, QUEEN, VIPER]
			# Random is also possible, but not necessary right now
		}

	def __repr__(self):
		return "Feedback Ability Action Class"

	def reset(self):
		self.cost = 2.0
		self.target = None

	def checkProceduralPrecondition(self, gameObject, agent):
		unit = agent.getUnit(gameObject)

		if self.abilityId not in agent.available_abilities:
			print("Can cast feedback: False")
			return False

		print("Can cast feedback: True")

		enemies = gameObject.enemy_units()
		enemies_in_sight = enemies.closer_than(unit.sight_range, unit.position)

		target = None
		for enemy in enemies_in_sight:
			if enemy in self.susceptible_targets[enemy.race]:
				if unit.in_ability_cast_range(self.abilityId, enemy):
					if target is None:
						target = enemy
						print("Found valid feedback target")
					else:
						if enemy.energy_percentage > target.energy_percentage:
							target = enemy


		self.target = target

		# idea: calculate action cost by calculating most damage against n enemy units
		# would help determine if attack action against 1 enemy unit would be more or less
		# useful than doing AoE ability against 3 enemy units

		return self.target is not None

	def perform(self, gameObject, agent, firstAction):
		unit = agent.getUnit(gameObject)
		gameObject.do(unit(self.abilityId, self.target))
		print("Performing Feedback!")
