from ML.MLObjectives.MLobjectiveType import MLObjectiveType
from models.bars import Bars
from tradeTypes.tradeType import TradeType
from indicators.indicatorType import IndicatorType


class MLProfitObjective(MLObjectiveType):
    def __init__(
        self,
        trade_type: TradeType,
        indicator: IndicatorType,
        bars: Bars,
    ):
        self.trade_type = trade_type
        self.indicator = indicator
        self.bars = bars

    def objective(self):
        current_pl = 0
        actions = self.indicator.backtest(self.bars)
        for bar, action in zip(self.bars.get_bars().iterrows(), actions):
            current_pl = self.trade_type.handle(action, bar[1])
        return current_pl
