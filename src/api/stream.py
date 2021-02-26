from typing import Any, Callable, Dict, Iterable
from tda.auth import easy_client
from tda import auth
from tda.streaming import StreamClient
from auth.const import API_KEY, ACCOUNT_ID, TOKEN_PATH, REDIRECT_URI
from selenium import webdriver

import asyncio
import json
import logging
logging.getLogger('').addHandler(logging.StreamHandler())

# client = easy_client(
#         api_key=API_KEY,
#         redirect_uri=REDIRECT_URI,
#         token_path=TOKEN_PATH,
#         webdriver_func=lambda: webdriver.Chrome())
try:
    client = auth.client_from_token_file(TOKEN_PATH, API_KEY)
    stream_client = StreamClient(client, account_id=int(ACCOUNT_ID))
except FileNotFoundError:
    from selenium import webdriver
    from webdriver_manager.chrome import ChromeDriverManager
    with webdriver.Chrome(ChromeDriverManager().install()) as driver:
        client = auth.client_from_login_flow(
            driver, API_KEY, REDIRECT_URI, TOKEN_PATH)
        stream_client = StreamClient(client, account_id=int(ACCOUNT_ID))

async def read_stream(handler: Callable[[Dict[Any, Any]], None], symbols: Iterable[str]):
  await stream_client.login()
  await stream_client.quality_of_service(StreamClient.QOSLevel.EXPRESS)
  await stream_client.chart_equity_subs(
    symbols=symbols,
  )
  stream_client.add_chart_equity_handler(handler)
  #await stream_client.quality_of_service(StreamClient.QOSLevel.EXPRESS)
  #await stream_client.level_one_equity_subs(
  #  symbols=symbols, 
    # fields=[StreamClient.LevelOneEquityFields.BID_PRICE, 
    #         StreamClient.LevelOneEquityFields.ASK_PRICE, 
    #         StreamClient.LevelOneEquityFields.LAST_PRICE]
  #)
  #stream_client.add_level_one_equity_handler(handler)

  while True:
      await stream_client.handle_message()

def start_stream(handler: Callable[[Dict[Any, Any]], None], symbols: Iterable[str]):
  asyncio.get_event_loop().run_until_complete(read_stream(handler, symbols))