from typing import List
from auth.const import Actions
from indicators.indicatorType import IndicatorType
from models.bars import Bars
import talib


class MACD(IndicatorType):
    def __init__(self, fastperiod=12, slowperiod=26, signalperiod=9, **kwargs):
        self.fastp = fastperiod
        self.slowp = slowperiod
        self.signalp = signalperiod

    def run(self, bars: Bars) -> Actions:
        """MACD based trade signals, return BUY, SELL

        Args:
            bars (Bars): Price History

        Returns:
            [Actions]: Trade Action
        """
        close = bars.get_close_numpy()

        macd, macdsignal, macdhist = talib.MACD(
            close,
            fastperiod=self.fastp,
            slowperiod=self.slowp,
            signalperiod=self.signalp,
        )

        last = len(macdhist) - 1
        if macdhist[last - 1] < 0 and macdhist[last] >= 0:
            # - to + BUY
            return Actions.BUY
        elif macdhist[last - 1] >= 0 and macdhist[last] < 0:
            # + to - SELL
            return Actions.SELL
        else:
            return Actions.NONE

    def backtest(self, bars: Bars) -> List:
        """Use this for more efficient backtesting since MACD will only be run once.
            Will return a list of actions for each bar.

        Args:
            bars (Bars): Price History
        """
        close = bars.get_close_numpy()

        macd, macdsignal, macdhist = talib.MACD(
            close,
            fastperiod=self.fastp,
            slowperiod=self.slowp,
            signalperiod=self.signalp,
        )

        actions = []

        for index, hist in enumerate(macdhist):
            if macdhist[index - 1] < 0 and hist >= 0:
                actions.append(Actions.BUY)
            elif macdhist[index - 1] >= 0 and hist < 0:
                actions.append(Actions.SELL)
            else:
                actions.append(Actions.NONE)

        return actions
