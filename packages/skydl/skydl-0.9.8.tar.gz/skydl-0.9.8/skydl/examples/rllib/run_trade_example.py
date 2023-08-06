# -*- coding: utf-8 -*-
import sys
import numpy as np
import skydl.models_zoo.rllib.rlenv.gym
import pandas as pd
import talib
import gym
import baselines.common.tf_util as U
from baselines.deepq import deepq
from baselines.deepq.utils import BatchInput
from baselines.deepq.replay_buffer import ReplayBuffer
from baselines.common.schedules import LinearSchedule

def do_main():
    csv_path = sys.path[0] + "/../../datasets/data/trading/AAPL.csv"
    df = pd.read_csv(csv_path, usecols=['Date', 'High', 'Low', 'Open', 'Close', 'Volume'])
    df = df[~np.isnan(df['Open'])].set_index('Date')
    # ###calc return
    df['Return'] = df['Close'].pct_change() * 100
    df = df.fillna(0)
    # Normalization of returns
    mean = df['Return'].mean()
    std = df['Return'].std()
    df['Return'] = (df['Return'] - np.array(mean)) / np.array(std)
    # ###calc ATR
    _high = df.High.values
    _low = df.Low.values
    _close = df.Close.values
    # Compute the ATR and perform Normalisation
    df['ATR'] = talib.ATR(_high, _low, _close, timeperiod=14)
    df.dropna(inplace=True)
    df['ATR'] = (df['ATR'] - np.mean(df['ATR'])) / np.std(df['ATR'])
    df.dropna(inplace=True)
    df_min_max = df.drop(['Open', 'High', 'Low', 'Close', 'Volume'], axis=1)
    low_box = df_min_max.min(axis=0).values
    high_box = df_min_max.max(axis=0).values
    env = gym.make('trading-v0')
    env.do_init(q_size=4, states=df, observation=df[['Return', 'ATR']], low_box=low_box, high_box=high_box)

    act, train, update_target, debug = deepq.build_train(
            make_obs_ph=lambda name: BatchInput(env.observation_space.shape, name=name),
            q_func=GymTradingNets._model,
            num_actions=env.action_space.n,
            optimizer=tf.train.AdamOptimizer(learning_rate=5e-4),
        )

if __name__ == '__main__':
    do_main()
