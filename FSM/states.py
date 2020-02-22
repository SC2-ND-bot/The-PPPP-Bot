from enum import Enum, auto

class AgentStates(Enum):
    IDLE_STATE: 1
    PERFORM_ACTION_STATE: 2
    END_STATE: 3