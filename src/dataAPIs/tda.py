from typing import Any, Callable, Dict, Iterable
from alpaca_trade_api.rest import TimeFrame
from auth.const import API_KEY, REDIRECT_URI, TOKEN_PATH, ACCOUNT_ID
from dataAPIs.dataAPIType import DataAPIType
from models.bars import Bars
from datetime import datetime
from tda import auth, client
from tda.streaming import StreamClient
import asyncio


class TDADataAPI(DataAPIType):
    def __init__(self) -> None:
        try:
            self.client = auth.client_from_token_file(TOKEN_PATH, API_KEY)
        except FileNotFoundError:
            from selenium import webdriver
            from webdriver_manager.chrome import ChromeDriverManager

            with webdriver.Chrome(ChromeDriverManager().install()) as driver:
                self.client = auth.client_from_login_flow(
                    driver, API_KEY, REDIRECT_URI, TOKEN_PATH
                )

    def get_bars_timeframe(
        self, symbol: str, timeframe: TimeFrame, start: datetime, end: datetime
    ) -> Bars:
        # Update to support alpaca timeframes
        r = self.client.get_price_history(
            symbol,
            start_datetime=start,
            end_datetime=end,
            frequency_type=client.Client.PriceHistory.FrequencyType.MINUTE,
            frequency=timeframe,
        )
        assert r.status_code == 200, r.raise_for_status()

        res = r.json()
        return Bars(res["candles"])

    # Old Streaming code
    async def read_stream(
        self, handler: Callable[[Dict[Any, Any]], None], symbols: Iterable[str]
    ):
        stream_client = StreamClient(self.client, account_id=int(ACCOUNT_ID))
        await stream_client.login()
        await stream_client.quality_of_service(StreamClient.QOSLevel.EXPRESS)
        await stream_client.chart_equity_subs(
            symbols=symbols,
        )
        stream_client.add_chart_equity_handler(handler)

        while True:
            await stream_client.handle_message()

    # Old streaming code
    def start_stream(
        self, handler: Callable[[Dict[Any, Any]], None], symbols: Iterable[str]
    ):
        asyncio.get_event_loop().run_until_complete(self.read_stream(handler, symbols))
