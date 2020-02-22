import random
import math
import sc2
from buildOrder import buildtreeNode
from buildOrder import buildOrder
from sc2 import Race, Difficulty
from sc2.constants import *
from sc2.player import Bot, Computer
from sc2.position import Point2, Point3
from FSM.state_machine import StateMachine
from agents.adeptAgent import AdeptAgent

class PPPP(sc2.BotAI):
    def __init__(self):
        self.path_coord_dict = {}
        self.working_locations = {}
        self.agents = {}

    def create_agent(self, unit):
        if unit.type_id == ADEPT:
            print('made adept agent')
            self.agents[unit] = AdeptAgent(unit)

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
        #####################################################################################################

        ######################################################################################################

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

        # Testing for GOAP

        # for unit in self.units(ADEPT).ready:
        #     if not self.agents.get(unit, False):
        #         print('trying to create unit')
        #         print(unit.type_id)
        #         self.create_agent(unit)
        #     else:
        #         self.agents[unit].stateMachine.run_step(self)

        # if self.units(ADEPT).amount < 1:
        #     for gw in self.structures(GATEWAY).ready.idle:
        #         if self.can_afford(ADEPT) and len(self.structures(CYBERNETICSCORE).ready) > 0:
        #             self.do(gw.train(ADEPT), subtract_cost=True, subtract_supply=True)

        # # If we have no pylon, build one at main base ramp
        # if len(self.structures(PYLON)) < 1 and self.already_pending(PYLON) == 0:
        #     worker = self.workers.random_or(None)
        #     if self.can_afford(PYLON) and worker:
        #         self.do(worker.build(UnitTypeId.PYLON,self.main_base_ramp.protoss_wall_pylon))
        
        # for gw in self.structures(GATEWAY).ready.idle:
        #     print('trying to build adept step 1')
        #     if self.can_afford(ADEPT) and len(self.structures(CYBERNETICSCORE).ready) > 0:
        #         print('trying to build adept step 2')
        #         self.do(gw.train(ADEPT), subtract_cost=True, subtract_supply=True)

        # # If we have no pylon, build one at main base ramp
        # if len(self.structures(PYLON)) < 1 and self.already_pending(PYLON) == 0:
        #     worker = self.workers.random_or(None)
        #     if self.can_afford(PYLON) and worker:
        #         self.do(worker.build(UnitTypeId.PYLON,self.main_base_ramp.protoss_wall_pylon))
        
        # # Once we have a pylon completed
        # if self.structures(PYLON).ready:
        #     pylon = self.structures(PYLON).ready.random
        #     if self.structures(GATEWAY).ready:
        #         # If we have gateway completed, build cyber core
        #         if not self.structures(CYBERNETICSCORE):
        #             if self.can_afford(CYBERNETICSCORE) and self.already_pending(CYBERNETICSCORE) == 0:
        #                 cybernetics_wall_location = self.main_base_ramp.protoss_wall_buildings[1]
        #                 await self.build(CYBERNETICSCORE, cybernetics_wall_location)
        #     else:
        #         # If we have no gateway, build gateway
        #         gateway_wall_location = self.main_base_ramp.protoss_wall_buildings[0]
        #         if self.can_afford(GATEWAY) and self.already_pending(GATEWAY) == 0:
        #             await self.build(GATEWAY, gateway_wall_location)


        #  # Build gas near completed nexuses once we have a cybercore (does not need to be completed
        # if self.structures(CYBERNETICSCORE):
        #     for nexus in self.townhalls.ready:
        #         vgs = self.vespene_geyser.closer_than(15, nexus)
        #         for vg in vgs:
        #             if not self.can_afford(ASSIMILATOR):
        #                 break

        #             worker = self.select_build_worker(vg.position)
        #             if worker is None:
        #                 break

        #             if not self.gas_buildings or not self.gas_buildings.closer_than(1, vg):
        #                 self.do(worker.build(ASSIMILATOR, vg), subtract_cost=True)
        #                 self.do(worker.stop(queue=True))
            
            # # TODO: redistribute workers
            # if nexus.surplus_harvesters > 0:
            #     await self.distribute_workers()
                
        #     # TODO: This needs work
        #     if self.supply_workers + self.already_pending(PROBE) < self.townhalls.amount * 22 and nexus.is_idle:
        #         if self.can_afford(PROBE):
        #             self.do(nexus.train(PROBE), subtract_cost=True, subtract_supply=True)

        #     # if self.supply_workers > 16 * self.townhalls.amount() and self.gas_buildings.ready < self.townhalls.amount() * 2:
        #     #     closest_vespene_geysers = enemy_zerglings.closest_n_units(nexus, 2)

        # if self.supply_left < 3 and self.already_pending(PYLON) == 0:
        #     worker = self.workers.idle.random_or(None)
        #     if self.can_afford(PYLON) and worker:
        #         self.do(worker.build(UnitTypeId.PYLON,near=self.townhalls.ready.random_or(None)))

        # self.build_protoss_ramp_wall()
        # self.manage_worker_count()

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
        [Bot(Race.Protoss, PPPP(), name="The PPPP"), Computer(Race.Protoss, Difficulty.VeryEasy)],
        realtime=False,
    )

if __name__ == "__main__":
    main()
