from agents.agent import Agent
from actions.attackMoveAction import AttackMoveAction

class AdeptAgent(Agent):
	def __init__(self, unit=None, gameObject=None, planner=None):
		super().__init__()
		self.unit = unit
		self.last_shield_health_percentage = 1.0
		self.gameObject = gameObject
		self.planner = planner
		self.availableActions.append(AttackMoveAction(self, self.gameObject))

	def hasValidPlan(self):
		# Add additional checks that should abort plan, like is_under_attack
		return self.unit.is_idle

	# Requires further changes
	def is_under_attack(self):
		if self.last_shield_health_percentage < self.unit.shield_health_percentage:
			self.last_shield_health_percentage = self.unit.shield_health_percentage
			return True
		return False
