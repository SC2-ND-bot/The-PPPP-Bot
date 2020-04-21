from agents.agent import Agent
from actions.findEnemyAction import FindEnemyAction
from actions.attackEnemyAction import AttackEnemyAction
from actions.retreatAction import RetreatAction

class InterceptorAgent(Agent):
	def __init__(self, unitTag=None, planner=None):
		super().__init__(unitTag, planner)
		self.last_shield_health_percentage = 1.0
		self.state = {
			"canAttack": True,
			"attacking": False,
			"underAttack": False,
			"health_critical": False,
			"retreating": False
		}

		self.availableActions.append(FindEnemyAction())
		self.availableActions.append(AttackEnemyAction())
		self.availableActions.append(RetreatAction())

	def isPlanInvalid(self, gameObject):
		# Add additional checks that should abort plan, like is_under_attack
		unit = self.getUnit(gameObject)
		return self.state["health_critical"] and not self.state["retreating"]

	# Requires further changes, not working right now
	def is_under_attack(self, gameObject):
		unit = self.getUnit(gameObject)
		if self.last_shield_health_percentage < unit.shield_health_percentage:
			self.last_shield_health_percentage = unit.shield_health_percentage
			return True
		return False
