from FSM.state_machine import StateMachine
from FSM.states import AgentStates
from actions.findChokePoint import FindChokePoint

class Agent:

	def __init__(self, unitTag=None, planner=None):
		self.unitTag = unitTag
		self.stateMachine = StateMachine()
		self.planner = planner

		self.availableActions = [FindChokePoint()]
		self.plannedActions = []
		self.currentAction = None
		self.state = {}
		self.goal = ('defendBase', True)

		self.stateMachine.add_state("IDLE_STATE", self.idleStateHandler)
		self.stateMachine.add_state("PERFORM_ACTIONS_STATE", self.performActionsStateHandler)
		self.stateMachine.add_state("END_STATE", self.endStateHandler, True)

		self.stateMachine.set_start("IDLE_STATE")

	def getUnit(self, gameObject):
		return gameObject.units.by_tag(self.unitTag)

	def isPlanInvalid(self, gameObject):
		raise NotImplementedError

	def idleStateHandler(self, gameObject):
		plan = self.planner.plan(self, self.availableActions, gameObject)
		if plan is not None:
			self.plannedActions = plan
			return "PERFORM_ACTIONS_STATE"
		else:
			return "IDLE_STATE"

	def performActionsStateHandler(self, gameObject):
		if self.isPlanInvalid(gameObject):
			return "IDLE_STATE"

		if self.currentAction is None:
			self.currentAction = self.plannedActions.pop()

		self.currentAction.reset()
		if not self.currentAction.checkProceduralPrecondition(gameObject, self):
			self.state = { **self.state, **self.currentAction.effects }
			if len(self.plannedActions) == 0:
				return "IDLE_STATE"
			else:
				self.currentAction = self.plannedActions.pop()
		self.currentAction.perform(gameObject, self, True)

		return "PERFORM_ACTIONS_STATE"

	def loadActions(self):
		raise NotImplementedError

	# # Still unsure if we require this state and handler
	def endStateHandler(self, gameObject):
		print('reached end state')
