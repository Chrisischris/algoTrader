from auth.const import Actions
import datetime
import pytz
import holidays


tz = pytz.timezone("US/Eastern")
us_holidays = holidays.US()


# TODO Compare against schedule, or use TDA to get market hours
def isAfterHours(timestamp: datetime):
    if not timestamp:
        dt = datetime.datetime.now(tz)
    else:
        dt = timestamp
    openTime = datetime.time(hour=9, minute=30, second=0)
    closeTime = datetime.time(hour=16, minute=0, second=0)
    # If a holiday
    if dt.strftime("%Y-%m-%d") in us_holidays:
        return True
    # If before 0930 or after 1600
    if (dt.time() < openTime) or (dt.time() > closeTime):
        return True
    # If it's a weekend
    if dt.date().weekday() > 4:
        return True

    return False


# TODO use TDA API
def isAfterHoursEquity():
    return


# TODO use TDA API
def isAfterHoursOptions():
    return


def trailingStopLoss(
    currentPrice: float, positionHigh: float, stopLossPercentage: float
):
    """Trailing Stop Loss Action

    Args:
        currentPrice (float): Current price
        positionHigh (float): Highest price during postion holding
        stopLossPercentage (float): How far away to trail
            IE: stopLossPercentage = 5
                positionHigh = 100
                A sell signal would be generated at currentPrice <= 95

    Returns:
        Actions: Action signal
    """
    if currentPrice <= (positionHigh * (1 - (stopLossPercentage / 100))):
        return Actions.SELL
    else:
        return Actions.NONE


def takeProfit(currentPrice: float, purchasePrice: float, takeProfitPercentage: float):
    """Take Profit Action

    Args:
        currentPrice (float): Current Price
        purchasePrice (float): Price you purchased at
        takeProfitPercentage (float): The overall percent you want to take profit at
            IE: takeProfitPercentage = 200
                purchasePrice = 50
                A sell signal would be generated at currentPrice >= 100

    Returns:
        Actions: Action Signal
    """
    if currentPrice >= (purchasePrice * (takeProfitPercentage / 100)):
        return Actions.SELL
    else:
        return Actions.NONE
