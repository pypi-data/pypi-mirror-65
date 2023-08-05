from load_and_update_data.get_fund_data import DataLoader
import pandas as pd
import numpy as np
import numpy as np
import matplotlib as mpl
import pylab as pl
import copy

import matplotlib.pyplot as plt
import matplotlib.cm as cm
import matplotlib.colors as colors
mpl.rcParams['font.family'] = ['SimHei']

YEAR = 242
T = 20 

# reserve
RESERVE = 0.1
ADJUSTED = 0.02

# fee
FEE = 0.01
BUY = 'BUY'
SEL = 'SELL'
CASH_WAIT_DAY = 5
BUY_INT = 1
SEL_INT = -1

class BacktestInfo():
    
    def __init__(self,cash=None):
        self.cash = cash
        self.cash_wait_list = []
        self.cash_wait_list_new = []
        self.position = []
        self.position_history = {}
        self.trade_history = {}
        self.market_value_history = {}
        self.weights_history_v1 = []
        self.weights_history_v2 = {}
        self.order_list = []
        self.order_list_new = []
        self.cash_history = {}
        self.fee_history = {}
        self.fee_total = 0
        
class BtElm():

    def __init__(self,index_name=None,index_value=None,volume=0,date=None,cash=None,amount=None,wait_day=None,direction=None):
        self.index_name = index_name
        self.index_value = index_value
        self.volume = volume
        self.date = date
        self.cash = cash
        self.amount = amount
        self.wait_day = wait_day
        self.direction = direction
    
    def __str__(self):
        return f'<index={self.index_name} index_value={self.index_value} volume={self.volume}  amount={self.amount} cash={self.cash} wait_day={self.wait_day} >'

