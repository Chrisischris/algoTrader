from alpaca_trade_api.rest import REST
from dataAPIs.dataAPIType import DataAPIType
from auth.const import APCA_API_KEY_ID, APCA_API_SECRET_KEY
from models.bars import Bars
from datetime import datetime


class AlpacaDataAPI(DataAPIType):
    def __init__(self) -> None:
        self.api = REST(APCA_API_KEY_ID, APCA_API_SECRET_KEY)

    def get_bars_timeframe(
        self, symbol: str, timeframe, start: datetime, end: datetime
    ) -> Bars:
        date_format = "%Y-%m-%d"
        start = start.strftime(date_format)
        end = end.strftime(date_format)
        bars = self.api.get_bars(symbol, timeframe, start, end, adjustment="raw").df
        return Bars(bars)
