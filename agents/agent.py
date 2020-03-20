from FSM.state_machine import StateMachine
from FSM.states import AgentStates

# TODO for @Hermes: create loadActions, DataProvider
# TODO: figure out communication between game, FSM, and actions

class Agent:

	def __init__(self):
		self.unit = None
		self.worldState = {}
		self.stateMachine = StateMachine()
		self.planner = None

		self.availableActions = []
		self.currentActions = []

		self.stateMachine.add_state("IDLE_STATE", self.idleStateHandler)
		self.stateMachine.add_state("PERFORM_ACTIONS_STATE", self.performActionsStateHandler)
		self.stateMachine.add_state("END_STATE", self.endStateHandler, True)

		self.stateMachine.set_start("IDLE_STATE")

		# TODO: Create DataProvider which feeds the agents goals and state information
		# self.dataProvider = DataProvider()

	def hasValidPlan(self):
		raise NotImplementedError

	def idleStateHandler(self, gameObject):
		print('in idle state')
		# goal = self.dataProvider.getGoal()
		goal = ('movingTowardsEnemy', True)

		# TODO: Should return all relevant world information
		# worldState = self.dataProvider.getWorldState()
		worldState = None

		# agent, actions, state, goal
		plan = self.planner.plan(self, self.availableActions, self.worldState, goal)

		if plan is not None:
			self.currentActions = plan
			return "PERFORM_ACTIONS_STATE"
		else:
			print('No valid plan found, agent will remain idle')
			return "IDLE_STATE"

	def performActionsStateHandler(self, gameObject):
		print('in perform actions state')
		if not self.hasValidPlan():
			return "IDLE_STATE"

		success = False
		if self.hasValidPlan():
			for index, action in enumerate(self.currentActions):
				firstAction = index == 0
				action.perform(firstAction)
			success = True

			if not success:
				print('Queuing Actions failed, going back to idle state')
				return "IDLE_STATE"

			return "PERFORM_ACTIONS_STATE"

	def loadActions(self):
		raise NotImplementedError

	# # Still unsure if we require this state and handler
	def endStateHandler(self):
		print('reached end state')
