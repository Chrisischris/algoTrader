# Algorithmic Stock Trader / Backtester

<p align="center">
<a href="https://github.com/Chrisischris/algoTrader/actions"><img alt="Master Branch Status" src="https://github.com/Chrisischris/algoTrader/actions/workflows/python-app.yml/badge.svg?branch=master"></a>
<a href="https://github.com/psf/black"><img alt="Code style: black" src="https://img.shields.io/badge/code%20style-black-000000.svg"></a>
</p>

## Pre Reqs
1. Create a TDA developer account here https://developer.tdameritrade.com/ and make a new app with a callback url of "http://localhost:8080/" and take note of the "Consumer Key" this is the api key you will give this script

## How To Run From Source
1. In Terminal Run: `pip3 install -r requirements.txt`
    * If you get an error about C++ Build Tools, follow the link and install Visual Studio Build Tools -> C++ Build Tools -> Then make sure C++ x64/x86 Build Tools and Windows 10 SDK are selected under the Optional Installs menu
2. Create auth/const.py using the constTemplate.py
3. In Terminal Run: `python main.py`

## Capabilities
- Choose from the indicators supplied such as MACD, MomentumSMA, or Pivot Points and a Trader
- You can choose to backtest a certain time-frame that outputs to a CSV or output live paper trading