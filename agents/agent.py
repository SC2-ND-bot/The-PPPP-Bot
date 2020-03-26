from FSM.state_machine import StateMachine
from FSM.states import AgentStates

# TODO for @Hermes: create loadActions, DataProvider
# TODO: figure out communication between game, FSM, and actions

class Agent:

	def __init__(self, unitTag=None, planner=None):
		self.unitTag = unitTag
		self.stateMachine = StateMachine()
		self.planner = planner

		self.availableActions = []
		self.currentActions = []

		self.stateMachine.add_state("IDLE_STATE", self.idleStateHandler)
		self.stateMachine.add_state("PERFORM_ACTIONS_STATE", self.performActionsStateHandler)
		self.stateMachine.add_state("END_STATE", self.endStateHandler, True)

		self.stateMachine.set_start("IDLE_STATE")

		# TODO: Create DataProvider which feeds the agents goals and state information
		# self.dataProvider = DataProvider()

	def getUnit(self, gameObject):
		return gameObject.units.by_tag(self.unitTag)

	def hasValidPlan(self):
		raise NotImplementedError

	def idleStateHandler(self, gameObject):
		print('in idle state')

		# agent, actions, gameObject
		plan = self.planner.plan(self, self.availableActions, gameObject)

		if plan is not None:
			self.currentActions = plan
			return "PERFORM_ACTIONS_STATE"
		else:
			print('No valid plan found, agent will remain idle')
			return "IDLE_STATE"

	def performActionsStateHandler(self, gameObject):
		print('in perform actions state')
		if not self.hasValidPlan(gameObject):
			return "IDLE_STATE"

		success = False
		try:
			for index, action in enumerate(self.currentActions):
				action.perform(gameObject, self.getUnit(gameObject), index == 0)
			success = True
		except:
			print('Failed to queue up actions')

		if not success:
			print('Queuing Actions failed, going back to idle state')
			return "IDLE_STATE"

		return "PERFORM_ACTIONS_STATE"

	def loadActions(self):
		raise NotImplementedError

	# # Still unsure if we require this state and handler
	def endStateHandler(self, gameObject):
		print('reached end state')
