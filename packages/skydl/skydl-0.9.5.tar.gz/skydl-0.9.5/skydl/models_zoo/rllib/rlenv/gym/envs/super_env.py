# coding: utf-8 or # -*- coding: utf-8 -*-
"""
参考：OpenAI Gym for Trading  https://github.com/Henry-bee/gym_trading
"""
import numpy as np
import gym
from gym import spaces


class SuperEnv(gym.Wrapper):
    metadata = {'render.modes': ['human']}

    def __init__(self, env=gym.Env()):
        super().__init__(env)

    def do_init(self, q_size=4, gamma=0.8, states=[], observation=[], low_box=np.array([]), high_box=np.array([]), train=True):
        self.q_size = q_size
        self.gamma = gamma
        self.states = states
        self.observation = observation
        self.action_space = spaces.Discrete(q_size)
        # self.observation_space = spaces.Box(0, 255, [height, width, 3]), for RGB pixels.
        # ref: https://github.com/openai/gym/issues/593
        self.observation_space = spaces.Box(low_box, high_box)  # 需要被子类重新设值
        self.train = train

    def reset(self):
        print("superEnv#reset")

    def step(self, action):
        return None, None, None, None

    def render(self, mode='human'):
        # super().render(mode)
        print("superEnv#render")

    def seed(self, seed=None):
        seed = super().seed(seed)
        print("superEnv#seed")
        return seed

    def close(self):
        super().close()
        print("superEnv#close")


