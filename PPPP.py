import random
import math
import sc2
from buildOrder import buildtreeNode
from buildOrder import buildOrder
from lateGameFSM import lateGameFSM
from sc2 import Race, Difficulty
from sc2.constants import *
from sc2.player import Bot, Computer
from sc2.position import Point2, Point3

from buildOrder import buildOrder
from buildOrder import buildtreeNode

from agents.adeptAgent import AdeptAgent
from agents.sentryAgent import SentryAgent

from FSM.state_machine import StateMachine
from goapPlanner import GoapPlanner

planner = GoapPlanner()

class PPPP(sc2.BotAI):
	def __init__(self):
		self.path_coord_dict = {}
		self.working_locations = {}
		self.agents = {}
		self.worldState = {}
		self.nexus_construct_time = 0
		self.goal = ('attacking', True)

	async def create_agent(self, unit):
		if unit.type_id == ADEPT:
			print('made adept agent')
			self.agents[unit.tag] = AdeptAgent(unit.tag, planner)

	async def on_step(self, iteration):
		if iteration == 0:
			await self.chat_send("(probe)(pylon)(cannon)(cannon)(gg)")
			await self.build_coord_dict()
			self.buildTree = buildOrder(self.game_data, self.enemy_race)
			self.lateGameBuild = lateGameFSM(self.enemy_race)
		bases = self.townhalls.ready
		gas_buildings = self.gas_buildings.ready
		for resource in bases | gas_buildings:
			x_coord = math.floor(resource.position.x)
			y_coord = math.floor(resource.position.y)
			self.working_locations[(x_coord, y_coord)] = resource

		# Logic for returning idle workers to work (Milestone 1)
		for worker in self.workers:
			if worker.is_idle:
				self.go_to_work(worker)
		#####################################################################################################

		# Creates and Manages agents
		for unit in self.units(ADEPT).ready:
			if not self.agents.get(unit.tag, False):
				print('trying to create unit')
				print(unit.type_id)
				self.create_agent(unit)
			else:
				self.agents[unit.tag].stateMachine.run_step(self)

		######################################################################################################

		# Logic for execution of build tree (Milestone 2)
		map_center = self.game_info.map_center
		position_towards_map_center = self.start_location.towards(map_center, distance=random.randint(0, 15))
		if self.time < 450:
			inst = self.buildTree.stepDown(self.minerals, self.vespene, self.supply_left, self.state)
			if inst != None:
				if inst[1] == 0: # A unit
					if inst[0] == UnitTypeId.PROBE:
						nexus = random.choice(self.townhalls)
						if self.do(nexus.train(PROBE), subtract_cost=True, subtract_supply=True):
							self.buildTree.curr.executed = True
					else:
						if self.train(inst[0]):
							self.buildTree.curr.executed = True
				elif inst[1] == 1: # A building
					if self.tech_requirement_progress(inst[0]) >= 1:
						if await self.build(inst[0], near=position_towards_map_center, placement_step=1):
							self.buildTree.curr.executed = True
				elif inst[1] == -1: # Research
					if self.research(inst[0]):
						self.buildTree.curr.executed = True

		# Logic for execution of late-game build FSM (Milestone 4)
		if self.time > 450:
			toBuild = self.lateGameBuild.getInstructions(self.structures, self.enemy_units, self.enemy_structures)
			for inst in toBuild:
				if inst[0] != UnitTypeId(0) and self.already_pending(inst[0]) == 0:
					if inst[1] == "building":
						await self.build(inst[0], near=position_towards_map_center, placement_step=1)
					elif inst[1] == "unit":
						self.train(inst[0])

		# Logic for execution of economy FSM (Milestone 3)
		if self.supply_left <= 3 and self.already_pending(UnitTypeId.PYLON) == 0:
			await self.build(UnitTypeId.PYLON, near=position_towards_map_center, placement_step=1)
		if self.supply_workers < len(self.townhalls) * 25 and self.supply_left > 5 and self.already_pending(UnitTypeId.PROBE) == 0:
			nexus = random.choice(self.townhalls)
			self.do(nexus.train(UnitTypeId.PROBE), subtract_cost=True, subtract_supply=True)
		for ass in self.gas_buildings:
			if (ass.assigned_harvesters < 1 or (ass.assigned_harvesters < 3 and self.time > 180)) and self.already_pending(UnitTypeId.ASSIMILATOR) == 0 and self.already_pending(UnitTypeId.NEXUS) == 0:
				worker = self.select_build_worker(position_towards_map_center)
				self.do(worker.gather(ass))
		for nexus in self.townhalls:
			geysers = self.vespene_geyser.closer_than(15, nexus)
			for geyser in geysers:
				if not self.gas_buildings.closer_than(1, geyser):
					if not self.can_afford(UnitTypeId.ASSIMILATOR):
						break
					worker = self.select_build_worker(geyser.position)
					if worker is None:
						break
					if not self.gas_buildings or not self.gas_buildings.closer_than(1, geyser):
						self.do(worker.build(UnitTypeId.ASSIMILATOR, geyser), subtract_cost=True)
						self.do(worker.stop(queue=True))
						await self.distribute_workers()
		if self.time > self.nexus_construct_time + 180 and len(self.townhalls) < 4:
			exp = await self.get_next_expansion()
			await self.build(UnitTypeId.NEXUS, exp)
			self.nexus_construct_time = self.time
			await self.distribute_workers()

	async def build_coord_dict(self):
		path_matrix = self.game_info.pathing_grid.data_numpy
		mheight = len(path_matrix)
		mwidth = len(path_matrix[1])
		for i in range(0, mheight):
			for j in range(0, mwidth):
				if path_matrix[i,j] == 1:
					neighbors = lambda i, j: [(x,y) for x in range(i-1, i+2) for y in range(j-1, j+2) if (-1 < i <= mheight and -1 < j <= mwidth and (i != x or j != y) and (0 <= x <= mheight) and (0 <= y <= mwidth))]
					self.path_coord_dict.setdefault((i,j), [])
					for z in neighbors(i,j):
						if path_matrix[z] == 1:
							self.path_coord_dict[(i,j)].append(z)
		print("build_coord_dict() FINISHED!")

	async def build_worldState_dict(self):
		self.worldState['minerals'] = self.minerals # Resources
		self.worldState['vespene'] = self.vespene
		self.worldState['warp_gate_count'] = self.warp_gate_count
		self.worldState['army_count'] = self.army_count
		self.worldState['workers'] = self.workers
		self.worldState['townhalls'] = self.townhalls # Your townhalls (nexus, hatchery, etc.)
		self.worldState['gas_buildings'] = self.gas_buildings # Your gas structures (refinery, extractor, etc.)
		self.worldState['units'] = self.units # Your units (includes larva and workers)
		self.worldState['structures'] = self.structures # Your structures (includes townhalls and gas buildings)
		self.worldState['start_location'] = self.start_location # Your spawn location (your first townhall location)
		self.worldState['main_base_ramp'] = self.main_base_ramp # Location of your main base ramp
		self.worldState['enemy_units'] = self.enemy_units # The following contains enemy units and structures inside your units' vision range
		self.worldState['enemy_structures'] = self.enemy_structures
		self.worldState['enemy_start_location'] = self.enemy_start_location # Enemy spawn locations as a list of Point2 points
		self.worldState['blips'] = self.blips # Enemy units that are inside your sensor tower range
		self.worldState['enemy_race'] = self.enemy_race
		self.worldState['mineral_field'] = self.mineral_field # All mineral fields on the map
		self.worldState['vespene_geyser'] = self.vespene_geyser # All vespene fields, even those that have a gas building on them
		self.worldState['expansion_locations'] = self.expansion_locations # Locations of possible expansions
		self.worldState['destructables'] = self.destructables # All destructable rocks (except the platforms below the main base ramp)


	def go_to_work(self, worker):
		x_coord = math.floor(worker.position.x)
		y_coord = math.floor(worker.position.y)
		worker_coords = (x_coord, y_coord)

		working_location = self.find_working_location(worker_coords)
		if working_location is not None:
			if working_location.type_id == NEXUS:
				for mineral in self.mineral_field:
					if mineral.distance_to(working_location.position) <= 8:
						self.do(worker.gather(mineral))
						break
			else:
				self.do(worker.gather(working_location))

	def find_working_location(self, root):
		visited = [root]
		queue = [root]
		while queue:
			node = queue.pop(0)
			for neighbor in self.path_coord_dict.get(node, []):
				if neighbor not in visited:
					if self.working_locations.get(neighbor) is not None:
						working_location = self.working_locations[neighbor]
						is_not_full = working_location.surplus_harvesters <= 0

						# if is_not_full:
						#	  return working_location
						return working_location

					visited.append(neighbor)
					queue.append(neighbor)
		return None

def main():
	sc2.run_game(
		sc2.maps.get("AcropolisLE"),
		[Bot(Race.Protoss, PPPP(), name="The PPPP"), Computer(Race.Zerg, Difficulty.VeryEasy)],
		realtime=False,
	)

if __name__ == "__main__":
	main()
