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

mpl.rcParams['font.family'] = ['Heiti TC']



username = 'huangkejia'
password = 'Huangkejia123456'
database = 'quant_data'

dl = DataLoader(username, password, database_name=database)
index_data = dl.get_data('active_asset_index').set_index('date').drop(['标普500','德标30','日经225'],axis = 1).fillna(method= 'ffill')
date_list = index_data.loc['20050101':,].index.tolist()
asset_list = index_data.columns.tolist()
YEAR = 242
T = 20 

class IndexData():
    
    '''
    asset allocation cleaned data
    '''

class BacktestInfo():
    
    '''
    save backtest history
    '''

    def __init__(self,cash=None,period=None,top=None):
        self.index_cash       = cash
        self.index_position   = []
        self.index_position_history     = {}
        self.index_market_value_history = {}
        self.index_weights_history = []
        
class BtElm():

    '''
    memory element of backtest info, include trade cash position market_value 
    '''

    def __init__(self,index_name=None,index_value=None,volume=0,date=None,cash=None,amount=None):
        self.index_name = index_name
        self.index_value = index_value
        self.volume = volume
        self.date = date
        self.cash = cash
        self.amount = amount
    
    def __str__(self):
        return f'<index={self.index_name} index_value={self.index_value} volume={self.volume}  amount={self.amount}>'
    

def judge_switch(d, date_list, T):
    if date_list.index(d) % T == 0:
        return True
    return False

def check_position(bt_info):
    for i in bt_info.position:
        print(i)
        
def plot_mv(index_data, col_list, name):
    df = index_data[col_list].loc['20150101':,].fillna(method='bfill')
    (df /df.iloc[0]).plot.line(figsize=(18,9),legend=False,fontsize = 13)
    l = pl.legend(loc='lower left',fontsize = 13)
    s = pl.title(name, fontsize=20)
        
def asset_allocation(Weights, name):    
    assets = list(Weights.keys())
    bt_info = BacktestInfo(cash=1e8)
    for d in date_list:
        w_new = {}
        for a_i in assets:
            if np.isnan(index_data.loc[d,a_i]):
                w_new[a_i] = 0
            else:
                w_new[a_i] = Weights[a_i]
        s =  sum(list(w_new.values()))
        w_new = {k : v / s for k, v in w_new.items()}     
    
        # build portfolio
        if date_list.index(d) == 0:
            for a in asset_list:
                if  w_new[a] == 0:
                    continue
                i = index_data.loc[d,a]
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

                pos_i.index_value = index_data.loc[d, pos_i.index_name] 
                pos_i.amount = pos_i.index_value * pos_i.volume

            if judge_switch(d, date_list, T):
                
                total_amount = sum([pos_i.amount for pos_i in bt_info.position if pos_i.volume >0])
                #d_last = date_list(date_list.index(d) - 1)

                for pos_i in bt_info.position:  
                    target_amount = total_amount * w_new[pos_i.index_name]
                    pos_i.amount = target_amount
                    pos_i.volume = target_amount / index_data.loc[d, pos_i.index_name] 

        
        #update position history and market value
        for pos_i in bt_info.position:
            pos_i.index_value = index_data.loc[d, pos_i.index_name] 
            pos_i.amount = pos_i.index_value * pos_i.volume
        
        bt_info.position_history[d] = [copy.deepcopy(pos_i) for pos_i in bt_info.position if pos_i.volume >0]
        bt_info.market_value_history[d] = sum([ pos.amount for pos in bt_info.position_history[d]]) 

        weights_i = { pos_i.index_name: pos_i.amount/ bt_info.market_value_history[d] for pos_i in bt_info.position}
        weights_i['date'] = d
        bt_info.weights_history.append(weights_i)




def plot():
    weights_df = pd.DataFrame(bt_info.weights_history).set_index('date')
#     weights_df.plot.area(figsize=(18,9),legend=False,fontsize = 13)
#     l = pl.legend(loc='lower left',fontsize = 13)
#     s = pl.title('asset allocation', fontsize=20)

    mv_df = pd.DataFrame([ {'date':k, 'mv':v} for k,v in bt_info.market_value_history.items()]).set_index('date')
    mv_df.plot.line(figsize=(18,9),legend=False,fontsize = 13)
    l = pl.legend(loc='lower left',fontsize = 13)
    s = pl.title('market value', fontsize=20)
    five_year_return = mv_df['mv'][-1] / mv_df['mv'][-(5 * YEAR)]
    
    year = len(date_list)/YEAR
    total_return = (mv_df['mv'][-1] / mv_df['mv'][0])-1
    annualized_return = np.exp(np.log(total_return)/year) - 1
    annualized_volatiltity = (mv_df['mv'].shift(1) / mv_df['mv']).std() * np.sqrt((len(date_list) - 1) / year)
    sharpe = annualized_return / annualized_volatiltity
    mdd = 1 - (mv_df.loc[:, 'mv'] / mv_df.loc[:, 'mv'].rolling(10000, min_periods=1).max()).min()
    mv_df['date'] = mv_df.index
    mdd_part1 = (mv_df.loc[:, 'mv'] / mv_df.loc[:, 'mv'].rolling(10000, min_periods=1).max())
    mdd_date1 = mv_df.loc[mv_df.loc[:mdd_part1.idxmin(),'mv'].idxmax(),'date']
    mdd_date2 = mv_df.loc[mdd_part1.idxmin(),'date']
    print(f'totol return : {total_return}')
    print(f'annualized return : {annualized_return}')
    print(f'annualized volatiltity : {annualized_volatiltity}')
    print(f'sharpe : {sharpe}')
    print(f'max draw down: {mdd} start {mdd_date1} end {mdd_date2} ')
    print(f'recent five year : {five_year_return}')
    
    df = mv_df.set_index('date').join(index_data[[k for k, v in w_new.items() if v > 0]]).fillna(method='bfill')
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
    w_new['five_year_return'] = five_year_return

    plot_mv(index_data.loc[mdd_date1:mdd_date2,], index_data.columns.tolist(), '全资产最大回撤时净值')    
    return w_new


