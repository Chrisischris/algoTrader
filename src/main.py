from autoTraders.backtestTrader import BacktestTrader
from indicators.macd import MACD
from tradeTypes.paperTradeStock import PaperTradeStock
from datetime import datetime
from dataAPIs.alpaca import AlpacaDataAPI
from ML.gridSearch import GridSearch
from sklearn.model_selection import ParameterGrid
from ML.MLObjectives.MLprofitObjective import MLProfitObjective


def main():
    # BACKTESTING

    traders = [
        BacktestTrader(
            PaperTradeStock("AAPL", 10, 120, True),
            MACD(540, 1260, 30),
            AlpacaDataAPI(),
            datetime(2021, 4, 5, 9),
            datetime(2021, 5, 5, 9),
        )
    ]

    BacktestTrader.start_traders(traders)


def macd_grid_search():
    param_grid = ParameterGrid(
        {
            "tsl_percent": [*range(2, 50)],
            "tp_percent": [0, *range(101, 200)],
            "fastperiod": [*range(60, 3600, 240)],
            "slowperiod": [*range(60, 3600, 240)],
            "signalperiod": [*range(30, 3600, 120)],
        }
    )

    max_profit, best_params = GridSearch(
        "TSLA",
        AlpacaDataAPI(),
        param_grid,
        PaperTradeStock,
        MACD,
        MLProfitObjective,
        datetime(2021, 4, 5, 9),
        datetime(2021, 5, 5, 9),
    ).run(True, True)

    print(max_profit, best_params)


if __name__ == "__main__":
    main()
