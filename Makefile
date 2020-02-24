# This Makefile assumes that StarCraft II: Wings of Liberty is already installed
# The bot will look for the Starcraft executable at '/Applications/StarCraft II/Versions'

# Run to install necessary code, execute test, and cleanup
all: install test clean

# Builds the evironment required for the bot itself
build:
	curl -O https://www.battle.net/download/getInstallerForGame?gameProgram=STARCRAFT_2
	curl -O http://blzdistsc2-a.akamaihd.net/MapPacks/Ladder2019Season3.zip
	curl -O https://www.python.org/downloads/release/python-381/
	pip install --upgrade pipenv burnysc2

# Installs the Python library containing the API used by the bot
install:
	pip install --upgrade pipenv burnysc2

# Runs a test game until the user ends the game
test:
	python3 ./PPPP.py	

# Removes the python library containing the API used by the bot
clean:
	pip3 uninstall burnysc2
