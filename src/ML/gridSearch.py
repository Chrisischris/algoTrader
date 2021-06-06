from typing import Type
from sklearn.model_selection import ParameterGrid
from datetime import datetime, timedelta
from dataAPIs.dataAPIType import DataAPIType
from alpaca_trade_api.rest import TimeFrame
from progressbar import ProgressBar, widgets
from concurrent.futures import as_completed, ProcessPoolExecutor
from models.bars import Bars
from tradeTypes.tradeType import TradeType
from indicators.indicatorType import IndicatorType
from ML.MLObjectives.MLobjectiveType import MLObjectiveType
from auth.const import OUTPUT_PATH
import pandas
import os


class GridSearch:
    """Grid Search for indicatorType and tradeType parameters"""

    my_widgets = [
        widgets.Percentage(),
        " ",
        widgets.SimpleProgress(),
        " ",
        widgets.Bar(),
        " ",
        widgets.Timer(),
        " ",
        widgets.AdaptiveETA(),
        " ",
        widgets.Variable("currentBest", format="Current Best: {formatted_value}"),
    ]

    def __init__(
        self,
        symbol: str,
        data_api: DataAPIType,
        param_grid: ParameterGrid,
        trade_type: Type[TradeType],
        indicator: Type[IndicatorType],
        objective: Type[MLObjectiveType],
        start: datetime = datetime.now() - timedelta(days=7),
        end: datetime = datetime.now(),
    ):
        """init

        Args:
            symbol (str): The stock symbol
            data_api (DataAPIType): Data api
            param_grid (ParameterGrid): These params are all sent to the TradeType and
                the Indicator so be careful with duplicate param names
            trade_type (Type[TradeType]): The Trade Type to use
            indicator (Type[IndicatorType]): The Indicator Type to use
            objective (Type[MLObjectiveType]): The MLObjective to use for determine best
                parameters
            start (datetime, optional): Start date of price data.
                Defaults to datetime.now()-timedelta(days=7).
            end (datetime, optional): End date of price data.
                Defaults to datetime.now().
        """
        self.symbol = symbol
        self.param_grid = param_grid
        self.trade_type = trade_type
        self.indicator = indicator
        self.objective = objective
        self.bars = data_api.get_bars_timeframe(symbol, TimeFrame.Minute, start, end)

    def run(self, output_csv=False, progress_bar=False):
        max_profit = float("-inf")
        best_params = dict()
        results = []

        with ProcessPoolExecutor() as executor:
            futures = []
            for params in self.param_grid:
                futures.append(
                    executor.submit(
                        run_one,
                        params=params,
                        symbol=self.symbol,
                        bars=self.bars,
                        trade_type=self.trade_type,
                        indicator=self.indicator,
                        objective=self.objective,
                    )
                )

            num_done = 0
            if progress_bar:
                pbar = ProgressBar(widgets=self.my_widgets).start(len(futures))

            for future in as_completed(futures):
                params, profit = future.result()

                results.append({**params, "Objective Result": profit})
                if profit > max_profit:
                    max_profit = profit
                    best_params = params

                num_done += 1
                if progress_bar:
                    pbar.update(
                        num_done, currentBest=str(max_profit) + " " + str(best_params)
                    )

        if progress_bar:
            pbar.finish()

        if output_csv:
            all_results = pandas.DataFrame(results)
            all_results.to_csv(
                os.path.join(OUTPUT_PATH, self.symbol + " Grid Search" + ".csv")
            )

        return max_profit, best_params


def run_one(
    params: dict,
    symbol: str,
    bars: Bars,
    trade_type: Type[TradeType],
    indicator: Type[IndicatorType],
    objective: Type[MLObjectiveType],
):
    trader = objective(
        trade_type(symbol, **params),
        indicator(**params),
        bars,
    )

    profit = trader.objective()
    return params, profit
