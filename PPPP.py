import random

import sc2
from sc2 import Race, Difficulty
import math
# from sc2.ids.unit_typeid import UnitTypeId
from sc2.constants import *
from sc2.player import Bot, Computer
from sc2.position import Point2, Point3
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
            await self.chat_send("(probe)(pylon)(cannon)(cannon)(gg)")
            await self.build_coord_dict()
            for unit in self.units:
                await create_agent(unit)

        bases = self.townhalls.ready
        gas_buildings = self.gas_buildings.ready
        
        for resource in bases | gas_buildings:
            x_coord = math.floor(resource.position.x)
            y_coord = math.floor(resource.position.y)
            self.working_locations[(x_coord, y_coord)] = resource

        if not self.townhalls:
            # Attack with all workers if we don't have any nexuses left, attack-move on enemy spawn (doesn't work on 4 player map) so that probes auto attack on the way
            for worker in self.workers:
                self.do(worker.attack(self.enemy_start_locations[0]))
            return
        
        ################# This is the logic relevant for milestone 1 #################
        
        for worker in self.workers:
            if worker.is_idle:
                self.go_to_work(worker)

        ######################################################################################################

        # If we have no pylon, build one at main base ramp
        if len(self.structures(PYLON)) < 1 and self.already_pending(PYLON) == 0:
            if self.can_afford(PYLON):
                await self.build(PYLON, near=self.main_base_ramp.protoss_wall_pylon)

        # Make probes until we have 16 in each base
        for nexus in self.structures(NEXUS):
            if nexus.surplus_harversters > 0:
                
            # Train probe on nexuses that are undersaturated (avoiding distribute workers functions)
            # if nexus.assigned_harvesters < nexus.ideal_harvesters and nexus.is_idle:
            if self.supply_workers + self.already_pending(PROBE) < self.townhalls.amount * 22 and nexus.is_idle:
                if self.can_afford(PROBE):
                    self.do(nexus.train(PROBE), subtract_cost=True, subtract_supply=True)

        # If we have less than 3 nexuses and none pending yet, expand
        if self.townhalls.ready.amount + self.already_pending(NEXUS) < 3:
            if self.can_afford(NEXUS):
                await self.expand_now()

        if self.supply_left < 3 and self.already_pending(PYLON) == 0:
            if self.can_afford(PYLON):
                print("trying to build pylon")
                await self.build(PYLON, near=self.start_location)


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
