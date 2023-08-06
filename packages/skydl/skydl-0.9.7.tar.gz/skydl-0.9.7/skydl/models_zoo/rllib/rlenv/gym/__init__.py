"""
https://github.com/dennybritz/reinforcement-learning
Deep Reinforcement Learning Demysitifed (Episode 2) — Policy Iteration, Value Iteration and Q-learning
https://medium.com/@m.alzantot/deep-reinforcement-learning-demysitifed-episode-2-policy-iteration-value-iteration-and-q-978f9e89ddaa
"""
from gym.envs.registration import register

register(
    id='qtable-v0',
    entry_point='skydl.models_zoo.rllib.rlenv.gym.envs:QTableEnv',
    # max_episode_steps=1000,
    # reward_threshold=200
)
register(
    id='trading-v0',
    entry_point='skydl.models_zoo.rllib.rlenv.gym.envs:TradingEnv',
    # max_episode_steps=1000,
    # reward_threshold=200
)
