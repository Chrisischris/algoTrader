from typing import Any, Dict, List
from pandas import DataFrame, Series


class Bars:
    def __init__(self, all_bars: DataFrame):
        if isinstance(all_bars, DataFrame):
            self.bars = all_bars
        elif isinstance(all_bars, List[Dict[Any, Any]]):
            # TODO this is to handle TDA candle format
            pass

    def get_bars(self) -> DataFrame:
        return self.bars

    def get_latest_bar(self) -> Series:
        return self.bars.iloc[len(self.bars) - 1]
