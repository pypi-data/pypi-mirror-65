import pandas as pd
import datetime
from ...data.struct import AssetWeight, AssetPosition, AssetPrice, AssetValue
from . import Helper

class BacktestInfo(Helper):
    
    '''
    save backtest history
    '''

    def __init__(self):
        pass
        
    def setup(self, saa: AssetWeight):
        self.saa_weight = saa
        self.cash_history = {}
        self.position_history = {}
        self.market_price_history = {}
        self.pending_trade_history = {}
        self.weights_history = {}
        self.tactic_history = {}
        self.trade_history = {}
        self.rebalance_date = []
    
    def update(self, dt: datetime, cur_position:AssetPosition,cur_price:AssetPrice,pend_trades: list ):   
        print('update : ', dt)
        self.cash_history[dt] = cur_position.cash
        self.position_history[dt] = cur_position.__dict__
        self.market_price_history[dt] = AssetValue(prices=cur_price, positions=cur_position).sum()
        self.pending_trade_history[dt] = pend_trades
        self.weights_history[dt] = {k: v/ self.market_price_history[dt]  for k, v in cur_position.__dict__.items()}
        #self.tactic_history[dt] = 
        #self.trade_history[dt] = 
        #self.rebalance_date.append()

    def dict_to_df(self, dic):
        # 回测信息格式由dict -> df, cash market_price
        return pd.DataFrame([{'datetime': k , 'value': v } for k, v in dic.items()])            
