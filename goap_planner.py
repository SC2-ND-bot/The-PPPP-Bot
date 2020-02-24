class GoapPlanner:
	def __init__(self):
		# TODO: add needed variables, etc.
	
	# Plan what sequence of actions can fulfill the goal.
	# Returns null if a plan could not be found, or a list of the actions that must be performed, in order, to fulfill the goal.
	def plan(agent, actions, state, goal):
		
		# reset the actions so we can start fresh with them
		for action in actions:
			action.doReset()
		
		# check what actions can run using their checkProceduralPrecondition
		usableActions = []
		for action in actions:
			if action.checkProceduralPrecondition(agent):
				usableActions.append(action)
		
		# we now have all actions that can run, stored in usableActions
		
		#build up the tree and record the leaf nodes that provide a solution to the goal.
		leaves = []
		root = self.Node(None, 0, state, None)
		if not self.buildGraph(root, leaves, usableActions, goal):
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
		while n is not None:
			if n.action is not None:
				result.append(n.action)
			n = n.parent
		
		# we now have this action list in correct order
		
		queue = []
		for action in result:
			queue.append(action)
		
		return queue
	
	class Node:
		def __init__(self, parent, cost, state, action):
			self.parent = parent
			self.cost = cost
			self.state = state
			self.action = action
	
	# Returns true if at least one solution was found.
	# The possible paths are stored in the leaves list. Each leaf has a 'runningCost' value where the lowest cost will be the best action sequence.
	def buildGraph(parent, leaves, actions, goal):
		found = False
		
		# go through each action available at this node and see if we can use it here
		for action in actions:
		
			# if the parent state has the conditions for this action's preconditions, we can use it here
			if self.inState(action.Preconditions, parent.state):
				
				# apply the action's effects to the parent state
				currentState = self.populateState(parent.state, action.Effects)
				
				node = self.Node(parent, parent.cost + action.cost, currentState, action)
				
				if self.inState(goal, currentState):
					leaves.append(node)
					found = True
				else:
					subset = self.actionSubset(actions, action)
					if self.buildGraph(node, leaves, subset, goal):
						found = True
		
		return found
	
	# Check that all items in 'conditions' are in 'state'. 
	# If just one does not match or is not there then this returns false.
	def inState(conditions, state):
		allMatch = True
		
		for c in conditions:
			match = False
			for s in state:
				if s == c:
					match = True
					break
			if not match:
				allMatch = False
		
		return allMatch
	
	# Apply the stateChange to the currentState
	def populateState(currentState, stateChange):
		state = {}
		
		for s in currentState:
			state[s.Key] = s.Value
		
		for change in stateChange:
			exists = False
			
			for s in state:
				if state[s] == change:
					exists = True
					break
			
			if exists:
				state.RemoveWhere(#TODO)
				state[change.Key] = change.Value
			else:
				# if it does not exist in the current state, add it
				state[change.Key] = change.Value
		
		return state
	
	
	# Create a subset of the actions excluding removedAction. Creates a new set.
	def actionSubset(actions, removedAction):
		subset = []
		for action in actions:
			if action != removedAction:
				subset.append(action)
		return subset
	