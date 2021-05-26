from ML.MLObjectives.MLobjectiveType import MLObjectiveType
from models.bars import Bars
from tradeTypes.tradeType import TradeType
from indicators.indicatorType import IndicatorType


class MLProfitObjective(MLObjectiveType):
    def __init__(
        self,
        tradeType: TradeType,
        indicator: IndicatorType,
        bars: Bars,
    ):
        self.tradeType = tradeType
        self.indicator = indicator
        self.bars = bars

    def objective(self):
        currentPL = 0
        actions = self.indicator.backtest(self.bars)
        for bar, action in zip(self.bars.get_bars().iterrows(), actions):
            currentPL = self.tradeType.handle(action, bar[1])
        return currentPL
