# The-ProfanelyPrimalProtossPunster-Bot

## Installation and Testing

First, you must install [Starcraft II: Wings of Liberty](https://www.battle.net/download/getInstallerForGame?gameProgram=STARCRAFT_2) manually through this download.  You must also install [all the maps](http://blzdistsc2-a.akamaihd.net/MapPacks/Ladder2019Season3.zip) by downloading this file.  The password for
the zip file is "iagreetotheeula" and it implies your agreement to the [AI and Machine Learning License](http://blzdistsc2-a.akamaihd.net/AI_AND_MACHINE_LEARNING_LICENSE.html).

You must also have [Python 3.7](https://www.python.org/downloads/release/python-381/) or newer.

Then, you can install all other dependencies by running `make install`.

After installation, you can run the bot in a test game by running `make test`.

Finally, to clean up and remove dependencies you can run `make clean`.

You can also attempt to build the entire environment by executing `make build`.  This will still required your interaction because you will need to sign into your Blizzard account.

## High Level Strategy

This bot will implement a strategy which involves storing a wide vareity of possible build orders (gathered from examples by professional human players) and executing these build orders according to their projected effectiveness.  Right now a build order is implemented in the code for competition against a Zerg opponent.  As time goes on this order will be replaced with more effective ones and a full tree will be constructed.

## Control Mechanisms and Functionality

Our bot utilizes four control mechanisms to strategically pursue victory:

The first is a behavior tree which implements the build orders discussed above.  The tree is implemented using two additional classes, buildtreeNode and buildOrder.  The node class contains functionality which allows for the evaluation and execution of training units, building buildings, or conducting research.  Each node represents a singular action and the conditions that must be met for it to be undertaken.  The buildOrder class constructs all of the nodes at the beginning of the game and handles stepping through the tree.  After a node is executed, this class evaluates which branch to take to move further down an optimal build order.  Decisions on which buildOrder to pursue down the tree can be made on a variety of factors including enemy race, enemy units on the map, game duration, resources available, and others.

The second is a finite state machine which controls all army and structure production after the initial build order is complete.  It does this by determining what units and buildings the enemy has and then constructing its own units and buildings to counter them.  It utilizes established best-known counters gathered from the online Starcraft II community.  This leads to a late-game army composition which is optimally build to defeat the specific enemy that the bot is playing against.

The third is a finite state machine which manages the bot's econonmy.  It dynamically evaluates the game state to determien when to build probes, assimilators, expansions, and pylons.  It also works to properly distribute workers in order to maintain the optimal ratio of mineral to gas resource gathering.

The fourth is a Goal Orientied Action Planner, which is in charge of controlling units at a micro scale. It does so by utilizing four main pieces. 

1. Agents:
Each agent is in of defining their FSM and triggering each 'tick', as well as determining what actions it has available to perform. The following agents have been implemented:
   - Adept: Early game unit used to apply early pressure to the opponent. Good against light enemies.
   - Sentry: Unit which has many abilities, and is used to create hallucinations for scouting purposes.
   - Phoenix: Flying unit which does bonus damage against light units. Also, hallucinations of this unit are usually used to scout. 
2. Planner:
Determines what sequence of actions it has to perform in order to meet the goal and determines what goal each agent should complete (this is yet to be implemented)
3. Actions:
 Allow the planner to determine which sequence of actions to create by providing a list of preconditions and effects, as well as a cost associated with the action. It also includes the finer details of how the bot will execute each action. The following actions have been implemented:
   - FindEnemyAction: As the name suggest, this action is used to attack the opposing team when the player has spotted any enemy units.
   - AttackEnemyAction: Action which target specific enemy units, currently it simply pics the weakest unit.
   - RetreatAction: This action allows the friendly unit to retreat while it's weapon is on cooldown or its health is criticially low.
   - ScoutAction: Sends a hallucination unit to the enemy base
   - ScoutHallucinationAction: Creates a hallucination for scouting purposes
4. Finite State Machine:
The FSM will place each agent into either an idle or a performAction state where it can calculate upcoming goals/plans or execture specific actions respectively.

A lot of the unit specific work related to the GOAP is yet to be implemented, however the groundwork has been established so that now unit specific code can be written modularly. Currently the Protoss units that have been integrated as agents are Zealots, Adepts, Sentries, Stalkers, Phoenixes, and Immortals.

## Dependancies

Dependancies are listed below.  See the installation section for instructions on how to install them.

*StarCraft II*
- [Starcraft II: Wings of Liberty](https://www.battle.net/download/getInstallerForGame?gameProgram=STARCRAFT_2)
- [Maps](http://blzdistsc2-a.akamaihd.net/MapPacks/Ladder2019Season3.zip)
-  MacOS, Windows, or Linux running Wine

*The Bot*
- [Python 3.7](https://www.python.org/downloads/release/python-381/)
- [SC2 API](https://github.com/BurnySc2/python-sc2) (Installed by the Makefile)
