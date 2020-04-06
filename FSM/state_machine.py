class StateMachine:
    def __init__(self):
        self.handlers = {}
        self.startState = None
        self.endStates = []
        self.currentState = None

    def add_state(self, name, handler, endState=False):
        self.handlers[name] = handler
        if endState:
            self.endStates.append(name)

    def set_start(self, name):
        self.startState = name

    def run_step(self, gameObject):

        if self.currentState is None:
            self.currentState = self.startState

        try:
            handler = self.handlers[self.currentState]
        except:
            raise KeyError("must call .set_start() before .run_step()")
        if not self.endStates:
            raise Exception("at least one state must be an end_state")

        # Perform State Action
        newState = handler(gameObject)

        if newState in self.endStates:
            print('reached end state for unit')
        else:
            self.currentState = newState