# search grid with simply asset allocation backtest
def search_grid(Weights):
    assets = list(Weights.keys())
    bt_info = BacktestInfo(cash=1e8)
    for d in date_list:
        w_new = {}
        for a_i in assets:
            if np.isnan(index_data.loc[d,a_i]):
                w_new[a_i] = 0
            else:
                w_new[a_i] = Weights[a_i]
        s =  sum(list(w_new.values()))
        w_new = {k : v / s for k, v in w_new.items()}     
    
        # build portfolio
        if date_list.index(d) == 0:
            for a in asset_list:
                if  w_new[a] == 0:
                    continue
                i = index_data.loc[d,a]
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

                pos_i.index_value = index_data.loc[d, pos_i.index_name] 
                pos_i.amount = pos_i.index_value * pos_i.volume

            if judge_switch(d, date_list, T):
                
                total_amount = sum([pos_i.amount for pos_i in bt_info.position if pos_i.volume >0])
                #d_last = date_list(date_list.index(d) - 1)

                for pos_i in bt_info.position:  
                    target_amount = total_amount * w_new[pos_i.index_name]
                    pos_i.amount = target_amount
                    pos_i.volume = target_amount / index_data.loc[d, pos_i.index_name] 

        
        #update position history and market value
        for pos_i in bt_info.position:
            pos_i.index_value = index_data.loc[d, pos_i.index_name] 
            pos_i.amount = pos_i.index_value * pos_i.volume
        
        pos_his = [copy.deepcopy(pos_i) for pos_i in bt_info.position if pos_i.volume >0]
        bt_info.market_value_history[d] = sum([ pos.amount for pos in pos_his]) 

        weights_i = { pos_i.index_name: pos_i.amount/ bt_info.market_value_history[d] for pos_i in bt_info.position}
        weights_i['date'] = d
        #bt_info.weights_history.append(weights_i)

    mv_df = pd.DataFrame([ {'date':k, 'mv':v} for k,v in bt_info.market_value_history.items()]).set_index('date')
    year = len(date_list)/YEAR
    total_return = mv_df['mv'][-1] / mv_df['mv'][0]
    five_year_return = (mv_df['mv'][-1] / mv_df['mv'][-(5 * YEAR)] - 1)
    annualized_return = np.exp(np.log(total_return)/year) - 1
    annualized_volatiltity = (mv_df['mv'].shift(1) / mv_df['mv']).std() * np.sqrt((len(date_list) - 1) / year)
    sharpe = annualized_return / annualized_volatiltity
    mdd = 1 - (mv_df.loc[:, 'mv'] / mv_df.loc[:, 'mv'].rolling(10000, min_periods=1).max()).min()
    bt_info = 0
    Weights['mdd'] = mdd
    Weights['annual_ret'] = annualized_return
    Weights['sharpe'] = sharpe
    Weights['5_year_ret'] = five_year_return
    Weights['annual_vol'] = annualized_volatiltity
    
    
    return Weights


'''
# reasearch
res = []
for i in range(200,1000,20):
    for j in range(300,1000-i,20):
        t1 = time.time()
        for k in range(0,1000-i-j,20):
            l = 1000 - i-k-j
            w = {
                '国债指数':i/1000,
                '中证信用':j/1000,
                '标普500人民币':k/1000,
                '中证500':l/1000,
                '德标30人民币': 0.0,
                 '沪深300': 0.0,
                 '日经225人民币': 0.0,
                 '创业板指': 0.0,
                 '房地产指数': 0.0,
                 '黄金': 0.0,
                 '石油': 0.0,
            }
            res.append(search_grid(w))
    
        print(f'j = {j} finish, cost time {time.time() - t1}')  
    print('finish i ')



df = pd.read_csv('backtest_result.csv',encoding='utf-8',index_col=0)

df_10 = df[df['mdd']<0.1]
df_10 = df_10[df_10['mdd']>0.095]
df_10 = df_10.sort_values(['mdd','annual_ret'],ascending=False)[['中证500','中证信用','国债指数','标普500人民币']]


df_7 = df[df['mdd']<0.07]
df_7 = df_7[df_7['mdd']>0.065]
df_7 = df_7.sort_values(['mdd','annual_ret'],ascending=False)[['中证500','中证信用','国债指数','标普500人民币']]


res10 = []
for i in df_10.head(30).to_dict('records'):
    i['德标30人民币']=0
    i['沪深300']=0.0
    i['日经225人民币']=0.0
    i['创业板指']=0.0
    i['房地产指数']=0
    i['黄金']=0.0
    i['石油']=0.0
    res10.append(search_grid(i))

pd.DataFrame(res10).drop(['德标30人民币','沪深300','日经225人民币','创业板指','房地产指数','黄金','石油'], axis = 1)


res7 = []
for i in df_7.head(30).to_dict('records'):
    i['德标30人民币']=0
    i['沪深300']=0.0
    i['日经225人民币']=0.0
    i['创业板指']=0.0
    i['房地产指数']=0
    i['黄金']=0.0
    i['石油']=0.0
    res7.append(search_grid(i))


pd.DataFrame(res7).drop(['德标30人民币','沪深300','日经225人民币','创业板指','房地产指数','黄金','石油'], axis = 1)
'''