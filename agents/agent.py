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
		self.plannedActions = []
		self.currentAction = None
		self.state = {}

		self.stateMachine.add_state("IDLE_STATE", self.idleStateHandler)
		self.stateMachine.add_state("PERFORM_ACTIONS_STATE", self.performActionsStateHandler)
		self.stateMachine.add_state("END_STATE", self.endStateHandler, True)

		self.stateMachine.set_start("IDLE_STATE")

		# TODO: Create DataProvider which feeds the agents goals and state information
		# self.dataProvider = DataProvider()

	def getUnit(self, gameObject):
		return gameObject.units.by_tag(self.unitTag)

	def isPlanInvalid(self):
		raise NotImplementedError

	def idleStateHandler(self, gameObject):
		print("\n\n",self.unitTag)
		print('in idle state')
		print('state at the start of idle: ', self.state)

		# agent, actions, gameObject
		plan = self.planner.plan(self, self.availableActions, gameObject)
		print("plan: ", plan)
		if plan is not None:
			print("plan is not None")

			self.plannedActions = plan
			return "PERFORM_ACTIONS_STATE"
		else:
			print('No valid plan found, agent will remain idle')
			return "IDLE_STATE"

	def performActionsStateHandler(self, gameObject):
		print("\n\n",self.unitTag)
		print('in perform actions state')
		if self.isPlanInvalid(gameObject):
			return "IDLE_STATE"

		if self.currentAction is None:
			self.currentAction = self.plannedActions.pop()

		print("state before queuing actions: ", self.state)
		print("planned Actions: ", self.plannedActions)
		self.currentAction.reset()
		print("checking: ", self.currentAction)
		if not self.currentAction.checkProceduralPrecondition(gameObject, self):
			self.state = { **self.state, **self.currentAction.effects }
			if len(self.plannedActions) == 0:
				print('preconditions failed, plan is empty. Going back to idle state')
				return "IDLE_STATE"
			else:
				self.currentAction = self.plannedActions.pop()
				print('preconditions failed, new current action: ', self.currentAction)
		print("performing: ", self.currentAction)
		self.currentAction.perform(gameObject, self.getUnit(gameObject), True)
		# for index, action in enumerate(self.plannedActions):
			# 	print('performing action: ', action)
			# 	print('first action?: ', index==0)
			# 	action.perform(gameObject, self.getUnit(gameObject), index == 0)
		# 	# Update agent state to reflect actions
		# 	# print("state after queuing actions: ", self.state)
		# except Exception:
		# 	print('Failed to perfrom action: ', Exception)

		return "PERFORM_ACTIONS_STATE"

	def loadActions(self):
		raise NotImplementedError

	# # Still unsure if we require this state and handler
	def endStateHandler(self, gameObject):
		print('reached end state')
