import datetime
import copy
import json
import numpy as np
import pandas as pd
import os

from .asset_helper import SAAHelper, TAAHelper
from .trader import AssetTrader, FundTrader
from .report import BacktestInfo
from ...data.manager.manager_fund import FundDataManager
from ...data.struct import AssetWeight, AssetPrice, AssetPosition, AssetValue
from ...data.struct import FundPosition, TAAParam, AssetTradeParam, FundTradeParam


class FundBacktestEngine:

    DEFAULT_CASH_VALUE = 1e8

    def __init__(self, data_manager: FundDataManager, trader, taa_params:TAAParam=None):
        self._dm = data_manager
        self._saa_helper = SAAHelper() # 战略目标
        self._taa_helper = TAAHelper(taa_params=taa_params) if taa_params else None
        self._report_helper = BacktestInfo()
        self._trader = trader

    @property
    def is_fund_backtest(self):
        return isinstance(self._trader, FundTrader)

    def init(self):
        if not self._dm.inited:
            self._dm.init()
        self._saa_helper.init()
        if self._taa_helper:
            self._taa_helper.init()
        self._report_helper.init()
        self._trader.init()

    def run(self, saa: AssetWeight, start_date: datetime.date=None, end_date: datetime.date=None, cash: float=None):
        cash = cash or self.DEFAULT_CASH_VALUE
        # init position
        self.cur_asset_position = AssetPosition(cash=cash)
        self.cur_fund_position = FundPosition(cash=cash)
        cur_asset_mv = AssetValue(prices=AssetPrice(cash=1), positions=self.cur_asset_position)
        print(cur_asset_mv)
        self._pending_trades = []

        # init days
        start_date = start_date or self._dm.start_date
        end_date = end_date or self._dm.end_date

        # setup helpers
        self._saa_helper.setup(saa)
        if self._taa_helper:
            self._taa_helper.setup(saa)
        self._report_helper.setup(saa)
        self._trader.setup(saa)

        # loop trading days
        _dts = self._dm.get_trading_days()
        dts = _dts[(_dts.datetime >= start_date) & (_dts.datetime <= end_date)].datetime # df with datetime.date
        for t in dts:
            self._run_on(t)
        
    def _run_on(self, dt):
        # current asset price
        cur_asset_price = self._dm.get_index_price_data(dt)
        if self.is_fund_backtest:
            fund_nav = self._dm.get_fund_nav(dt)
            fund_score = {index_id: self._dm.get_fund_score(dt, index_id) for index_id in self.cur_asset_position.__dict__.keys()}
            
        # finalize trades
        if self.is_fund_backtest:
            self._pending_trades = self._trader.finalize_trade(dt, self._pending_trades, cur_asset_price, self.cur_asset_position, self.cur_fund_position, fund_nav)
        else:
            self._pending_trades = self._trader.finalize_trade(dt, self._pending_trades, cur_asset_price, self.cur_asset_position)

        target_asset_allocation = self.calc_asset_allocation(dt, cur_asset_price)

        if self.is_fund_backtest:
            virtual_position, trade_list = self._trader.calc_fund_trade(dt, self.cur_asset_position, cur_asset_price, target_asset_allocation, self.cur_fund_position, fund_nav, fund_score)
        else:
            virtual_position, trade_list = self._trader.calc_asset_trade(dt, self.cur_asset_position, cur_asset_price, target_asset_allocation)
        if trade_list and len(trade_list) > 0:
            self.book_trades(trade_list)
        self._report_helper.update(dt, self.cur_asset_position, cur_asset_price, self._pending_trades)

    def calc_asset_allocation(self, dt, cur_asset_price: AssetPrice):
        cur_saa = self._saa_helper.on_price(dt, cur_asset_price)
        if self._taa_helper:
            asset_pct = self._dm.get_index_pcts(dt)
            cur_taa = self._taa_helper.on_price(dt, cur_asset_price, cur_saa, asset_pct)
        else:
            cur_taa = cur_saa
        return cur_taa

    def book_trades(self, trade_list: list):
        self._pending_trades += trade_list

    def report(self):
        result = self._report_helper.result()# backtest result
        index_df = self._dm.get_index_price()
        self._report_helper.backtest_plot(index_df)# backtest plot


def saa_backtest(m: FundDataManager, saa: AssetWeight):
    asset_param = AssetTradeParam() # type in here
    t = AssetTrader(asset_param)
    b = FundBacktestEngine(data_manager=m, trader=t, taa_params=None)
    b.init()
    b.run(saa=saa)

def taa_backtest(m: FundDataManager, saa: AssetWeight):
    taa_param = TAAParam()  # type in here
    asset_param = AssetTradeParam() # type in here
    t = AssetTrader(asset_param)
    b = FundBacktestEngine(data_manager=m, trader=t, taa_params=taa_param)
    b.init()
    b.run(saa=saa)

def fund_backtest_without_taa(m: FundDataManager, saa: AssetWeight):
    asset_param = AssetTradeParam() # type in here
    fund_param = FundTradeParam() # type in here
    t = FundTrader(asset_param, fund_param)
    b = FundBacktestEngine(data_manager=m, trader=t, taa_params=None)
    b.init()
    b.run(saa=saa)

def fund_backtest(m: FundDataManager, saa: AssetWeight):
    taa_param = TAAParam()  # type in here
    asset_param = AssetTradeParam() # type in here
    fund_param = FundTradeParam() # type in here
    t = FundTrader(asset_param, fund_param)
    b = FundBacktestEngine(data_manager=m, trader=t, taa_params=taa_param)
    b.init()
    b.run(saa=saa)


if __name__ == '__main__':
    m = FundDataManager('20150101', '20160101')
    m.init()

    saa = AssetWeight(
        hs300=15/100,
        csi500=5/100,
        gem=3/100,
        sp500rmb=7/100,
        national_debt=60/100,
        gold=10/100,
        cash=5/100
    )
    
    #saa_backtest(m, saa)
    #taa_backtest(m, saa)
    #fund_backtest_without_taa(m, saa)
    fund_backtest(m, saa)
