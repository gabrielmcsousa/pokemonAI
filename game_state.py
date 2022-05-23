from enum import Enum

class GameState(Enum):
    NONE = 0,
    RUNNING = 1,
    ENDED = 2,
    WIN = 3,
    LOSE = 4