class StateMachine:
    def __init__(self):
        self.handlers = {}
        self.startState = None
        self.endStates = []
        self.currentState = None

    def add_state(self, name, handler, endState=False):
        name = name.upper()
        self.handlers[name] = handler
        if end_state:
            self.endStates.append(name)
    
    def set_start(self, name):
        self.startState = name.upper()

    def run_step(self, state):
        if self.currentState is None:
            self.currentState = self.startState

        try:
            handler = self.handlers[self.currentState]
        except:
            raise InitializationError("must call .set_start() before .run_step()")
        if not self.endStates:
            raise  InitializationError("at least one state must be an end_state")
        
        
        newState = handler(state).upper()
        
        if newState in self.endStates:
            print('reached end state for unit')
        else:
            self.currentState = newState
        