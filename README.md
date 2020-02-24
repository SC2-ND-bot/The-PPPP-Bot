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

This bot will implement a strategy which involves storing a wide vareity of possible build orders (gathered from examples by professional human players) and executing these build orders according to their projected effectiveness.  Right now only a simple, short build order is implemented in the code.  As time goes on this order will be replaced with more effective ones and a full tree will be constructed.

## Control Mechanisms and Functionality

Our bot utilizes two control mechanisms to strategically pursue victory:

The first is a behavior tree which implements the build orders discussed above.  The tree is implemented using two additional classes, buildtreeNode and buildOrder.  The node class contains functionality which allows for the evaluation and execution of training units, building buildings, or conducting research.  Each node represents a singular action and the conditions that must be met for it to be undertaken.  The buildOrder class constructs all of the nodes at the beginning of the game and handles stepping through the tree.  After a node is executed, this class evaluates which branch to take to move further down an optimal build order.  Decisions on which buildOrder to pursue down the tree can be made on a variety of factors including enemy race, enemy units on the map, game duration, resources available, and others.

The second is **WRITE G.O.A.P. DESCRIPTION HERE**

## Dependancies

Dependancies are listed below.  See the installation section for instructions on how to install them.

*StarCraft II*
- [Starcraft II: Wings of Liberty](https://www.battle.net/download/getInstallerForGame?gameProgram=STARCRAFT_2)
- [Maps](http://blzdistsc2-a.akamaihd.net/MapPacks/Ladder2019Season3.zip)
-  MacOS, Windows, or Linux running Wine

*The Bot*
- [Python 3.7](https://www.python.org/downloads/release/python-381/)
- [SC2 API](https://github.com/BurnySc2/python-sc2) (Installed by the Makefile)