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
		# Add additional checks that should abort plan
		print('start*****************************')
		print(self.unit.position)
		print(self.unit.position[0])
		print(self.unit.position[1])
		print(self.is_under_attack())
		print(self.unit.shield_health_percentage)
		print(self.unit.is_idle)
		return self.unit.is_idle

	def is_under_attack(self):
		print(self.last_shield_health_percentage)
		print(self.unit.shield_health_percentage)
		if self.last_shield_health_percentage < self.unit.shield_health_percentage:
			self.last_shield_health_percentage = self.unit.shield_health_percentage
			return True
		return False
