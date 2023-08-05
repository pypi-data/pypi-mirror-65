from load_and_update_data.get_fund_data import DataLoader
import pandas as pd
import numpy as np
from sqlalchemy import create_engine
from type_ranks import type_ranks 
import random
from datetime import datetime, timedelta
import matplotlib as mpl
import pylab as pl
import copy
mpl.rcParams['font.family'] = ['Heiti TC']

class FundData():
    
    '''
    fund backtest clean data
    '''
    
    ASSET_DICT = {
        'A股大盘':'沪深300',
        'A股中盘':'中证500',
        '美股大盘':'标普500',
        '创业板':'创业板指',
        '德国大盘':'德标30',
        '日本大盘':'日经225',
        '利率债':'国债指数',
        '信用债':'中证信用',
        '房地产':'房地产指数',
        '黄金':'黄金',
        '石油':'石油',    
    }
    ASSET_NAME = ['A股大盘','A股中盘','美股大盘','创业板','德国大盘','日本大盘','利率债','信用债','房地产','黄金','石油']
    YEAR = 242
    SCORE_TAG = '大类资产评级v1'
    TRADEABLE = ['Open','Limited']
    FORBIDDEN = ['Suspended','Close']
    FEE = 0.01
    FUNDS_NUMS = 2 # each type of asset number
    MAX_LOAD = 10 # max number of loading funds of each type asset
    BUY = 'BUY'
    SEL = 'SELL'
    BUY_INT = 1
    SEL_INT = -1
    SCORE_BEGIN_DAY = '20180331'
    
    def __init__(self):
        self.db_connect()
        self.index_data = self.dl.get_data('active_asset_index').set_index('date').drop(['标普500人民币','德标30人民币','日经225人民币'],axis=1).dropna().astype(float)
        self.switch_date = self.get_switch_date()
        self.get_fund_score_and_fund_list()
        self.get_fee()
        self.get_fund_nav()
        self.get_suspend()
        
    def db_connect(self):
        username = 'huangkejia'
        password = 'Huangkejia123456'
        database = 'quant_data'
        derivedbase = 'derived_data'
        self.dl = DataLoader(username, password, database_name=database)
        self.d2 = DataLoader(username, password, database_name=derivedbase)
      
    def get_fund_score_and_fund_list(self):
        # get fund score first level asset, second level date
        # get total fund list
        self.score_data = {}
        for a_i in self.ASSET_NAME:
            self.score_data[self.ASSET_DICT[a_i]] = {}
        self.fund_list = []
        for d in self.switch_date:   
            funds_score_d = type_ranks(self.SCORE_TAG, self.ASSET_NAME, d)
            max_version = funds_score_d['version'].max()
            funds_score_d = funds_score_d[funds_score_d['version'] == max_version]
            funds_score_d = funds_score_d[funds_score_d['is_full'] == 1]
            for a_i in self.ASSET_NAME:
                fund_l = funds_score_d[funds_score_d['tag_name'] == a_i].fund_id.tolist()[:self.MAX_LOAD]
                self.score_data[self.ASSET_DICT[a_i]][d] = fund_l
                self.fund_list.extend(fund_l)
        self.fund_list =  list(set(self.fund_list))
        
    def get_switch_date(self):
        # get first date of month as switch date
        self.date_list = self.index_data[self.index_data.index>=self.SCORE_BEGIN_DAY].index.tolist()
        
        month_list = ['2017','2018','2019']
        month_list = [i+str(j+1).zfill(2) for i in month_list for j in range(12)] + ['202001']
        
        switch_date = []
        for m in month_list:
            if not month_list.index(m) % 3 == 0:
                 continue
            tmp = []
            for d in self.date_list:
                if m in d:
                    tmp.append(d)
            if len(tmp) < 1:
                continue
            switch_date.append(min(tmp))
        return switch_date

    def get_fee(self):
        manage_fee = self.dl.get_data('fund_fee_info', column_names=['manage_fee','fund_id','trustee_fee']).set_index('fund_id')
        self.fund_fee = {i: BtElm(hold_fee=sum(manage_fee.loc[i,])/100, buy_fee=self.FEE, sel_fee=self.FEE) for i in self.fund_list}
        
    def get_fund_nav(self):
        self.fund_nav = {}
        for fund_i in self.fund_list:
            try:
                nav_i = self.dl.get_data('nav', column_names=['adjusted_net_value','subscribe_status','redeem_status','datetime','fund_id'],
                                   select_columns = ['datetime','datetime','fund_id'],
                                   aim_values=[self.switch_date[0], self.switch_date[-1], fund_i], 
                                   operator=['>=', '<=', '='])
                self.fund_nav[fund_i] = nav_i.set_index('datetime')
            except:
                continue
   
    def get_suspend(self):
        self.suspend_buy = {}
        self.suspend_sel = {}

        for i in self.date_list:
            self.suspend_buy[i] = []
            self.suspend_sel[i] = []

        for f in self.fund_nav:
            df = self.fund_nav[f].copy()
            for d,dic in zip(df.index,df.to_dict('records')):
                if d not in self.date_list:
                    continue
                if not dic['redeem_status'] in self.TRADEABLE:
                    self.suspend_sel[d].append(dic['fund_id'])

                if not dic['subscribe_status'] in self.TRADEABLE:
                    self.suspend_buy[d].append(dic['fund_id'])
    
    
