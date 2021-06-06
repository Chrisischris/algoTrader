from auth.const import Actions
import datetime
import pytz
import holidays


tz = pytz.timezone("US/Eastern")
us_holidays = holidays.US()


# TODO Compare against schedule, or use TDA to get market hours
def is_after_hours(timestamp: datetime):
    if not timestamp:
        dt = datetime.datetime.now(tz)
    else:
        dt = timestamp
    open_time = datetime.time(hour=9, minute=30, second=0)
    close_time = datetime.time(hour=16, minute=0, second=0)
    # If a holiday
    if dt.strftime("%Y-%m-%d") in us_holidays:
        return True
    # If before 0930 or after 1600
    if (dt.time() < open_time) or (dt.time() > close_time):
        return True
    # If it's a weekend
    if dt.date().weekday() > 4:
        return True

    return False


# TODO use TDA API
def is_after_hours_equity():
    return


# TODO use TDA API
def is_after_hours_options():
    return


def trailing_stop_loss(
    current_price: float, position_high: float, stop_loss_percentage: float
):
    """Trailing Stop Loss Action

    Args:
        current_price (float): Current price
        positionHigh (float): Highest price during postion holding
        stop_loss_percentage (float): How far away to trail
            IE: stopLossPercentage = 5
                positionHigh = 100
                A sell signal would be generated at currentPrice <= 95

    Returns:
        Actions: Action signal
    """
    if current_price <= (position_high * (1 - (stop_loss_percentage / 100))):
        return Actions.SELL
    else:
        return Actions.NONE


def take_profit(
    current_price: float, purchase_price: float, take_profit_percentage: float
):
    """Take Profit Action

    Args:
        current_price (float): Current Price
        purchase_price (float): Price you purchased at
        take_profit_percentage (float): The overall percent you want to take profit at
            IE: takeProfitPercentage = 200
                purchasePrice = 50
                A sell signal would be generated at currentPrice >= 100

    Returns:
        Actions: Action Signal
    """
    if current_price >= (purchase_price * (take_profit_percentage / 100)):
        return Actions.SELL
    else:
        return Actions.NONE
