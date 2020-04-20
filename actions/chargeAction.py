from actions.action import Action
from sc2.ids.ability_id import AbilityId

class ChargeAction(Action):
	def __init__(self):
		super().__init__()
		self.cost = 0.75
		self.target = None
		self.abilityId = AbilityId.EFFECT_CHARGE
		self.effects["attacking"] = True
		self.effects["retreating"] = False

	def __repr__(self):
		return "Charge Ability Action Class"

	def reset(self):
		self.target = None

	def checkProceduralPrecondition(self, gameObject, agent):
		unit = agent.getUnit(gameObject)
		
		if self.abilityId not in agent.available_abilities:
			return False
		
		enemies = gameObject.enemy_units()
		enemies_unit_can_attack = enemies.in_attack_range_of(unit, 3.9)

		enemy_to_attack = None
		for enemy in enemies_unit_can_attack:
			if enemy_to_attack is None:
				enemy_to_attack = enemy
			else:
				if enemy_to_attack.shield_health_percentage > enemy.shield_health_percentage:
					enemy_to_attack = enemy

		self.target = enemy_to_attack

		return self.target is not None

	def perform(self, gameObject, agent, firstAction):
		unit = agent.getUnit(gameObject)
		gameObject.do(unit(self.abilityId, self.target))