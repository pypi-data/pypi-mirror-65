import gym
from gym import error, spaces, utils
from gym.utils import seeding
import os
import numpy as np

try:
    import amle_py
except ImportError as e:
    raise error.DependencyNotInstalled("{}. (HINT: you can install HFO dependencies with 'pip3 install amle-py'.)".format(e))

from amle_py import AmLEInterface


class Cap32Env(gym.Env):
  '''
  This class represent the amle gym environment.
  It's using the amle_python_interface class and it's built by gym.
  '''

  metadata = {'render.modes': ['human']}
  def __init__(self, game, game_path, sound=False, speed=32):
    '''
    Create a new Cap32Env object. The emulator is started with the game loaded.
    The environment is initialized.
    :param game: The game named to loaded.
    :param game_path: The game path to loaded.
    :param sound: Enables/disables sound. Default value: False
    :param speed: Sets the speed of the emulator. Default value: 32
    '''
    self.game = game
    self.game_path = game_path

    if not os.path.exists(self.game_path):
      msg = 'You asked for game %s but path %s does not exist'
      raise IOError(msg % (game, self.game_path))
    
    self.amle = amle_py.AmLEInterface()
    self.amle.toggleSound(sound)
    self.amle.loadSnapshot(game, game_path)

    self.amle.setEmulatorSpeed(speed)

    nbLegalActions = self.amle.getNbLegalActions()
    self._action_set = np.empty(nbLegalActions, dtype=np.int32)
    self.amle.getLegalActions(self._action_set)
    
    self.action_space = spaces.Discrete(len(self._action_set))

    self.screen_height = self.amle.getScreenHeight()
    self.screen_width = self.amle.getScreenWidth()
    self.observation_space = spaces.Box(low=0, high=255, shape=(self.screen_height, self.screen_width), dtype=np.int32)
    
    
  
  def step(self, a):
    '''
    Makes a step in the emulation, goes to the next frame, applies effect of given actions.
    :param a: The action to send.
    :return: Return the observation, reward, a game over boolean and informations as the number of lives.
    '''
    reward = 0.0  
    action = self._action_set[a]
    reward = self.amle.act(action)
    ob = np.zeros(shape=(self.screen_height, self.screen_height))
    self.amle.getScreen(ob)
    return ob, reward, self.amle.gameOver(), {"alme.getNbLives": self.amle.getNbLives()}




  def reset(self):
    '''
    Reset the game.
    '''
    self.amle.resetGame()
    
  def render(self, mode='human'):
    '''
    Empty function because the emulator necessarily display the screen game.
    '''
    pass
  