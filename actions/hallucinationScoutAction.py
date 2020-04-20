from actions.action import Action

class HallucinationScoutAction(Action):
	def __init__(self):
		super().__init__()
		self.cost = 2.0
		self.scoutLocations = None

		self.effects["scouting"] = True

	def __repr__(self):
		return "Hallucination Action Class"

	def reset(self):
		self.scoutLocations = None

	def checkProceduralPrecondition(self, gameObject, agent):
		unit = agent.getUnit(gameObject)

		if not unit.is_hallucination:
			return False

		self.scoutLocations = [gameObject.enemy_start_locations[0]]

		return self.scoutLocations is not None

	def perform(self, gameObject, agent, firstAction):
		unit = agent.getUnit(gameObject)
		for index, location in enumerate(self.scoutLocations):
			gameObject.do(unit.move(location, index != 0))
