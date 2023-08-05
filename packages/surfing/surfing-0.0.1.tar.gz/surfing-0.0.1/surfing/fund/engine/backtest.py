import datetime
import copy
import json
import numpy as np
import pandas as pd
import os

from .asset_helper import SAAHelper, TAAHelper
from .trader import AssetTrader
from .report import BacktestInfo
from ...data.manager.manager_fund import FundDataManager
from ...data.struct import AssetWeight, AssetPrice, AssetPosition, AssetValue


class FundBacktestEngine:

    def __init__(self, data_manager: FundDataManager):
        self._dm = data_manager
        self._saa_helper = SAAHelper() # 战略目标
        self._taa_helper = TAAHelper()
        self._report_helper = BacktestInfo()
        self._asset_trader = AssetTrader()

    def init(self):
        self._dm.init()
        self._saa_helper.init()
        self._taa_helper.init()
        self._report_helper.init()
        self._asset_trader.init()

    def run(self, saa: AssetWeight, start_date: datetime.date=None, end_date: datetime.date=None):
        # init position
        self.cur_asset_position = AssetPosition(cash=1e8)
        cur_asset_mv = AssetValue(prices=AssetPrice(cash=1), positions=self.cur_asset_position)
        print(cur_asset_mv)
        self._pending_trades = []

        # init days
        start_date = start_date or self._dm.start_date
        end_date = end_date or self._dm.end_date

        # setup helpers
        self._saa_helper.setup(saa)
        self._taa_helper.setup(saa)
        self._report_helper.setup(saa)
        self._asset_trader.setup(saa)

        # loop trading days
        _dts = self._dm.get_trading_days()
        dts = _dts[(_dts.datetime >= start_date) & (_dts.datetime <= end_date)].datetime # df with datetime.date
        for t in dts:
            self._run_on(t)
        
    def _run_on(self, dt):
        # current asset price
        cur_asset_price = self._dm.get_index_price_data(dt)
        self._pending_trades = self._asset_trader.finalize_trade(dt, self._pending_trades, cur_asset_price, self.cur_asset_position)
        target_asset_allocation = self.calc_asset_allocation(dt, cur_asset_price)

        virtual_position, trade_list = self._asset_trader.calc_trade(dt, self.cur_asset_position, cur_asset_price, target_asset_allocation)
        if trade_list and len(trade_list) > 0:
            self.book_trades(trade_list)
        self._report_helper.update(dt, self.cur_asset_position, cur_asset_price, self._pending_trades)

    def calc_asset_allocation(self, dt, cur_asset_price: AssetPrice):
        cur_saa = self._saa_helper.on_price(dt, cur_asset_price)
        asset_pct = self._dm.get_index_pcts(dt)
        cur_taa = self._taa_helper.on_price(dt, cur_asset_price, cur_saa, asset_pct)
        return cur_taa

    def book_trades(self, trade_list: list):
        self._pending_trades += trade_list


if __name__ == '__main__':
    m = FundDataManager('20100101', '20200101')
    saa = AssetWeight(
        hs300=15/100,
        csi500=5/100,
        gem=3/100,
        sp500rmb=7/100,
        national_debt=60/100,
        gold=10/100,
        cash=5/100
    )
    b = FundBacktestEngine(data_manager=m)
    b.init()
    b.run(saa=saa)