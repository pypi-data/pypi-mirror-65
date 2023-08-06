# coding: utf-8 or # -*- coding: utf-8 -*-
"""
参考：OpenAI Gym for Trading With DQN OpenAI Baseline  https://github.com/AdrianP-/gym_trading
OpenAI Baseline: https://github.com/openai/baselines
Gym_trading by Peter Henry: https://github.com/Henry-bee/gym_trading/
Also, good thougths in Trading and Q learning: https://github.com/savourylie/Stock-Price-Forecaster
https://github.com/Prediction-Machines/Trading-Gym
https://github.com/Prediction-Machines/Trading-Brain
https://github.com/Kismuz/btgym
"""
# import matplotlib.dates as mdates
# import matplotlib.finance as mf
import matplotlib.pyplot as plt
from .super_env import SuperEnv
from .trading.portfolio import Portfolio
import pandas as pd


class TradingEnv(SuperEnv):

    def __init__(self):
        super().__init__()

    def do_init(self, q_size=4, gamma=0.8, states=[], observation=[], low_box=0, high_box=0, train=True):
        super().do_init(q_size=q_size, gamma=gamma, states=states, observation=observation, low_box=low_box, high_box=high_box, train=train)
        self.portfolio = Portfolio(prices=states[['Open', 'Close']], trade_period=5000, train_end_index=observation.shape[0])

    def reset(self):
        super().reset()
        if self.train:
            obs = self.observation.values[0]
            self.current_index = 1
            self._end = self.observation.shape[0] - 1
        else:
            obs = self.observation.values[0]
            self.current_index = 1
            self._end = self.observation.shape[0] - 1
        self._data = self.states.iloc[self.current_index:self._end + 1]
        self.portfolio._reset(self.train)
        return obs

    def step(self, action):
        super().step(action)
        # Return the observation, done, reward from Simulator and Portfolio
        reward, info = self.portfolio._step(action)
        # obs, done = self.sim._step(self.portfolio.open_trade, self.portfolio.curr_trade["Trade Duration"])
        if self.portfolio.open_trade:
            obs = self.observation.values[self.current_index] + [self.portfolio.open_trade] + [self.portfolio.curr_trade["Trade Duration"]]
        else:
            obs = self.observation.values[self.current_index]
        self.current_index += 1
        done = self.current_index > self._end
        return obs, reward, done, info

    def render(self, mode='human'):
        super().render(mode)

    def seed(self, seed=None):
        return super().seed(seed)

    def generate_summary_stats(self):
        print("SUMMARY STATISTICS")
        journal = pd.DataFrame(self.portfolio.journal)
        print("Total Trades Taken: ", journal.shape[0])
        print("Total Reward: ", journal['Profit'].sum())
        print("Average Reward per Trade: ", journal['Profit'].sum() / journal['Profit'].count())
        print("Win Ratio: %s %%" % (((journal.loc[journal['Profit'] > 0, 'Profit'].count()) / journal.shape[0]) * 100))

        fig, ax = plt.subplots(figsize=(40, 10))

        data = self._data
        # Get a OHLC list with tuples (dates, Open, High, Low, Close)
        # ohlc = list(zip(mdates.date2num(data.index.to_pydatetime()), data.Open.tolist(), data.High.tolist(), data.Low.tolist(), data.Close.tolist()))
        ohlc = list(zip(list(range(data.shape[0])), data.Open.tolist(), data.High.tolist(),
                        data.Low.tolist(), data.Close.tolist()))
        # Filter out buy and sell orders for plotting
        buys = journal.loc[journal.Type == 'BUY', :]
        sells = journal.loc[journal.Type == 'SELL', :]

        # #Plotting functions
        # mf.candlestick_ohlc(ax, ohlc, width=0.02, colorup='green', colordown='red')
        ax.plot(buys['Entry Time'], buys['Entry Price'] - 0.001, 'b^', alpha=1.0)
        ax.plot(sells['Entry Time'], sells['Entry Price'] + 0.001, 'rv', alpha=1.0)

        print("-----save plt to png: trading_env.png")
        plt.savefig("trading_env.png")
        # plt.show()

        import pprint
        pp = pprint.PrettyPrinter(indent=2)
        pp.pprint(self.portfolio.journal)
