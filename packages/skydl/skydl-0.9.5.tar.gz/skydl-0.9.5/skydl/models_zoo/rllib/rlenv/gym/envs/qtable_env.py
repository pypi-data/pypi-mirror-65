# coding: utf-8 or # -*- coding: utf-8 -*-
"""
参考：http://mnemstudio.org/path-finding-q-learning-example-1.htm
http://www.cnblogs.com/dragonir/p/6224313.html
"""
import numpy as np
from gym import spaces
from py_common_util.common.common_utils import CommonUtils
from .super_env import SuperEnv


class QTableEnv(SuperEnv):
    def __init__(self):
        super().__init__()

    def do_init(self, q_size=4, gamma=0.8, states=[], observation=[], low_box=np.array([]), high_box=np.array([]), train=True):
        super().do_init(q_size=q_size, gamma=gamma, states=states, observation=observation, low_box=low_box, high_box=high_box, train=train)
        self.observation_space = spaces.Box(0, 5, (6,))
        self.q = np.zeros([self.q_size, self.q_size])
        self.initial_states = CommonUtils.cycle([1, 3, 5, 2, 4, 0])
        self.curr_state = 0

    def step(self, action):
        print("_step, action=%d" % action)
        reward, done = self.reward(self.curr_state, action)
        print("===Q value[Action,State]=== %d " % reward)
        print(self.q)
        return self.curr_state, reward, done, None

    def reset(self):
        print("reset")
        self.curr_state = next(self.initial_states)
        print("curr_state=%d" % self.curr_state)
        return None

    def render(self, mode='human'):
        super().render(mode)

    def seed(self, seed=None):
        return super().seed(seed)

    def close(self):
        super().close()

    def maximum(self, state, return_index_only=False):
        winner = 0
        done = False
        while not done:
            found_new_winner = False
            for i in range(self.q_size):
                if i != winner:
                    if self.q[state][i] > self.q[state][winner]:
                        winner = i
                        found_new_winner = True
            if not found_new_winner:
                done = True
        return (winner, done) if return_index_only else (self.q[state][winner], done)

    def reward(self, curr_state, action):
        rewards = np.array(
            [[-1, -1, -1, -1, 0, -1],
            [-1, -1, -1, 0, -1, 100],
            [-1, -1, -1, 0, -1, -1],
            [-1, 0, 0, -1, 0, -1],
            [0, -1, -1, 0, -1, 100],
            [-1, 0, -1, -1, 0, 100]])
        curr_reward = 0
        done = False
        if rewards[curr_state][action] >= 0:
            reward, done = self.maximum(action)
            curr_reward = rewards[curr_state][action] + self.gamma * reward
            self.q[curr_state][action] = curr_reward
            self.curr_state = action
        return curr_reward, done
