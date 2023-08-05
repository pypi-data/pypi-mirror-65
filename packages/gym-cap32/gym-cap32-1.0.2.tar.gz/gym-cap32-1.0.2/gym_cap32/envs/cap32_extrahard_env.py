import gym
from gym import error, spaces, utils
from gym.utils import seeding
import numpy as np

class Cap32ExtraHardEnv(gym.Env):
    metadata = {'render.modes': ['human']}