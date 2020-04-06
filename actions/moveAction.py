from actions.action import Action

class MoveAction(Action):
	def __init__(self, agent, destination):
		super().__init__(agent)

		self.agent = agent
		self.gameObject = agent.gameObject
		self.cost = 1
		self.destination = destination

		# self.preconditions["attackingArea"] = False
		self.effects["position"] = True
		self.effects["movingTowardsDestination"] = True

	def __repr__(self):
		return "Move Action Class"

	# def calcCost(self):
	#	# determine the cost for this action
	#	# will be used during planning

	def reset(self):
		self.destination = None

	def checkProceduralPrecondition(self, agent):
		# This should generate a valid attackLocation
		attackLocation = self.gameObject.enemy_start_locations[0]
		self.destination = attackLocation
		return True

	def perform(self): #firstAction
		self.gameObject.do(self.agent.unit.move(self.destination))
		
	def isDone(self):
		if self.agent.unit.distance_to_squared(self.attackLocation) <= self.agent.unit.detect_range: #unit.sight_range
			return True
		return False
		
	def updateWorldState(self, gameObject, destination):
		self.gameObject = gameObject
		self.destination = destination
		self.gameObject.do(self.agent.unit.move(self.attackLocation))
