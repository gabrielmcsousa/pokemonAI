from enum import Enum, IntEnum

class GameState(Enum):
    NONE = 0,
    RUNNING = 1,
    ENDED = 2

class PlayerOri():
    #TODO: FIX ORIENTATION ISSUE. ONLY TURNING CLOCKWISE AND NOT DOING FULL 360
    UP = 0
    RIGHT = 90
    DOWN = 180
    LEFT = 270
    TURN_LEFT = 4
    TURN_RIGHT = 5