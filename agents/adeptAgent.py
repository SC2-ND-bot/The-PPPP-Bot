from agents.agent import Agent
from actions.attackMoveAction import AttackMoveAction
from actions.attackEnemyAction import AttackEnemyAction

class AdeptAgent(Agent):
	def __init__(self, unitTag=None, planner=None):
		super().__init__(unitTag, planner)
		self.last_shield_health_percentage = 1.0
		self.availableActions.append(AttackMoveAction())
		self.availableActions.append(AttackEnemyAction())

	def hasValidPlan(self, gameObject):
		# Add additional checks that should abort plan, like is_under_attack
		unit = self.getUnit(gameObject)
		return not unit.is_attacking

	# Requires further changes, not working right now
	def is_under_attack(self, gameObject):
		unit = self.getUnit(gameObject)
		if self.last_shield_health_percentage < unit.shield_health_percentage:
			self.last_shield_health_percentage = unit.shield_health_percentage
			return True
		return False