class BacktestInfo():
    
    '''
    save backtest history
    '''

    def __init__(self,cash=None,period=None,top=None,last_amount=None,weights=None):
        self.cash       = cash
        self.cash_weights = {}
        self.last_amount = last_amount
        self.position   = []
        self.trade_history        = []
        self.cash_history         = {}
        self.position_history     = {}
        self.market_value_history = {}
        self.weights_history = {}
        self.trade_list = []
        self.order_list = []
        self.wait_sel_list = []
        self.fund_fee = []
        self.fee_history = {}
        self.fee_total = 0
        self.hold_fee_total = 0
        self.suspend_buy = {}
        self.suspend_sel = {}
        self.weights = { k: v for k,v in weights.items() if v > 0}
        
class BtElm():

    '''
    memory element of backtest info, include trade cash position market_value 
    '''

    def __init__(self,fundid=None,unit_net_value=None,volume=0,date=None,cash=None,direction=None,weights=None,sel_fee=None,buy_fee=None,hold_fee=None,amount=None,paired=None,sel_part=None):
        self.fundid = fundid
        self.unit_net_value = unit_net_value
        self.volume = volume
        self.date = date
        self.cash = cash
        self.amount = amount
        self.direction = direction
        self.weights = weights
        self.sel_fee = sel_fee
        self.buy_fee = buy_fee
        self.hold_fee = hold_fee
        self.paired = paired
        self.sel_part = sel_part
    
     
    def __str__(self):
        return f'<fundid={self.fundid} unit_net_value={self.unit_net_value} volume={self.volume}  amount={self.amount} weights={self.weights} direction={self.direction}>'
    
    
