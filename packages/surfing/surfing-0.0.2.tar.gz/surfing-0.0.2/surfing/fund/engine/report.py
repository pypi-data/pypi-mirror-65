import pandas as pd
import numpy as np
import datetime
import copy
from pprint import pprint 
import matplotlib as mpl
import pylab as pl
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import matplotlib.colors as colors
mpl.rcParams['font.family'] = ['Heiti TC']

from ...data.manager.manager_fund import FundDataManager
from ...data.struct import AssetWeight, AssetPosition, AssetPrice, AssetValue
class BacktestInfo:
    
    '''
    save backtest history
    '''
    TRADING_DAYS_PER_YEAR = 242

    def __init__(self):
        pass

    def init(self):
        pass    

    def setup(self, saa: AssetWeight):
        self.saa_weight = saa.__dict__
        self.cash_history = {}
        self.position_history = {}
        self.market_price_history = {}
        self.pending_trade_history = {}
        self.weights_history = {}
        self.tactic_history = {}
        self.trade_history = {}
        self.rebalance_date = []
    
    def update(self, dt: datetime, cur_position:AssetPosition,cur_price:AssetPrice,pend_trades: list ):   
        self.cash_history[dt] = cur_position.cash
        self.position_history[dt] = cur_position.__dict__
        self.market_price_history[dt] = AssetValue(prices=cur_price, positions=cur_position).sum()
        self.pending_trade_history[dt] = pend_trades
        self.weights_history[dt] = AssetValue(prices=cur_price, positions=cur_position).get_weight()
        #self.tactic_history[dt] = 
        #self.trade_history[dt] = 
        #self.rebalance_date.append()      

    def result(self):
        self.mv_df = pd.DataFrame([ {'date':k, 'mv':v} for k,v in self.market_price_history.items()]).set_index('date')
        year = self.mv_df.shape[0]/self.TRADING_DAYS_PER_YEAR
        total_return = self.mv_df['mv'][-1] / self.mv_df['mv'][0]
        try:
            five_year_return = (self.mv_df['mv'][-1] / self.mv_df['mv'][-(5 * self.TRADING_DAYS_PER_YEAR)] - 1)
        except:
            five_year_return = five_year_return = (self.mv_df['mv'][-1] / self.mv_df['mv'][0] - 1)
        annualized_return = np.exp(np.log(total_return)/year) - 1
        annualized_volatiltity = (self.mv_df['mv'].shift(1) / self.mv_df['mv']).std() * np.sqrt((self.mv_df.shape[0] - 1) / year)
        sharpe = annualized_return / annualized_volatiltity
        mdd = 1 - (self.mv_df.loc[:, 'mv'] / self.mv_df.loc[:, 'mv'].rolling(10000, min_periods=1).max()).min()
        mdd_part1 = (self.mv_df.loc[:, 'mv'] / self.mv_df.loc[:, 'mv'].rolling(10000, min_periods=1).max())
        self.mdd_date1 = self.mv_df.loc[:mdd_part1.idxmin(),'mv'].idxmax()
        self.mdd_date2 = mdd_part1.idxmin()
        w = copy.deepcopy(self.saa_weight)
        w['mdd'] = mdd
        w['annual_ret'] = annualized_return
        w['sharpe'] = sharpe
        w['5_year_ret'] = five_year_return
        w['annual_vol'] = annualized_volatiltity
        w['mdd_d1'] = self.mdd_date1
        w['mdd_d2'] = self.mdd_date2
        pprint(w)
        return w
    
    def backtest_plot(self, index_df):
        self.plot_asset_weights()
        self.plot_market_value(index_df)
        self.plot_mdd_period_assets(index_df)

    def plot_asset_weights(self):
        res = []
        for k,v in self.weights_history.items():
            v = v.__dict__
            v['date'] = k
            res.append(v)
        weights_df = pd.DataFrame(res).set_index('date')
        weights_df = weights_df.drop(['cash'], axis = 1).dropna()[1:]
        res = []
        for dic, s in zip(weights_df.to_dict('records'), weights_df.sum(axis = 1).values):
            res.append({ k: v/ s for k, v in dic.items()})
        df = pd.DataFrame(res)
        df.index = weights_df.index
        df.plot.area(figsize=(18,9),legend=False,fontsize = 13)
        l = pl.legend(loc='lower left',fontsize = 9)
        s = pl.title('weights history', fontsize=20)

    def plot_market_value(self, index_df):    
        index_df_raw = index_df.loc[self.mv_df.index[0]:self.mv_df.index[-1],]
        index_df = index_df_raw.copy().fillna(method='bfill')
        index_df = index_df/index_df.iloc[0]
        w_l = []
        for idx, r in index_df_raw.iterrows():
            nan_asset = [k for k,v in r.to_dict().items() if np.isnan(v)]
            wgts = self.saa_weight.copy()
            wgts['cash'] = 0
            for k in nan_asset:
                wgts[k] = 0
            s = sum([v  for k,v in wgts.items()])
            wgts = {k :v /s for k, v in wgts.items()}
            wgts['datetime'] = idx
            w_l.append(wgts)
        wgts_df = pd.DataFrame(w_l).set_index('datetime').drop(['cash'], axis = 1)
        self.mv_df['benchmark'] = (wgts_df * index_df).sum(axis = 1)
        self.mv_df =self.mv_df / self.mv_df.iloc[0]
        self.mv_df.plot.line(figsize=(20,12),legend=False,fontsize = 13)
        l = pl.legend(loc='lower left',fontsize = 10)
        s = pl.title('market value', fontsize=20)

    def plot_mdd_period_assets(self, index_df): 
        l = list(self.saa_weight.keys())
        l.remove('cash')
        df = index_df[l].loc[self.mdd_date1:self.mdd_date2].fillna(method='bfill')
        (df /df.iloc[0]).plot.line(figsize=(18,9),legend=False,fontsize = 13)
        l = pl.legend(loc='lower left',fontsize = 13)
        s = pl.title('during mdd period  market value of all assets', fontsize=20)    