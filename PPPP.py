import random

import sc2
from sc2 import Race, Difficulty
from sc2.constants import *
from sc2.player import Bot, Computer

class PPPP(sc2.BotAI):
    async def on_step(self, iteration):
        if iteration == 0:
            await self.chat_send("(probe)(pylon)(cannon)(cannon)(gg)")

        if not self.townhalls:
            # Attack with all workers if we don't have any nexuses left, attack-move on enemy spawn (doesn't work on 4 player map) so that probes auto attack on the way
            for worker in self.workers:
                self.do(worker.attack(self.enemy_start_locations[0]))
            return

        potential_working_locations = {}

        nexuses = self.structures(NEXUS)

        print(self.resources[0].position.y)

        for worker in self.workers:
            if worker.is_idle:
                print("this worker is idle, here are the available structures")
                for resource in self.resources:
                    remaining = 0
                    if resource.is_vespene_geyser:
                        remaining = resource.vespene_contents
                    else:
                        remaining = resource.mineral_contents
                    potential_working_locations[resource.position] = {
                        "empty": remaining <= 0,
                        "full": resource.ideal_harvesters - resource.assigned_harvesters <= 0
                    }


        # If we have no pylon, build one near starting nexus
        if self.supply_left < 4 and self.already_pending(PYLON) == 0:
            if self.can_afford(PYLON):
                await self.build(PYLON, near=self.main_base_ramp.protoss_wall_pylon)


        # Make probes until we have 16 total
        for nexus in nexuses:
            if self.supply_workers < 22 * len(nexuses) and nexus.is_idle:
                if self.can_afford(PROBE):
                    self.do(nexus.train(PROBE), subtract_cost=True, subtract_supply=True)
        
        abilities = await self.get_available_abilities(nexuses)
        for loop_nexus, abilities_nexus in zip(nexuses, abilities):
            if AbilityId.EFFECT_CHRONOBOOSTENERGYCOST in abilities_nexus:
                for nexus in nexuses:
                    if not nexus.is_idle and not nexus.has_buff(BuffId.CHRONOBOOSTENERGYCOST):
                        self.do(loop_nexus(AbilityId.EFFECT_CHRONOBOOSTENERGYCOST, nexus))
                        break

def main():
    sc2.run_game(
        sc2.maps.get("AcropolisLE"),
        [Bot(Race.Protoss, PPPP(), name="CheeseCannon"), Computer(Race.Protoss, Difficulty.VeryEasy)],
        realtime=False,
    )


if __name__ == "__main__":
    main()
