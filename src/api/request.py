from tda import auth, client
from auth.const import API_KEY, REDIRECT_URI, TOKEN_PATH
import json
from datetime import datetime, timedelta

def request(symbol: str, start: datetime, end: datetime):
  try:
      c = auth.client_from_token_file(TOKEN_PATH, API_KEY)
  except FileNotFoundError:
      from selenium import webdriver
      from webdriver_manager.chrome import ChromeDriverManager
      with webdriver.Chrome(ChromeDriverManager().install()) as driver:
          c = auth.client_from_login_flow(
              driver, API_KEY, REDIRECT_URI, TOKEN_PATH)

  # TODO Handle requests for greater than api willing to return
  r = c.get_price_history(
      symbol,
      start_datetime = start,
      end_datetime = end,
      frequency_type = client.Client.PriceHistory.FrequencyType.MINUTE,
      frequency = client.Client.PriceHistory.Frequency.EVERY_MINUTE,
    )
  assert r.status_code == 200, r.raise_for_status()
  
  res = r.json()
  # print(json.dumps(res, indent=4))
  resStart = datetime.fromtimestamp(res['candles'][0]['datetime'] / 1000)
  resEnd = datetime.fromtimestamp(res['candles'][len(res['candles']) - 1]['datetime'] / 1000)
  # print('Data Start: ', resStart.isoformat(' '))
  # print('Data End: ', resEnd.isoformat(' '))

  if not(start.timestamp() - 60 < resStart.timestamp() and start.timestamp() + 60 > resStart.timestamp()):
    print('Response start is more than 60 seconds off from requested')
    print('Requested: ', start.isoformat(' '))
    print('Response:  ', resStart.isoformat(' '))
  if not(end.timestamp() - 60 < resEnd.timestamp() and end.timestamp() + 60 > resEnd.timestamp()):
    print('Response end is more than 60 seconds off from requested')
    print('Requested: ', end.isoformat(' '))
    print('Response:  ', resEnd.isoformat(' '))
  return res
