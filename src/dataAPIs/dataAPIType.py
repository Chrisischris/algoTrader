from abc import ABC, abstractmethod
from models.bars import Bars
from datetime import datetime
from alpaca_trade_api.rest import TimeFrame


class DataAPIType(ABC):
    @abstractmethod
    def get_bars_timeframe(
        self, symbol: str, timeframe: TimeFrame, start: datetime, end: datetime
    ) -> Bars:
        """Get price bars of a certain timeframe and return as a Bars object

        Args:
            symbol (str): Stock symbol
            timeframe ([type]): Timeframe: Hourly, Minutely, etc., These will use
                alpacas b/c it makes the most sense
            start (datetime): Start Date
            end (datetime): End Date

        Returns:
            Bars: The bars for that timeframe
        """
        pass

    # TODO Add methods for data streaming
