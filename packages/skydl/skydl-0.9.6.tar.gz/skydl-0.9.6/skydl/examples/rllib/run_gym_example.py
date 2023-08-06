# -*- coding: utf-8 -*-
import gym
import skydl.models_zoo.rllib.rlenv.gym

env = gym.make("qtable-v0")
env.do_init(q_size=6)
for i_episode in range(50):
    print(f"======episode={i_episode}, env.action_space.n={env.action_space.n}")
    observation = env.reset()
    for t in range(env.action_space.n):
        env.render("human")
        action = env.action_space.sample()
        observation, reward, done, info = env.step(action)
        if done:
            break