class BacktestEngine():
    
    '''
    fund backtest engine
        FundData        : class of backtest clean data
        BacktestInfo    : class of backtest info data
        BtElm           : class of element of backtest
    '''
    
    def __init__(self):
        
        w = {
            '标普500': 2/100,
            '德标30':0,
            '日经225':0,
            '国债指数':22/100,
            '中证500':16/100,
            '创业板指':0,
            '沪深300':0,
            '中证信用':60/100,
            '房地产指数':0,
            '黄金':0/100,
            '石油':0,
        }
        #self.bt_info = BacktestInfo(cash = 1e8, weights = w)
        #self.data = FundData()
        
    def get_weights(self, d):
        #d = self.date_list[0]
        data = {}
        for k, v in self.bt_info.weights.items():
            data[k] = {}
            first_filter = self.data.score_data[k][d][:self.data.FUNDS_NUMS]
            suspend_buy_today = self.data.suspend_buy[d]
            data[k]['weights'] = v

            # all recommended funds suspend buy, choose another one
            if all([ _ in suspend_buy_today for _ in first_filter ]):
                for i in self.data.score_data[k][d][self.data.FUNDS_NUMS:]:
                    if i not in suspend_buy_today:
                        data[k]['funds'] = [i]
                        break

            # remove suspend buy funds
            else:
                data[k]['funds'] = [ _ for _ in first_filter if _ not in suspend_buy_today]
        weights_today = {}
        for k ,v in data.items():
            for i in v['funds']:
                weights_today[i] = v['weights'] / len(v['funds'])
        return weights_today
    
    def get_unit_nv(self, d, fund_id):
        try:
            return float(self.data.fund_nav[fund_id].loc[d,'adjusted_net_value'])
        except:  
            datelist = self.data.fund_nav[fund_id].index.values
            d = datelist[datelist<d][-1]
            return float(self.data.fund_nav[fund_id].loc[d,'adjusted_net_value'])
    
    def get_sign(self, x):
        return int(x>0)*2-1
    
    def get_w(self, dic, k):
        if k not in list(dic.keys()):
            return 0
        else:
            return float(dic[k])
    
    def get_diff_weight(self, dic1, dic2, k):
        return self.get_w(dic2, k) - self.get_w(dic1, k)
    
    def get_date_diff(self, d1, d2):
        return self.data.date_list.index(d2) - self.data.date_list.index(d1)
    
    def backtest(self):
        for d in self.data.date_list:
            self.bt_info.order_list = []
            # rebalance 
            if d in self.data.switch_date:
                self.weights = self.get_weights(d)
                # build porfolio on first day
                if self.data.switch_date.index(d) == 0:        
                    for k,v in self.weights.items():
                        f_i = self.data.fund_fee[k]
                        p = self.get_unit_nv(d,k)
                        volume = self.bt_info.cash*v/p/(1+f_i.buy_fee)
                        o = BtElm(amount=self.bt_info.cash*v, fundid=k, unit_net_value=p, volume = volume)
                        self.bt_info.order_list.append(o)

                # rebalance, based on last day weights and marketvalue
                else:
                    last_day =  self.data.date_list[self.data.date_list.index(d) - 1]
                    last_weights = self.bt_info.weights_history[last_day]
                    last_weights.pop('date',None)
                    last_mv = self.bt_info.market_value_history[last_day]
                    pool = list(set(list(self.weights.keys()) + list(last_weights.keys())))
                    for f in pool:
                        w_diff = self.get_diff_weight(last_weights, self.weights, f)
                        p = self.get_unit_nv(d,f)
                        sign = self.get_sign(w_diff)
                        trade_fee = f_i.buy_fee if sign > 0 else f_i.sel_fee
                        volume = last_mv * w_diff /p /( 1 + sign* trade_fee)
                        o = BtElm(amount=last_mv * w_diff, fundid=f, unit_net_value=p, volume = volume)
                        self.bt_info.order_list.append(o)

            # every day trade  
            self.bt_info.fee_history[d] = {}

            ## fund trade fee and hold fee
            wait_tmp = self.bt_info.wait_sel_list
            self.bt_info.wait_sel_list = []
            for t_i in self.bt_info.order_list + wait_tmp:

                ## check if pos info exised else create new one 
                pos = None
                f_i = self.data.fund_fee[t_i.fundid]
                for pos_i in self.bt_info.position:
                    if pos_i.fundid == t_i.fundid:
                        pos = pos_i
                if pos == None:
                    pos = BtElm(fundid=t_i.fundid, volume=0,amount=0)
                    self.bt_info.position.append(pos) 

                ## trade process: update cash and pos volume
                ## buy sign == 1    sel sign == -1
                sign = self.get_sign(t_i.volume)

                direc = self.data.BUY if sign > 0 else self.data.SEL

                ## if forbiden sell today, put order in wait sell list
                if direc == self.data.SEL:
                    if t_i.fundid in self.data.suspend_sel[d]:
                        self.wait_sel_list.append(t_i)
                        continue

                p = self.get_unit_nv(d,t_i.fundid)
                trade_fee = f_i.buy_fee if sign > 0 else f_i.sel_fee
                a_book = t_i.volume * p
                a_real = t_i.volume * p * (1+ (sign* trade_fee))
                self.bt_info.fee_history[d][t_i.fundid] =  t_i.volume * p *(sign* trade_fee)
                self.bt_info.fee_total += t_i.volume * p *(sign* trade_fee)
                pos.volume += t_i.volume
                pos.amount += a_book

                pair_volume =  copy.deepcopy(t_i.volume)
                ## if sell, pay hold fee
                hold_fee_i = 0

                if direc == self.data.SEL:
                    for buy_i in self.bt_info.trade_history:
                        ## if same fundid
                        con1 = t_i.fundid == buy_i.fundid
                        ## if buy
                        con2 = buy_i.direction==self.data.BUY
                        ## if not sell all yet
                        con3 = buy_i.paired==False
                        if all([con1, con2, con3]):

                            v_dif = (buy_i.volume - buy_i.sel_part)
                            buy_i.sel_part = max(buy_i.volume, pair_volume)
                            ## matach by one trade compelte
                            if pair_volume == v_dif:
                                buy_i.paired = True
                                buy_i.sel_part += pair_volume
                                hold_fee_i += pair_volume * p *(self.get_date_diff(buy_i.date,d)/242) * f_i.hold_fee
                                pair_volume = 0

                            #matach by one trade , trade still have unsell part
                            elif pair_volume < v_dif :
                                buy_i.paired = False
                                buy_i.sel_part += pair_volume
                                hold_fee_i += pair_volume * p *(self.get_date_diff(buy_i.date,d)/242) * f_i.hold_fee
                                pair_volume = 0

                            #matach by more than one trade
                            else :
                                buy_i.paired = True
                                buy_i.sel_part = buy_i.volume
                                hold_fee_i += buy_i.volume * p *(self.get_date_diff(buy_i.date,d)/242) * f_i.hold_fee
                                pair_volume -= buy_i.volume

                            if pair_volume == 0:
                                break

                self.bt_info.hold_fee_total += hold_fee_i
                self.bt_info.cash -= (a_real + hold_fee_i)

                ## update trade history
                t = BtElm(fundid=t_i.fundid, volume=t_i.volume,direction=direc,date=d,unit_net_value=p,amount=a_book, paired=False,sel_part=0)
                #print(f'trade : {t}')
                self.bt_info.trade_history.append(t)
                fee_num = t_i.volume * p *(sign* trade_fee)

            ## update position fund unit_net_value and amount
            for pos_i in self.bt_info.position:
                pos_i.unit_net_value = self.get_unit_nv(d,pos_i.fundid)
                pos_i.amount = pos_i.unit_net_value * pos_i.volume

            #update position history and market value
            self.bt_info.position_history[d] = [copy.deepcopy(pos_i) for pos_i in self.bt_info.position if pos_i.volume >0]
            self.bt_info.market_value_history[d] = sum([ pos.amount for pos in self.bt_info.position_history[d]]) + self.bt_info.cash

            weights_i = { pos_i.fundid: pos_i.amount/ (self.bt_info.market_value_history[d] + self.bt_info.cash) for pos_i in self.bt_info.position}

            self.bt_info.weights_history[d] = weights_i
            self.bt_info.cash_history[d] = round(self.bt_info.cash,4)

    
    def mv_display(self):
        df_mv = pd.DataFrame([{'date':k, 'mv':v} for k,v in self.bt_info.market_value_history.items()]).set_index('date')
        df_mv.plot.line(figsize=(18,9),legend=False,fontsize = 13)
        
        
        
        l = pl.legend(loc='lower left',fontsize = 13)
        s = pl.title('market value', fontsize=20)
        year = len(df_mv.index.tolist())/self.data.YEAR
        total_return = df_mv['mv'][-1] / df_mv['mv'][0]
        annualized_return = np.exp(np.log(total_return)/year) - 1
        annualized_volatiltity = (df_mv['mv'].shift(1) / df_mv['mv']).std() * np.sqrt((len(df_mv.index.tolist()) - 1) / year)
        sharpe = annualized_return / annualized_volatiltity
        mdd = 1 - (df_mv.loc[:, 'mv'] / df_mv.loc[:, 'mv'].rolling(10000, min_periods=1).max()).min()
        df_mv['date'] = df_mv.index
        mdd_part1 = (df_mv.loc[:, 'mv'] / df_mv.loc[:, 'mv'].rolling(10000, min_periods=1).max())
        mdd_date1 = df_mv.loc[df_mv.loc[:mdd_part1.idxmin(),'mv'].idxmax(),'date']
        mdd_date2 = df_mv.loc[mdd_part1.idxmin(),'date']

        print(f'totol return : {total_return}')
        print(f'annualized return : {annualized_return}')
        print(f'annualized volatiltity : {annualized_volatiltity}')
        print(f'sharpe : {sharpe}')
        print(f'max draw down: {mdd}')
        print(f'max draw down start date {mdd_date1} end date {mdd_date2} ')
