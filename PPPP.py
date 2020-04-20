import random
import math
import time

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

from agents.agent import Agent
from agents.adeptAgent import AdeptAgent
from agents.zealotAgent import ZealotAgent
from agents.sentryAgent import SentryAgent
from agents.phoenixAgent import PhoenixAgent
from agents.immortalAgent import ImmortalAgent
from agents.stalkerAgent import StalkerAgent

from FSM.state_machine import StateMachine
from goapPlanner import GoapPlanner

from sc2.data import Alert

planner = GoapPlanner()

class PPPP(sc2.BotAI):
	def __init__(self):
		self.path_coord_dict = {}
		self.working_locations = {}
		self.agents = {}
		self.goalTriggers = {
			"lastTimeScouting": time.time()
		}
		self.nexus_construct_time = 0

	async def on_upgrade_complete(self, upgrade_id):
		print("upgrade completed")
		for unit in self.units:
			print('switching goal to attacking')
			self.getAgent(unit).goal = ('attacking', True)

	async def on_unit_created(self, unit):
		if unit.type_id == ADEPT:
			print('made adept agent')
			self.agents[unit.tag] = AdeptAgent(unit.tag, planner)
		elif unit.type_id == ZEALOT:
			print('made zealot agent')
			self.agents[unit.tag] = ZealotAgent(unit.tag, planner)
		elif unit.type_id == SENTRY:
			print('made sentry agent')
			self.agents[unit.tag] = SentryAgent(unit.tag, planner)
		elif unit.type_id == IMMORTAL:
			print('made immortal agent')
			self.agents[unit.tag] = ImmortalAgent(unit.tag, planner)
		elif unit.type_id == PHOENIX:
			print('made phoenix agent')
			self.agents[unit.tag] = PhoenixAgent(unit.tag, planner)
		elif unit.type_id == STALKER:
			print('made stalker agent')
			self.agents[unit.tag] = StalkerAgent(unit.tag, planner)
		else:
			print('made default agent')
			self.agents[unit.tag] = ZealotAgent(unit.tag, planner)

	def getAgent(self, unit):
		try:
			return self.agents[unit.tag]
		except:
			print('unable to get unit: ', unit)
			return

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

		# Manages agents

		army_units = self.units.filter(lambda unit: unit.type_id != PROBE)
		for unit in army_units:
			if unit.health_percentage < 0.50 and unit.shield_percentage < 0.75:
				self.getAgent(unit).goal = ('retreating', True)
				print('switching goal to retreating')
			elif unit.type_id == ADEPT:
				if self.units(ADEPT).amount > 2:
					print('switching goal to attacking')
					self.getAgent(unit).goal = ('attacking', True)
			elif unit.type_id == SENTRY and unit.energy > 75:
				if time.time() - self.goalTriggers["lastTimeScouting"] > 45:
					print('switching goal to hallucinationCreated')
					self.getAgent(unit).goal = ('hallucinationCreated', True)
					self.goalTriggers['lastTimeScouting'] = time.time()
			elif unit.type_id == PHOENIX and unit.is_hallucination:
				print('switching goal to scouting')
				self.getAgent(unit).goal = ('scouting', True)
			print("unit: ", unit)
			print("goal: ", self.getAgent(unit).goal)
			self.getAgent(unit).stateMachine.run_step(self)

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
				if worker is not None:
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

	def resetAssignments(self):
		for goal in self.unitAssignments:
			self.unitAssignments[goal] = 0

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
		[Bot(Race.Protoss, PPPP(), name="The PPPP"), Computer(Race.Zerg, Difficulty.Easy)],
		realtime=False,
	)

if __name__ == "__main__":
	main()
