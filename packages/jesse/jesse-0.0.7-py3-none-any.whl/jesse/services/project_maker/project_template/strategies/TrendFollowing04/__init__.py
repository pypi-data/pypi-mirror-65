import jesse.indicators as ta
from jesse.strategies import Strategy
from jesse import utils


class TrendFollowing04(Strategy):
    def __init__(self, exchange, symbol, timeframe, hyper_parameters=None):
        if hyper_parameters is None:
            self.hp = default_hp
        else:
            self.hp = hyper_parameters

        super().__init__(
            'TrendFollowing04',
            '0.0.1',
            exchange=exchange,
            symbol=symbol,
            timeframe=timeframe
        )

    def update_exit(self):
        """
        submits a stop order as the new take-profit order. used to exit on trend reversals
        """
        if self.is_long:
            exit_price = self.price - self.atr * self.hp['stop_loss_atr_rate']
            exit_price = round(exit_price, 2)

            # exiting SECOND half of the position
            if self.is_reduced:
                self.take_profit = abs(self.position.qty), exit_price
            # exiting FIRST half of the position
            else:
                if ((exit_price < self.position.entry_price) and (
                        exit_price > self.average_stop_loss)) or exit_price > self.position.entry_price:
                    self.stop_loss = abs(self.position.qty), exit_price

        if self.is_short:
            exit_price = self.price + self.atr * self.hp['stop_loss_atr_rate']
            exit_price = round(exit_price, 2)

            # exiting SECOND half of the position
            if self.is_reduced:
                self.take_profit = abs(self.position.qty), exit_price
            # exiting FIRST half of the position
            else:
                if ((exit_price > self.position.entry_price) and (
                        exit_price < self.average_stop_loss)) or exit_price < self.position.entry_price:
                    self.stop_loss = abs(self.position.qty), exit_price

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

        return False

    def go_short(self):
        entry = self.low - (self.atr * 0.3)
        stop = self.high + self.atr * self.hp['stop_loss_atr_rate']
        qty = utils.risk_to_qty(self.balance, 6, entry, stop)
        qty = round(qty, 2)
        risk = abs(entry - stop)
        reduce_at = entry - risk * self.hp['take_profit_rate']
        margin = abs(entry - reduce_at)

        self.sell = qty, round(entry, 2)
        self.stop_loss = qty, round(stop, 2)
        self.take_profit = [
            (qty / 2, round(reduce_at, 2)),
            (qty / 2, round(reduce_at - margin, 2))
        ]

    def go_long(self):
        entry = self.high + (self.atr * 0.3)
        stop = self.low - self.atr * self.hp['stop_loss_atr_rate']
        qty = utils.risk_to_qty(self.balance, 6, entry, stop)
        qty = round(qty, 2)
        risk = abs(entry - stop)
        reduce_at = entry + risk * self.hp['take_profit_rate']
        margin = abs(entry - reduce_at)

        self.buy = qty, round(entry, 2)
        self.stop_loss = qty, round(stop, 2)
        self.take_profit = [
            (qty / 2, round(reduce_at, 2)),
            (qty / 2, round(reduce_at + margin, 2))
        ]

    def on_reduced_position(self):
        self.update_exit()

    def update_position(self):
        self.update_exit()

    def should_cancel(self):
        return True

    def watch_list(self):
        return [
            ('trend', self.symbol_momentum),
            ('EMA{} {} {}'.format(self.hp['longer_EMA'], self.symbol, self.timeframe), self.longer_EMA),
            ('EMA{} {} {}'.format(self.hp['long_EMA'], self.symbol, self.timeframe), self.long_EMA),
            ('SRSI K {} {}'.format(self.symbol, self.timeframe), self.stoch),
        ]

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

        short = ta.ema(self.get_candles(self.exchange, symbol, '1D'), self.hp['daily_short_EMA'])
        long = ta.ema(self.get_candles(self.exchange, symbol, '1D'), self.hp['daily_long_EMA'])
        longer = ta.ema(self.get_candles(self.exchange, symbol, '1D'), self.hp['daily_longer_EMA'])

        if short > long and long > longer:
            return 1
        elif short < long and long < longer:
            return -1
        else:
            return 0

    @property
    def btc_momentum(self):
        symbol = 'BTCUSD' if self.exchange == 'Bitfinex' else 'BTCUSDT'

        short = ta.ema(self.get_candles(self.exchange, symbol, utils.anchor_timeframe(self.timeframe)),
                       self.hp['anchor_short_EMA'])
        long = ta.ema(self.get_candles(self.exchange, symbol, utils.anchor_timeframe(self.timeframe)),
                      self.hp['anchor_long_EMA'])

        if short > long:
            return 1
        elif short < long:
            return -1
        else:
            return 0

    @property
    def symbol_momentum(self):
        short = ta.ema(self.get_candles(self.exchange, self.symbol, utils.anchor_timeframe(self.timeframe)),
                       self.hp['anchor_short_EMA'])
        long = ta.ema(self.get_candles(self.exchange, self.symbol, utils.anchor_timeframe(self.timeframe)),
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
        return ta.ema(self.candles, self.hp['long_EMA'])

    @property
    def longer_EMA(self):
        return ta.ema(self.candles, self.hp['longer_EMA'])

    @property
    def EMA_200(self):
        return ta.ema(self.candles, 200)

    @property
    def short_EMA(self):
        return ta.ema(self.candles, self.hp['short_EMA'])

    @property
    def shorter_EMA(self):
        return ta.ema(self.candles, self.hp['shorter_EMA'])

    @property
    def stoch(self):
        k, d = ta.srsi(self.candles)
        return k

    @property
    def atr(self):
        return ta.atr(self.candles)

    # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # filters
    # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    def filters(self):
        return [
            self.filter_1,
            self.filter_3,
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

    def filter_3(self) -> bool:
        return (abs(self.longer_EMA - self.long_EMA) / self.price) * 100 > self.hp['min_distance_between_EMAs']

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
            {'name': 'take_profit_rate', 'type': float, 'min': 1.0, 'max': 3.0},
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
    'take_profit_rate': 1.5,
}
