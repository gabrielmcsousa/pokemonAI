import gym
from gym import spaces

class PokeEnv(gym.Env):
  """Custom Environment that follows gym interface"""
  metadata = {'render.modes': ['human']}

  def __init__(self):
    
    self.action_space = spaces.Discrete(4)

    '''
        observation:
            Player:
                Alive: discrete 2
                Orientation: discrete 4
                Self Pos: box[0, 0 => 44, 44]
                Num of Pokeballs: discrete 25
                Poke state: discrete 2
            
            Obj Sense:
                Object Pos: discrete 5
                Object Type: discrete 8
            
            World:
                Nearest NonUsedPokeStop: box[0, 0 => 44, 44]
                Nearest PokeCenter: box[0, 0 => 44, 44]
                Nearest NonBattledTrainer: box[0, 0 => 44, 44]
    '''

  def step(self, action):
    # Execute one time step within the environment
    ...
  def reset(self):
    # Reset the state of the environment to an initial state
    ...
  def render(self, mode='human', close=False):
    # Render the environment to the screen
    ...