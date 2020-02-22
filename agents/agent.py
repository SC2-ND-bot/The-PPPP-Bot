from FSM.state_machine import StateMachine
from FSM.states import AgentStates

# TODO for @Hermes: create loadActions, DataProvider
# TODO: figure out communication between game, FSM, and actions

class Agent:

    def __init__(self, unit):
        self.unit = unit
        self.stateMachine = StateMachine()

        self.availableActions = []
        self.currentActions = []

        self.stateMachine.add_state(AgentStates.IDLE_STATE, self.idleStateHandler)
        self.stateMachine.add_state(AgentStates.PERFORM_ACTION_STATE, self.performActionStateHandler)
        self.stateMachine.add_state(AgentStates.END_STATE, self.endStateHandler)

        self.stateMachine.set_start(AgentStates.IDLE_STATE)

        # TODO: Create DataProvider which feeds the agents goals and state information
        # self.dataProvider = DataProvider()

        # TODO: Define AgentPlanner class
        # self.planner = AgentPlanner()

    def idleStateHandler(self):
        # TODO: getGoal() should return a key:string -> value:boolean pair
        goal = self.dataProvider.getGoal()

        # TODO: Should return all relevant world information 
        worldState = self.dataProvider.getWorldState()

        # agent, actions, state, goal
        plan = self.planner.plan(goal, worldState, availableActions)

        if plan is not None:
            self.currentActions = plan
            return AgentStates.PERFORM_ACTION_STATE
        else:
            print('No valid plan found, agent will remain idle')
            return AgentStates.IDLE_STATE
        

    def performActionStateHandler(self):
        if not self.hasActivePlan():
            return AgentStates.IDLE_STATE

        action = self.currentActions[0]
        if action.isFinished():
            self.currentActions.pop(0)

        if self.hasActivePlan():
            newAction = self.currentActions[0]
            success = newAction.perform()

            if not success:
                print('Action failed, going back to idle state')
                return AgentStates.IDLE_STATE
                
            return AgentStates.PERFORM_ACTION_STATE

    def hasActivePlan(self):
        return len(self.currentActions) > 0

    # def loadActions(self):

    # # Still unsure if we require this state and handler
    # def endStateHandler(self):
