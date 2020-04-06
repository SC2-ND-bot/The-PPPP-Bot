class GoapPlanner:
	def __init__(self):
		print('planner was created')
		# TODO: add needed variables, etc.

	# Plan what sequence of actions can fulfill the goal.
	# Returns null if a plan could not be found, or a list of the actions that must be performed, in order, to fulfill the goal.
	def plan(self, agent, actions, gameObject):

		usableActions = []
		for action in actions:
			# reset the actions so we can start fresh with them
			action.doReset()
			# check what actions can run using their checkProceduralPrecondition
			if action.checkProceduralPrecondition(gameObject, agent):
				usableActions.append(action)

		# we now have all actions that can run, stored in usableActions

		#build up the tree and record the leaf nodes that provide a solution to the goal.
		leaves = []
		root = self.Node(None, 0, agent.state, None)
		if not self.buildGraph(root, leaves, usableActions, gameObject.goal):
			print("No available plan")
			return

		# get the cheapest leaf node
		cheapest_node = None
		for leaf in leaves:
			if cheapest_node is None:
				cheapest_node = leaf
			else:
				if leaf.cost < cheapest_node.cost:
					cheapest_node = leaf

		# get its node and work back through the parents
		result = []
		node = cheapest_node
		while node is not None:
			if node.action is not None:
				result.append(node.action)
			node = node.parent

		# we now have this action list in correct order

		queue = []
		for action in result:
			queue.append(action)
		#print("returning action queue: ", queue)
		return queue

	class Node:
		def __init__(self, parent, cost, state, action):
			self.parent = parent
			self.cost = cost
			self.state = state
			self.action = action

	# Returns true if at least one solution was found.
	# The possible paths are stored in the leaves list. Each leaf has a 'runningCost' value where the lowest cost will be the best action sequence.
	def buildGraph(self, parent, leaves, actions, goal):
		found = False

		# go through each action available at this node and see if we can use it here
		for action in actions:
			# if the parent state has the conditions for this action's preconditions, we can use it here
			if self.areActionConditionsMet(action.preconditions, parent.state):
				# apply the action's effects to the parent state
				stateAfterAction = self.populateState(parent.state, action.effects)
				node = self.Node(parent, parent.cost + action.cost, stateAfterAction, action)
				if self.isGoalMet(goal, stateAfterAction):
					leaves.append(node)
					found = True
				else:
					subset = self.actionSubset(actions, action)
					if self.buildGraph(node, leaves, subset, goal):
						found = True
		return found

	# Check that all items in 'conditions' are in 'state'.
	# If just one does not match or is not there then this returns false.
	def areActionConditionsMet(self, conditions, state):
		for condition in conditions:
			stateValue = state.get(condition, None)
			if stateValue is None:
				return False
			elif conditions[condition] is not stateValue:
				return False
		return True

	def isGoalMet(self, goal, state):
		stateValue = state.get(goal[0], None)
		if stateValue is None:
			return False
		if goal[1] is not stateValue:
			return False
		return True

	# Apply the actionEffects to the currentState
	def populateState(self, currentState, actionEffects):
		return { **currentState, **actionEffects }

	# Create a subset of the actions excluding removedAction. Creates a new set.
	def actionSubset(self, actions, removedAction):
		subset = []
		for action in actions:
			if action != removedAction:
				subset.append(action)
		return subset
