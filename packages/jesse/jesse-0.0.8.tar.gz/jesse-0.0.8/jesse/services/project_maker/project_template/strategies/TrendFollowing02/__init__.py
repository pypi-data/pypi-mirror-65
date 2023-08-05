from jesse.indicators import ema, srsi, atr
from jesse.strategies import Strategy
from jesse import utils


class TrendFollowing02(Strategy):
    def __init__(self, exchange, symbol, timeframe, hyper_parameters=None):
        if hyper_parameters is None:
            self.hp = default_hp
        else:
            self.hp = hyper_parameters

        super().__init__(
            'TrendFollowing02',
            '0.1.0',
            exchange=exchange,
            symbol=symbol,
            timeframe=timeframe
        )

    def should_long(self):
        # optimization trick: encounter the main timeframe and leave the anchor timeframe for further checking
        if not (self.is_trending_up and self.is_over_sold):
            return False

        if self.symbol in ['BTCUSDT', 'BTCUSD']:
            anchor_momentum = self.symbol_momentum == 1
        else:
            anchor_momentum = self.btc_momentum == 1 or self.symbol_momentum == 1

        if self.btc_daily_momentum == 1 and anchor_momentum:
            return True

        return False

    def should_short(self):
        # optimization trick: encounter the main timeframe and leave the anchor timeframe for further checking
        if not (self.is_trending_down and self.is_over_bought):
            return False

        if self.symbol in ['BTCUSDT', 'BTCUSD']:
            anchor_momentum = self.symbol_momentum == -1
        else:
            anchor_momentum = self.btc_momentum == -1 or self.symbol_momentum == -1

        if self.btc_daily_momentum == -1 and anchor_momentum:
            return True

    def go_short(self):
        entry = self.low - (self.atr * 0.3)
        stop = self.high + self.atr * self.hp['stop_loss_atr_rate']
        qty = utils.risk_to_qty(self.capital, 3, entry, stop)
        qty = round(qty, 2)

        self.sell = qty, round(entry, 2)
        self.stop_loss = qty, round(stop, 2)
        risk = abs(entry - stop)
        take_profit_price = entry - risk * self.hp['take_profit_rate']
        self.take_profit = qty, round(take_profit_price, 2)

    def go_long(self):
        entry = self.high + (self.atr * 0.3)
        stop = self.low - self.atr * self.hp['stop_loss_atr_rate']
        qty = utils.risk_to_qty(self.capital, 3, entry, stop)
        qty = round(qty, 2)

        self.buy = qty, round(entry, 2)
        self.stop_loss = qty, round(stop, 2)
        risk = abs(entry - stop)
        take_profit_price = entry + risk * self.hp['take_profit_rate']
        self.take_profit = qty, round(take_profit_price, 2)

    def should_cancel(self):
        return True

    @property
    def is_trending_up(self):
        return (self.EMA_200 < self.longer_EMA) and (self.longer_EMA < self.long_EMA) and (
                self.long_EMA < self.short_EMA)

    @property
    def is_trending_down(self):
        return (self.EMA_200 > self.longer_EMA) and (self.longer_EMA > self.long_EMA) and (
                self.long_EMA > self.short_EMA)

    @property
    def is_over_bought(self):
        return self.stoch > self.hp['overbought_level']

    @property
    def is_over_sold(self):
        return self.stoch < self.hp['oversold_level']

    @property
    def btc_daily_momentum(self):
        symbol = 'BTCUSD' if self.exchange == 'Bitfinex' else 'BTCUSDT'

        short = ema(self.get_candles(self.exchange, symbol, '1D'), self.hp['daily_short_EMA'])
        long = ema(self.get_candles(self.exchange, symbol, '1D'), self.hp['daily_long_EMA'])
        longer = ema(self.get_candles(self.exchange, symbol, '1D'), self.hp['daily_longer_EMA'])

        if short > long and long > longer:
            return 1
        elif short < long and long < longer:
            return -1
        else:
            return 0

    @property
    def btc_momentum(self):
        symbol = 'BTCUSD' if self.exchange == 'Bitfinex' else 'BTCUSDT'

        short = ema(self.get_candles(self.exchange, symbol, utils.anchor_timeframe(self.timeframe)),
                    self.hp['anchor_short_EMA'])
        long = ema(self.get_candles(self.exchange, symbol, utils.anchor_timeframe(self.timeframe)),
                   self.hp['anchor_long_EMA'])

        if short > long:
            return 1
        elif short < long:
            return -1
        else:
            return 0

    @property
    def symbol_momentum(self):
        short = ema(self.get_candles(self.exchange, self.symbol, utils.anchor_timeframe(self.timeframe)),
                    self.hp['anchor_short_EMA'])
        long = ema(self.get_candles(self.exchange, self.symbol, utils.anchor_timeframe(self.timeframe)),
                   self.hp['anchor_long_EMA'])

        if short > long:
            return 1
        elif short < long:
            return -1
        else:
            return 0

    # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # indicators
    # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    @property
    def long_EMA(self):
        return ema(self.candles, self.hp['long_EMA'])

    @property
    def longer_EMA(self):
        return ema(self.candles, self.hp['longer_EMA'])

    @property
    def EMA_200(self):
        return ema(self.candles, 200)

    @property
    def short_EMA(self):
        return ema(self.candles, self.hp['short_EMA'])

    @property
    def shorter_EMA(self):
        return ema(self.candles, self.hp['shorter_EMA'])

    @property
    def stoch(self):
        k, d = srsi(self.candles)
        return k

    @property
    def atr(self):
        return atr(self.candles)

    # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # filters
    # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    def filters(self):
        return [
            self.filter_1,
            self.filter_2,
            self.filter_3,
            self.filter_4,
            self.filter_5
        ]

    def filter_1(self) -> bool:
        """
        Reward/Risk ratio (R) must worth it
        """
        risk_per_qty = abs(self.average_entry_price - self.average_stop_loss)
        reward_per_qty = abs(self.average_take_profit - self.average_entry_price)

        R = abs(reward_per_qty / risk_per_qty)
        return (R > self.hp['min_R']) and (R < self.hp['max_R'])

    def filter_2(self) -> bool:
        return abs(self.price - self.long_EMA) < abs(self.price - self.longer_EMA)

    def filter_3(self) -> bool:
        return (abs(self.longer_EMA - self.long_EMA) / self.price) * 100 > self.hp['min_distance_between_EMAs']

    def filter_4(self) -> bool:
        if self.is_trending_up:
            passed = self.low > self.longer_EMA
        elif self.is_trending_down:
            passed = self.high < self.longer_EMA
        else:
            passed = False

        return passed

    def filter_5(self) -> bool:
        reward_per_qty = abs(self.average_take_profit - self.average_entry_price)

        if (reward_per_qty / self.average_entry_price) * 100 < self.hp['min_pnl']:
            return False

        return True

    # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # Genetic
    # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    @staticmethod
    def hyper_parameters():
        return [
            {'name': 'min_pnl', 'type': float, 'min': 1.0, 'max': 2.0},
            {'name': 'min_distance_between_EMAs', 'type': float, 'min': 0.1, 'max': 2.0},
            {'name': 'min_R', 'type': float, 'min': 0.8, 'max': 1.5},
            {'name': 'max_R', 'type': float, 'min': 3.5, 'max': 5.0},
            {'name': 'short_EMA', 'type': int, 'min': 9, 'max': 30},
            {'name': 'long_EMA', 'type': int, 'min': 31, 'max': 80},
            {'name': 'longer_EMA', 'type': int, 'min': 81, 'max': 200},
            {'name': 'daily_short_EMA', 'type': int, 'min': 9, 'max': 30},
            {'name': 'daily_long_EMA', 'type': int, 'min': 31, 'max': 80},
            {'name': 'daily_longer_EMA', 'type': int, 'min': 81, 'max': 200},
            {'name': 'anchor_short_EMA', 'type': int, 'min': 9, 'max': 30},
            {'name': 'anchor_long_EMA', 'type': int, 'min': 31, 'max': 80},
            {'name': 'anchor_longer_EMA', 'type': int, 'min': 81, 'max': 200},
            {'name': 'oversold_level', 'type': int, 'min': 1, 'max': 40},
            {'name': 'overbought_level', 'type': int, 'min': 60, 'max': 99},
            {'name': 'stop_loss_atr_rate', 'type': float, 'min': 0.8, 'max': 3.5},
            {'name': 'take_profit_rate', 'type': float, 'min': 1.0, 'max': 3.0}
        ]


# default hyper parameters
default_hp = {
    'min_pnl': .5,
    'min_distance_between_EMAs': 0.2,
    'min_R': 1.0,
    'max_R': 5.0,
    'short_EMA': 21,
    'long_EMA': 50,
    'longer_EMA': 100,
    'anchor_short_EMA': 21,
    'anchor_long_EMA': 50,
    'anchor_longer_EMA': 100,
    'daily_short_EMA': 21,
    'daily_long_EMA': 50,
    'daily_longer_EMA': 100,
    'oversold_level': 20,
    'overbought_level': 80,
    'stop_loss_atr_rate': 2,
    'take_profit_rate': 1.5
}
