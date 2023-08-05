import jesse.utils as ju
from jesse.services.candle import candle_includes_price
from jesse.strategies import Strategy
from jesse.indicators import ema, srsi, atr
from jesse.services import logger

# hyper parameters
default_hp = {
    'min_pnl': 1,
    'max_risk': 20,
    'min_R': 1,
    'max_R': 5,
    'small_ema_1': 8,
    'small_ema_2': 13,
    'small_ema_3': 21,
    'big_ema_1': 8,
    'big_ema_2': 21,
    'oversold_level': 20,
    'overbought_level': 80,
}


class TrendScalping01(Strategy):
    def __init__(self, exchange, symbol, timeframe, hyper_parameters=None):
        super().__init__('TrendScalping01', '0.1.0', exchange, symbol, timeframe)

        if hyper_parameters is None:
            self.hp = default_hp
        else:
            self.hp = hyper_parameters

        self.vars['trigger_candle'] = None

    def prepare(self):
        if self.position.is_close and self.vars['trigger_candle'] is None:
            # long
            if self.big_trend == 1 and self.small_trend == 1:
                if candle_includes_price(self.current_candle, self.ema1) and not candle_includes_price(
                        self.current_candle, self.ema3):
                    self.vars['trigger_candle'] = self.current_candle
                    return
            self.vars['trigger_candle'] = None

            # short
            if self.big_trend == -1 and self.small_trend == -1:
                if candle_includes_price(self.current_candle, self.ema1) and not candle_includes_price(
                        self.current_candle, self.ema3):
                    self.vars['trigger_candle'] = self.current_candle
                    return
            self.vars['trigger_candle'] = None

    def on_open_position(self):
        self.vars['trigger_candle'] = None

    def on_cancel(self):
        self.vars['trigger_candle'] = None

    def on_reduced_position(self):
        logger.info('Moving stop-loss to break even...')

        self.stop_loss = abs(self.position.qty), self.position.entry_price

    def should_long(self):
        if self.small_trend != 1 or self.big_trend != 1:
            return False

        if self.vars['trigger_candle'] is not None and self.is_over_sold:
            return True

        return False

    def should_short(self):
        if self.small_trend != -1 or self.big_trend != -1:
            return False

        if self.vars['trigger_candle'] is not None and self.is_over_bought:
            return True

        return False

    def go_long(self):
        last_bars = self.candles[-4:]
        entry = last_bars[:, 3].max()

        stop = entry - 2 * self.atr
        qty = round(ju.risk_to_qty(self.capital, 6, entry, stop), 2)
        margin = abs(entry - stop)
        reduce_at = entry + margin
        take_profit = reduce_at + margin

        self.buy = qty, round(entry, 2)
        self.stop_loss = qty, round(stop, 2)
        self.take_profit = [
            (qty / 2, round(reduce_at, 2)),
            (qty / 2, round(take_profit, 2)),
        ]

    def go_short(self):
        last_bars = self.candles[-4:]
        entry = last_bars[:, 4].min()

        stop = entry + 2 * self.atr
        qty = round(ju.risk_to_qty(self.capital, 6, entry, stop), 2)
        margin = abs(entry - stop)
        reduce_at = entry - margin
        take_profit = reduce_at - margin

        self.sell = qty, round(entry, 2)
        self.stop_loss = qty, round(stop, 2)
        self.take_profit = [
            (qty / 2, round(reduce_at, 2)),
            (qty / 2, round(take_profit, 2)),
        ]

    def should_cancel(self):
        if self.vars['trigger_candle'] is not None:
            if candle_includes_price(self.current_candle, self.ema3):
                return True

        return False

    # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # indicators
    # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    @property
    def stoch(self):
        k, d = srsi(self.candles)
        return k

    @property
    def atr(self):
        return atr(self.candles)

    @property
    def is_over_bought(self):
        return self.stoch > self.hp['overbought_level']

    @property
    def is_over_sold(self):
        return self.stoch < self.hp['oversold_level']

    @property
    def ema1(self):
        return ema(self.candles, self.hp['small_ema_1'])

    @property
    def ema2(self):
        return ema(self.candles, self.hp['small_ema_2'])

    @property
    def ema3(self):
        return ema(self.candles, self.hp['small_ema_3'])

    @property
    def big_trend(self):
        ema1 = ema(self.get_candles(self.exchange, self.symbol, ju.anchor_timeframe(self.timeframe)),
                   self.hp['big_ema_1'])
        ema2 = ema(self.get_candles(self.exchange, self.symbol, ju.anchor_timeframe(self.timeframe)),
                   self.hp['big_ema_2'])

        if ema1 < ema2:
            return -1
        if ema1 > ema2:
            return 1
        return 0

    @property
    def small_trend(self):
        ema1 = ema(self.candles, self.hp['small_ema_1'])
        ema2 = ema(self.candles, self.hp['small_ema_2'])
        ema3 = ema(self.candles, self.hp['small_ema_3'])

        if (ema1 < ema2) and (ema2 < ema3):
            return -1
        if (ema1 > ema2) and (ema2 > ema3):
            return 1
        return 0

    # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # filters
    # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    def filters(self):
        return [
            self.filter_1,
            self.filter_2
        ]

    def filter_1(self) -> bool:
        """
        Reward/Risk ratio (R) must worth it
        """
        risk_per_qty = abs(self.average_entry_price - self.average_stop_loss)
        reward_per_qty = abs(self.average_take_profit - self.average_entry_price)

        R = abs(reward_per_qty / risk_per_qty)
        return (R > self.hp['min_R']) and (R < self.hp['max_R'])

    def filter_2(self):
        reward_per_qty = abs(self.average_take_profit - self.average_entry_price)

        if (reward_per_qty / self.average_entry_price) * 100 < self.hp['min_pnl']:
            return False

        return True
