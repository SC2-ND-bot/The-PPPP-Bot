import random
import math
import sc2
from buildOrder import buildtreeNode
from buildOrder import buildOrder
from sc2 import Race, Difficulty
from sc2.constants import *
from sc2.player import Bot, Computer
from sc2.position import Point2, Point3
from sc2.ids.unit_typeid import UnitTypeId
from state_machine import StateMachine
from agents.probe import ProbeAgent

class PPPP(sc2.BotAI):
    def __init__(self):
        self.path_coord_dict = {}
        self.working_locations = {}
        self.agents = []

    def create_agent(self, unit):
        if unit.type_id == PROBE:
            newProbeAgent = ProbeAgent(unit)
            self.agents.append(newProbeAgent)


    async def on_step(self, iteration):
        if iteration == 0:
            # await self.chat_send("(probe)(pylon)(cannon)(cannon)(gg)")
            await self.build_coord_dict()
            self.buildTree = buildOrder(self.game_data)
        
        bases = self.townhalls.ready
        gas_buildings = self.gas_buildings.ready
        
        for resource in bases | gas_buildings:
            x_coord = math.floor(resource.position.x)
            y_coord = math.floor(resource.position.y)
            self.working_locations[(x_coord, y_coord)] = resource

        # if not self.townhalls:
        #     # Attack with all workers if we don't have any nexuses left, attack-move on enemy spawn (doesn't work on 4 player map) so that probes auto attack on the way
        #     for worker in self.workers:
        #         self.do(worker.attack(self.enemy_start_locations[0]))
        #     return

        nexuses = self.structures(NEXUS)
        
        # Logic for returning idle workers to work (Milestone 1)
        for worker in self.workers:
            if worker.is_idle:
                self.go_to_work(worker)

        ######################################################################################################

        # # If we have no pylon, build one near starting nexus
        # if len(self.structures(PYLON)) < 1 and self.already_pending(PYLON) == 0:
        #     if self.can_afford(PYLON):
        #         await self.build(PYLON, near=self.main_base_ramp.protoss_wall_pylon)

        # # Make probes until we have 16 in each base
        # for nexus in nexuses:
        #     if self.supply_workers < 19 and nexus.is_idle:
        #         if self.can_afford(PROBE):
        #             self.do(nexus.train(PROBE), subtract_cost=True, subtract_supply=True)
        
        # if self.supply_workers == 19 and len(self.structures(PYLON)) < 3 and self.already_pending(PYLON) == 0:
        #     if self.can_afford(PYLON):
        #         await self.build(PYLON, near=self.main_base_ramp.protoss_wall_pylon)

        # Logic for execution of build tree (Milestone 2)
        inst = self.buildTree.stepDown(self.minerals, self.vespene, self.supply_left, self.state)
        print(inst)
        if inst != None:
            if inst[1] == 0: # A unit
                if inst[0] == UnitTypeId.PROBE:
                    nexus = random.choice(nexuses)
                    if self.do(nexus.train(PROBE), subtract_cost=True, subtract_supply=True):
                        self.buildTree.curr.executed = True
                else:    
                    if self.train(inst[0]):
                        self.buildTree.curr.executed = True
            elif inst[1] == 1: # A building
                map_center = self.game_info.map_center
                position_towards_map_center = self.start_location.towards(map_center, distance=random.randint(0, 15))
                if await self.build(inst[0], near=position_towards_map_center, placement_step=1):
                    self.buildTree.curr.executed = True
            elif inst[1] == -1: # Research
                if self.research(self.nodeContents):
                    self.buildTree.curr.executed = True

        self.start_location

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
        else:
            print("could not find location")


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
                        #     return working_location
                        return working_location
                        
                    visited.append(neighbor)
                    queue.append(neighbor)
        return None

def main():
    sc2.run_game(
        sc2.maps.get("AcropolisLE"),
        [Bot(Race.Protoss, PPPP(), name="CheeseCannon"), Computer(Race.Protoss, Difficulty.VeryEasy)],
        realtime=False,
    )

if __name__ == "__main__":
    main()
