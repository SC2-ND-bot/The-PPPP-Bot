from enum import Enum

class AgentStates(Enum):
    IDLE_STATE: 0
    PERFORM_ACTION_STATE: 1
    END_STATE: 2