class BackTest:

    def __init__(self, dl=None, start_date='20050101'):
        if dl == None:
            dl = DataLoader('huangkejia', 'Huangkejia123456', database_name='quant_data')
        
        exchange_data = dl.get_data('exchange_rate').set_index('datetime')
        index_data = dl.get_data('active_asset_index').set_index('datetime').drop(['sp500rmb', 'dax30rmb', 'n225rmb', 'oil'],axis=1)
        index_data = index_data.join(exchange_data)
        index_data['sp500']  = index_data['sp500'] * index_data['USD_CFETS']
        index_data['dax30'] = index_data['dax30'] * index_data['EURO_CFETS']
        index_data['n225']= index_data['n225'] * index_data['YAN_CFETS']
        index_data = index_data.drop(['USD_CFETS','EURO_CFETS','YAN_CFETS','USD_MID_P','EURO_MID_P','YAN_MID_P', 'id'], axis=1)
        index_data.index = index_data.index.map(lambda x: x.strftime('%Y%m%d'))
        self.index_data = index_data
        self.date_list = index_data.loc[start_date:,].index.tolist()
        self.asset_list = index_data.columns.tolist()
    
    def v1(self, weights, name, picture=True):
        assets = list(weights.keys())
        bt_info = BacktestInfo(cash=1e8)
        for d in self.date_list:
            w_new = {}
            for a_i in assets:
                if self.index_data.loc[d,a_i] is None:
                    w_new[a_i] = 0
                else:
                    w_new[a_i] = weights[a_i]
            s =  sum(list(w_new.values()))
            w_new = {k : v / s for k, v in w_new.items()}     
        
            # build portfolio
            if self.date_list.index(d) == 0:
                for a in self.asset_list:
                    if  w_new[a] == 0:
                        continue
                    i = self.index_data.loc[d,a]
                    v = bt_info.cash * w_new[a] / i
                    pos = BtElm(index_name=a,date=d,index_value=i,volume = v, amount = v*i)
                    bt_info.position.append(pos) 

            else:
                # reblance 
                # update position price and amount
                today_asset = [k for k, v in w_new.items() if v > 0]
                for a_name in today_asset:
                    pos = None
                    for pos_i in bt_info.position:
                        if pos_i.index_name == a_name:
                            pos = pos_i
                    if pos == None:
                        pos = BtElm(index_name=a_name, volume=0,amount=0)
                        bt_info.position.append(pos) 

                    pos_i.index_value = self.index_data.loc[d, pos_i.index_name] 
                    pos_i.amount = pos_i.index_value * pos_i.volume

                if self.judge_switch(d, self.date_list, T):
                    
                    total_amount = sum([pos_i.amount for pos_i in bt_info.position if pos_i.volume >0])
                    #d_last = date_list(date_list.index(d) - 1)

                    for pos_i in bt_info.position:  
                        target_amount = total_amount * w_new[pos_i.index_name]
                        pos_i.amount = target_amount
                        pos_i.volume = target_amount / self.index_data.loc[d, pos_i.index_name] 

            
            #update position history and market value
            for pos_i in bt_info.position:
                pos_i.index_value = self.index_data.loc[d, pos_i.index_name] 
                pos_i.amount = pos_i.index_value * pos_i.volume
            
            bt_info.position_history[d] = [copy.deepcopy(pos_i) for pos_i in bt_info.position if pos_i.volume >0]
            bt_info.market_value_history[d] = sum([ pos.amount for pos in bt_info.position_history[d]]) 

            weights_i = { pos_i.index_name: pos_i.amount/ bt_info.market_value_history[d] for pos_i in bt_info.position}
            weights_i['date'] = d
            bt_info.weights_history_v1.append(weights_i)


        weights_df = pd.DataFrame(bt_info.weights_history_v1).set_index('date')
        if picture:
            weights_df.plot.area(figsize=(18,9),legend=False,fontsize = 13)
            l = pl.legend(loc='lower left',fontsize = 13)
            s = pl.title('asset allocation', fontsize=20)

        mv_df = pd.DataFrame([ {'date':k, 'mv':v} for k,v in bt_info.market_value_history.items()]).set_index('date')
        if picture:
            mv_df.plot.line(figsize=(18,9),legend=False,fontsize = 13)
            l = pl.legend(loc='lower left',fontsize = 13)
            s = pl.title('market value', fontsize=20)


        year = len(self.date_list)/YEAR
        total_return = mv_df['mv'][-1] / mv_df['mv'][0]
        annualized_return = np.exp(np.log(total_return)/year) - 1
        annualized_volatiltity = (mv_df['mv'].shift(1) / mv_df['mv']).std() * np.sqrt((len(self.date_list) - 1) / year)
        sharpe = annualized_return / annualized_volatiltity
        mdd = 1 - (mv_df.loc[:, 'mv'] / mv_df.loc[:, 'mv'].rolling(10000, min_periods=1).max()).min()
        mv_df['date'] = mv_df.index
        mdd_part1 = (mv_df.loc[:, 'mv'] / mv_df.loc[:, 'mv'].rolling(10000, min_periods=1).max())
        mdd_date1 = mv_df.loc[mv_df.loc[:mdd_part1.idxmin(),'mv'].idxmax(),'date']
        mdd_date2 = mv_df.loc[mdd_part1.idxmin(),'date']
        # print(f'totol return : {total_return}')
        # print(f'annualized return : {annualized_return}')
        # print(f'annualized volatiltity : {annualized_volatiltity}')
        # print(f'sharpe : {sharpe}')
        # print(f'max draw down: {mdd} start {mdd_date1} end {mdd_date2} ')
        
        df = mv_df.set_index('date').join(self.index_data[[k for k, v in w_new.items() if v > 0]]).fillna(method='bfill')
        if picture:
            (df /df.iloc[0]).plot.line(figsize=(18,9),legend=False,fontsize = 13)
            l = pl.legend(loc='lower left',fontsize = 13)
            s = pl.title('mv', fontsize=20)
        w_new['annualized_return'] = annualized_return
        w_new['annualized_volatiltity'] = annualized_volatiltity
        w_new['sharpe'] = sharpe
        w_new['mdd'] = mdd
        w_new['mdd_start'] = mdd_date1
        w_new['mdd_end'] = mdd_date2
        w_new['name'] = name
        
        if picture:
            self.plot_mv(self.index_data.loc[mdd_date1:mdd_date2,], self.index_data.columns.tolist(), '全资产最大回撤时净值')
        
        return w_new
    
    def v2(self, weights, picture=True):
        # dynamic
        switch_day = [ _ for _ in self.date_list if self.date_list.index(_) % T == 0]
        res = []
        for _ in switch_day:
            weights['date'] = _
            res.append(weights.copy())
        w_df = pd.DataFrame(res).set_index('date')

        bt_info = BacktestInfo(cash=1e8)


        for d in self.date_list:
            # print(f'--{d}--')

            #update order list
            ## find recent target weights
            ## get asset position
            ## get total amount and cash
            # update cash info, if wait day = 1, cash received 
            for c_i in bt_info.cash_wait_list:  
                if c_i.wait_day >1:
                    c_i.wait_day -= 1
                    bt_info.cash_wait_list_new.append(c_i)
                else:
                    bt_info.cash += c_i.cash
                    # print(f'cash receive {c_i.cash} total cash {bt_info.cash} ')
            bt_info.cash_wait_list = bt_info.cash_wait_list_new.copy()
            bt_info.cash_wait_list_new = []
            
            if d in switch_day:
                # build portfolio on the first day
                if switch_day.index(d) == 0:
                    w_d = w_df.loc[d,:].to_dict()
                    for a in self.asset_list:
                        i = self.index_data.loc[d,a]
                        w_i = bt_info.cash * (1-RESERVE) * w_d[a] 
                        v = w_i/ i
                        if v == 0:
                            continue
                        t = BtElm(index_name=a,date=d,volume = v,amount=w_i/bt_info.cash)
                        #print(f'order : {t}')
                        bt_info.order_list.append(t)

                # reblance    
                else:
                    
                    last_d = self.date_list[self.date_list.index(d) - 1]
                    last_w = bt_info.weights_history_v2[last_d]
                    last_mv = bt_info.market_value_history[last_d]
                    w_d = w_df.loc[d,:].to_dict()
                    
                    total_value = last_mv * (1 - RESERVE) 

                    for pos_i in bt_info.position:  
                        target_amount = total_value*w_d[pos_i.index_name]
                        diff_value = target_amount - pos_i.amount
                        trade_v = diff_value / self.index_data.loc[d, pos_i.index_name] /(1+FEE*self.get_sign(diff_value))
                        t = BtElm(index_name=pos_i.index_name,date=d,volume = trade_v)
                        bt_info.order_list.append(t)
                        #print(f'order : {t}')
            
            # trade  
            bt_info.trade_history[d] = []
            bt_info.fee_history[d] = {}
            
            for t_i in bt_info.order_list:
                ## check if pos info exised else create new one 
                pos = None
                for pos_i in bt_info.position:
                    if pos_i.index_name == t_i.index_name:
                        pos = pos_i
                if pos == None:
                    pos = BtElm(index_name=t_i.index_name, volume=0,amount=0)
                    bt_info.position.append(pos) 

                ## trade process: update cash and pos volume
                ## buy sign == 1    sel sign == -1
                sign = self.get_sign(t_i.volume)
                
                ## if have cash more than RESERVE RATE trade, else buy on next day
                posi_amount = sum([_.amount for _ in bt_info.position if _.amount >= 0]) 
                        
                cash_rate = bt_info.cash /(posi_amount + bt_info.cash)
                
                if cash_rate <=  (RESERVE - ADJUSTED) and sign == BUY_INT:
                    # print(f'not enough cash {t_i} cash_rate {cash_rate}')
                    bt_info.order_list_new.append(t_i)
                    continue
                
                direc = BUY if sign > 0 else SEL
                index_v = self.index_data.loc[d, t_i.index_name] 
                a_book = t_i.volume * index_v
                a_real = t_i.volume * index_v * (1+ (sign* FEE))
                bt_info.fee_history[d][t_i.index_name] =    t_i.volume * index_v *(sign* FEE)
                bt_info.fee_total += t_i.volume * index_v *(sign* FEE)
                pos.volume += t_i.volume
                pos.amount += a_book
                
                ## if buy, cash decrease immediately
                ## if sel, cash save in wait list
                if sign == BUY_INT:
                    bt_info.cash -= a_real
                elif sign == SEL_INT:
                    c_i = BtElm(cash=-a_real,wait_day=CASH_WAIT_DAY)
                    
                    bt_info.cash_wait_list.append(c_i)
                                
                ## update trade history
                t = BtElm(index_name=t_i.index_name,volume=abs(t_i.volume),direction=direc,date=d,index_value=index_v,amount=a_book)
                # print(f'trade : {t}')
                bt_info.trade_history[d].append(t)
            
            bt_info.order_list = bt_info.order_list_new.copy()
            bt_info.order_list_new = []
                
            
            ## update position fund unit_net_value and amount
            for pos_i in bt_info.position:
                pos_i.index_value = self.index_data.loc[d, pos_i.index_name] 
                pos_i.amount = pos_i.index_value * pos_i.volume
            
            #update position history and market value
            bt_info.position_history[d] = [copy.deepcopy(pos_i) for pos_i in bt_info.position if pos_i.volume >0]
            bt_info.market_value_history[d] = sum([ pos.amount for pos in bt_info.position_history[d]]) + bt_info.cash

            weights_i = { pos_i.index_name: pos_i.amount/ bt_info.market_value_history[d] for pos_i in bt_info.position}
            weights_i['date'] = d

            bt_info.weights_history_v2[d] = weights_i
            bt_info.cash_history[d] = bt_info.cash
        
        df = pd.DataFrame.from_dict(bt_info.weights_history_v2, orient='index')
        df['new_date'] = df['date'].apply(lambda x: x[:4]+ x[5:7] + x[8:])
        weights_df = df.set_index('new_date').drop(columns=['date'])
        if picture:
            weights_df.plot.area(figsize=(18,9),legend=False,fontsize = 13)
            l = pl.legend(loc='lower left',fontsize = 13)
            s = pl.title('asset allocation', fontsize=20)
        
        mv_df = pd.DataFrame([ {'date':k, 'mv':v} for k,v in bt_info.market_value_history.items()]).set_index('date')
        if picture:
            mv_df.plot.line(figsize=(18,9),legend=False,fontsize = 13)
            l = pl.legend(loc='lower left',fontsize = 13)
            s = pl.title('market value', fontsize=20)


        year = len(self.date_list)/YEAR
        total_return = mv_df['mv'][-1] / mv_df['mv'][0]
        five_year_return = mv_df['mv'][-1] / mv_df['mv'][-(5 * YEAR)]
        annualized_return = np.exp(np.log(total_return)/year) - 1
        annualized_volatiltity = (mv_df['mv'].shift(1) / mv_df['mv']).std() * np.sqrt((len(self.date_list) - 1) / year)
        sharpe = annualized_return / annualized_volatiltity
        mdd = 1 - (mv_df.loc[:, 'mv'] / mv_df.loc[:, 'mv'].rolling(10000, min_periods=1).max()).min()
        mv_df['date'] = mv_df.index
        mdd_part1 = (mv_df.loc[:, 'mv'] / mv_df.loc[:, 'mv'].rolling(10000, min_periods=1).max())
        mdd_date1 = mv_df.loc[mv_df.loc[:mdd_part1.idxmin(),'mv'].idxmax(),'date']
        mdd_date2 = mv_df.loc[mdd_part1.idxmin(),'date']
        # print(f'totol return : {total_return}')
        # print(f'annualized return : {annualized_return}')
        # print(f'annualized volatiltity : {annualized_volatiltity}')
        # print(f'sharpe : {sharpe}')
        # print(f'max draw down: {mdd} start {mdd_date1} end {mdd_date2} ')
        weights.pop('date', None)
        df = mv_df.set_index('date').join(self.index_data[[k for k, v in weights.items() if float(v) > 0]])
        if picture:
            (df /df.iloc[0]).plot.line(figsize=(18,9),legend=False,fontsize = 13)
            l = pl.legend(loc='lower left',fontsize = 13)
            s = pl.title('mv', fontsize=20)

        w_new = {}
        w_new['annualized_return'] = annualized_return
        w_new['five_year_return'] = five_year_return
        w_new['annualized_volatiltity'] = annualized_volatiltity
        w_new['sharpe'] = sharpe
        w_new['mdd'] = mdd
        w_new['mdd_start'] = mdd_date1
        w_new['mdd_end'] = mdd_date2
    
        if picture:
            self.plot_mv(self.index_data.loc[mdd_date1:mdd_date2,], self.index_data.columns.tolist(), '全资产最大回撤时净值')
        
        return w_new

    
    @staticmethod
    def judge_switch(d, date_list, T):
        if date_list.index(d) % T == 0:
            return True
        return False

    @staticmethod
    def plot_mv(index_data, col_list, name):
        df = index_data[col_list].fillna(method='bfill')
        (df /df.iloc[0]).plot.line(figsize=(18,9),legend=False,fontsize = 13)
        l = pl.legend(loc='lower left',fontsize = 13)
        s = pl.title(name, fontsize=20)
    
    @staticmethod
    def get_sign(x):
        return int(x > 0) * 2 - 1