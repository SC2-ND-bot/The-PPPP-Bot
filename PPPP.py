import random

import sc2
from sc2 import Race, Difficulty
import math
from sc2.constants import *
from sc2.player import Bot, Computer
from sc2.position import Point2, Point3

class PPPP(sc2.BotAI):
    def __init__(self):
        self.path_coord_dict = {}
        self.working_locations = {}

    async def on_step(self, iteration):
        if iteration == 0:
            await self.chat_send("(probe)(pylon)(cannon)(cannon)(gg)")
            await self.build_coord_dict()
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

        nexuses = self.structures(NEXUS)
        
        ################# This is the logic relevant for milestone 1 #################
        
        for worker in self.workers:
            if worker.is_idle:
                print("calling go to work")
                self.go_to_work(worker)

        ######################################################################################################

        # If we have no pylon, build one near starting nexus
        if len(self.structures(PYLON)) < 1 and self.already_pending(PYLON) == 0:
            if self.can_afford(PYLON):
                await self.build(PYLON, near=self.main_base_ramp.protoss_wall_pylon)

        # Make probes until we have 16 in each base
        for nexus in nexuses:
            if self.supply_workers < 22 and nexus.is_idle:
                if self.can_afford(PROBE):
                    self.do(nexus.train(PROBE), subtract_cost=True, subtract_supply=True)

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
        print("inside go to work")
        x_coord = math.floor(worker.position.x)
        y_coord = math.floor(worker.position.y)
        worker_coords = (x_coord, y_coord)

        working_location = self.bfs(worker_coords)
        print("working location: ", working_location)
        if (working_location is not None):
            print("working_location in self.structures(NEXUS): ", self.working_locations[working_location] in self.structures(NEXUS))
            if (self.working_locations[working_location] in self.structures(NEXUS)):
                # print("self.mineral_field: ", self.mineral_field)
                for mineral in self.mineral_field:
                    if mineral.distance_to(working_location) <= 8:
                        print("found minerals close to Nexus")
                        self.do(worker.gather(mineral))
                        break
            else:
                self.do(worker.gather(self.working_locations[working_location]))
        else:
            print("working location is None")
            
    def bfs(self, root):
        visited = [root]
        queue = [root]
        while queue:
            node = queue.pop(0)
            for neighbor in self.path_coord_dict[node]:
                if neighbor not in visited:
                    if self.working_locations.get(neighbor) is not None:
                        resource = self.working_locations[neighbor]
                        is_not_full = (resource.ideal_harvesters - resource.assigned_harvesters) > 0
                        is_not_empty = True

                        if resource.is_mineral_field:
                            is_not_empty = resource.mineral_contents > 0
                        elif resource.is_vespene_geyser:
                            is_not_empty = resource.vespene_contents > 0
                        if True:
                            return neighbor
                        
                    visited.append(neighbor)
                    queue.append(neighbor)

def main():
    sc2.run_game(
        sc2.maps.get("AcropolisLE"),
        [Bot(Race.Protoss, PPPP(), name="CheeseCannon"), Computer(Race.Protoss, Difficulty.VeryEasy)],
        realtime=True,
    )


if __name__ == "__main__":
    main()
