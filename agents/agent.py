from FSM.state_machine import StateMachine
from FSM.states import AgentStates
from goap_planner import GoapPlanner


# TODO for @Hermes: create loadActions, DataProvider
# TODO: figure out communication between game, FSM, and actions

class Agent:

    def __init__(self, unit):
        self.unit = unit
        self.stateMachine = StateMachine()

        self.availableActions = []
        self.currentActions = []

        self.planner = GoapPlanner()

        self.stateMachine.add_state("IDLE_STATE", self.idleStateHandler)
        self.stateMachine.add_state("PERFORM_ACTION_STATE", self.performActionStateHandler)
        self.stateMachine.add_state("END_STATE", self.endStateHandler, True)
        self.stateMachine.set_start("IDLE_STATE")

        # TODO: Create DataProvider which feeds the agents goals and state information
        # self.dataProvider = DataProvider()

    def idleStateHandler(self, gameObject):
        # TODO: getGoal() should return a key:string -> value:boolean pair
        print('in idle state')
        # goal = self.dataProvider.getGoal()
        goal = ('DISRUPT_ENEMY_ECONOMY', True)

        # TODO: Should return all relevant world information 
        # worldState = self.dataProvider.getWorldState()
        worldState = None

        # agent, actions, state, goal
        plan = self.planner.plan(self, self.availableActions, worldState, goal)

        if plan is not None:
            self.currentActions = plan
            return "PERFORM_ACTION_STATE"
        else:
            print('No valid plan found, agent will remain idle')
            return "IDLE_STATE"

    def performActionStateHandler(self, gameObject):
        if not self.hasActivePlan():
            return "IDLE_STATE"

        action = self.currentActions[0]
        if action.isFinished():
            self.currentActions.pop(0)

        if self.hasActivePlan():
            newAction = self.currentActions[0]
            success = newAction.perform()

            if not success:
                print('Action failed, going back to idle state')
                return "IDLE_STATE"
                
            return "PERFORM_ACTION_STATE"

    def hasActivePlan(self, gameObject):
        return len(self.currentActions) > 0

    def loadActions(self):
        raise NotImplementedError

    # # Still unsure if we require this state and handler
    def endStateHandler(self):
        print('reached end state')
