import pandas as pd
import numpy as np
import copy

import matplotlib as mpl
import pylab as pl
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import matplotlib.colors as colors

from type_ranks import type_ranks 
from load_and_update_data.get_fund_data import DataLoader
mpl.rcParams['font.family'] = ['Heiti TC']

# one year days YEAR = 242
# adjusted day T = 20 

class DefaultData:

    BUY = 'BUY'
    SEL = 'SELL'
    BUY_INT = 1
    SEL_INT = -1
    YEAR = 242
    SCORE_TAG = '大类资产评级v1'
    TRADEABLE = ['Open','Limited']
    FORBIDDEN = ['Suspended','Close']
    FEE = 0.007
    INDEX_FEE = 0
    ASSET_DICT = {
        'A股大盘':'沪深300',
        'A股中盘':'中证500',
        '美股大盘':'标普500人民币',
        '创业板':'创业板指',
        '德国大盘':'德标30人民币',
        '日本大盘':'日经225人民币',
        '利率债':'国债指数',
        '信用债':'中证信用',
        '房地产':'房地产指数',
        '黄金':'黄金',
        '石油':'石油',    
    }
    ASSET_NAME = ['A股大盘','A股中盘','美股大盘','创业板','德国大盘','日本大盘','利率债','信用债','房地产','黄金','石油']
    FUNDS_NUMS = 2 # each type of asset number
    MAX_LOAD = 10 # max number of loading funds of each type asset
    SCORE_BEGIN_DAY = '20180331'
    FUNDS_BACKTEST = 'FUNDS_BACKTEST'
    ASSET_BACKTEST = 'ASSET_BACKTEST'

class DBConnect:
    
    '''
    db connect with account info
    '''
    
    USERNAME = 'huangkejia'
    PASSWORD = 'Huangkejia123456'
    ORIGINBASE = 'quant_data'
    DERIVEDBASE = 'derived_data'

    def __init__(self):    
        self.db_origin = DataLoader(self.USERNAME, self.PASSWORD, database_name=self.ORIGINBASE)
        self.db_derived = DataLoader(self.USERNAME, self.PASSWORD, database_name=self.DERIVEDBASE)


class IndexData(DBConnect, DefaultData):
    
    '''
    asset allocation cleaned data
    '''

    def __init__(self,begin_date=None):   
        super(IndexData, self).__init__()
        self.index_data = self.db_origin.get_data('active_asset_index').set_index('date').loc[begin_date:,].drop(['标普500','德标30','日经225'],axis = 1).fillna(method= 'ffill')
        self.date_list = self.index_data.index.tolist()
        self.asset_list = self.index_data.columns.tolist()

class FundData(DBConnect, DefaultData):
     
    '''
    fund backtest cleaned data
    '''

    def __init__(self,begin_date=None,weights=None):
        super(FundData, self).__init__()
        self.weights = { k: float(v) for k,v in weights.items() if v > 0}
        self.index_data = self.db_origin.get_data('active_asset_index').set_index('date').loc[begin_date:,].drop(['标普500','德标30','日经225'],axis = 1).fillna(method= 'ffill')
        self.date_list = self.index_data.index.tolist()
        self.asset_list = list(self.weights.keys())
        self.get_fund_score_and_fund_list()
        self.get_fee()
        self.get_fund_nav()
        self.get_suspend()

    def get_unit_nv(self, d, fund_id):
        try:
            return float(self.fund_nav[fund_id].loc[d,'adjusted_net_value'])
        except:  
            datelist = self.fund_nav[fund_id].index.values
            d = datelist[datelist<d][-1]
            return float(self.fund_nav[fund_id].loc[d,'adjusted_net_value'])

    def get_fund_score_and_fund_list(self):
        # get fund score first level asset, second level date
        # get total fund list
        self.score_data = {}
        asset_list = [k for i in list(self.weights.keys()) for k,v in self.ASSET_DICT.items() if i == v]
        for a_i in asset_list:
            self.score_data[self.ASSET_DICT[a_i]] = {}
        self.fund_list = []
        
        for d in self.date_list:  
            try:
                funds_score_d = type_ranks(self.SCORE_TAG, asset_list, d)
            except:
                continue
            max_version = funds_score_d['version'].max()
            funds_score_d = funds_score_d[funds_score_d['version'] == max_version]
            funds_score_d = funds_score_d[funds_score_d['is_full'] == 1]
            for a_i in asset_list:
                fund_l = funds_score_d[funds_score_d['tag_name'] == a_i].fund_id.tolist()[:self.MAX_LOAD]
                self.score_data[self.ASSET_DICT[a_i]][d] = fund_l
                self.fund_list.extend(fund_l)
        self.fund_list =  list(set(self.fund_list))
        
    def get_fee(self):
        manage_fee = self.db_origin.get_data('fund_fee_info', column_names=['manage_fee','fund_id','trustee_fee','purchase_fee','redeem_fee']).set_index('fund_id')
        # right now fund fee data is not sufficient, if not exsited fill with default value
        # self.fund_fee = {i: BtElm(hold_fee=manage_fee.loc[i,][['manage_fee','trustee_fee']].sum()/100, buy_fee=manage_fee.loc[i,]['purchase_fee'], sel_fee=manage_fee.loc[i,]['redeem_fee']) for i in self.fund_list}
        self.fund_fee = {}
        manage_fee = manage_fee.fillna(0)
        for i in self.fund_list:
            hold_fee=manage_fee.loc[i,][['manage_fee','trustee_fee']].sum()/100
            buy_fee= manage_fee.loc[i,]['purchase_fee']/100
            sel_fee=manage_fee.loc[i,]['redeem_fee']/100
            buy_fee = self.FEE if buy_fee == 0 else buy_fee
            sel_fee = self.FEE if sel_fee == 0 else sel_fee
            self.fund_fee[i] = BtElm(hold_fee=hold_fee, buy_fee=buy_fee, sel_fee=sel_fee) 

    def get_fund_nav(self):
        self.fund_nav = {}
        for fund_i in self.fund_list:
            try:
                nav_i = self.db_origin.get_data('nav', column_names=['adjusted_net_value','subscribe_status','redeem_status','datetime','fund_id'],
                                select_columns = ['datetime','datetime','fund_id'],
                                aim_values=[self.date_list[0], self.date_list[-1], fund_i], 
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


class BacktestInfo:
    
    '''
    save backtest history
    '''

    def __init__(self,cash=None,weights=None,last_amount=None):
        self.cash       = cash
        self.cash_history = {}
        self.index_position   = []
        self.index_position_history     = {}
        self.position   = []
        self.position_history = {}
        self.trade_history        = []
        self.index_market_value_history = {}
        self.index_weights_history = {}
        self.index_weights = { k: float(v) for k,v in weights.items() if v > 0}
        self.market_value_history = {}
        self.wait_sel_list = []
        self.rebalance_date = []
        self.cash_wait_list = []
        self.cash_wait_list_new = []
        self.order_list = []
        self.order_list_new = []
        self.trade_history = []
        self.fee_history = {}
        self.fee_total = 0
        self.hold_fee_total = 0
        self.last_amount = last_amount
        self.weights_history = {}

class BtElm:

    '''
    memory element of index backtest info, 
    '''

    def __init__(self,index_name=None,index_value=None,fundid=None,fund_price=None,volume=0,date=None,cash=None,amount=None,types=None,wait_day=None,direction=None,sel_fee=None,buy_fee=None,hold_fee=None,paired=None,sel_part=None):
        self.index_name = index_name
        self.index_value = index_value
        self.fundid = fundid
        self.fund_price = fund_price
        self.volume = volume
        self.date = date
        self.cash = cash

        self.amount = amount
        self.types = types
        self.wait_day = wait_day
        self.direction = direction
        self.sel_fee = sel_fee
        self.buy_fee = buy_fee
        self.hold_fee = hold_fee
        self.paired = paired
        self.sel_part = sel_part

    def __str__(self):
        if self.types == DefaultData.ASSET_BACKTEST:
            return f'<index={self.index_name} index_value={self.index_value} volume={self.volume}  amount={self.amount}>'

        elif self.types ==  DefaultData.FUNDS_BACKTEST:
            return f'<fundid={self.fundid} fund_price={self.fund_price} volume={self.volume}  amount={self.amount} direction={self.direction}>'
    
    

class BacktestEngine():
    
    '''
    fund backtest engine
        FundData        : class of backtest clean data
        BacktestInfo    : class of backtest info data
        BtElm           : class of element of backtest
    '''
    
    EXCHANGE_LIMIT = 0.03   # if each fund weights difference over EXCHANGE_LIMIT, rebalance
    
    def __init__(self,begin_date=None,weights=None,types=None):
        self.data = IndexData(begin_date=begin_date) if types==DefaultData.ASSET_BACKTEST else FundData(begin_date=begin_date,weights=weights)
        self.weights = weights
        self.begin_date = begin_date
        self.types=types

        self.last_trade_day = ''# update after update backtest info everyday
        self.targets_w = {}     # target weight, update at the begin of each day
        self.lastday_w = {}     # weight last day , update after everyday trade
        self.asset_pool = []    # total assets combine with last day and today
        self.diff_w = {}        # the different bewteen target_w and lastday_w, exchange or not on this 
        self.rebalance = True   # boolean of whether to rebalance today, True rebalance, False not change
                                # rebalance includes building porfolio at the first day, 
        self.RESERVE = 0.0      # keep cash rate
        self.ADJUSTED = 1    # consider trading fee, keep more money than REASERVE 
        self.BUY = 'BUY'
        self.SEL = 'SELL'
        self.BUY_INT = 1
        self.SEL_INT = -1

        self.CASH_WAIT_DAY = 5
        self.cash_delay_con = False # input parameter, if True, all money get by sell will be delayed 
        self.enough_cash_trade = False # if cash not enough, buy next trade day


    def get_sign(self, x):
        return int(x>0)*2-1

    def get_tradable_asset(self, date):
        # get tradable asset and update weights
        self.targets_w  = {}
        for a_i in self.data.asset_list:
            if np.isnan(self.data.index_data.loc[date,a_i]):
                continue
            else:
                w = self.bt_info.index_weights.get(a_i, 0) 
                if w == 0:
                    continue
                self.targets_w[a_i] = w
        s =  sum(list(self.targets_w .values()))
        self.targets_w  = {k : v / s for k, v in self.targets_w .items()}     
        
        if self.types == self.data.ASSET_BACKTEST:
            return
        elif self.types == self.data.FUNDS_BACKTEST:    
            data = {}
            for k, v in self.targets_w.items():
                data[k] = {}
                first_filter = self.data.score_data[k][date][:self.data.FUNDS_NUMS]
                suspend_buy_today = self.data.suspend_buy[date]
                data[k]['weights'] = v
                
                # if all recommended funds suspend buy, choose another one
                if all([ _ in suspend_buy_today for _ in first_filter ]):
                    for i in self.data.score_data[k][date][self.data.FUNDS_NUMS:]:
                        if i not in suspend_buy_today:
                            data[k]['funds'] = [i]
                            break
            
                # remove suspend buy funds
                else:
                    data[k]['funds'] = [ _ for _ in first_filter if _ not in suspend_buy_today]
    
        self.targets_w = {}
        for k ,v in data.items():
            for i in v['funds']:
                self.targets_w[i] = v['weights'] / len(v['funds'])    

    def get_price(self, d, asset):
        if self.types == self.data.FUNDS_BACKTEST:    
            try:
                return float(self.data.fund_nav[asset].loc[d,'adjusted_net_value'])
            except:  
                datelist = self.data.fund_nav[asset].index.values
                d = datelist[datelist<d][-1]
                return float(self.data.fund_nav[asset].loc[d,'adjusted_net_value'])

        elif self.types == self.data.ASSET_BACKTEST:
            return self.data.index_data.loc[d, asset] 

        
    def get_date_diff(self, d1, d2):
        return self.data.date_list.index(d2) - self.data.date_list.index(d1)



    def get_pos(self, asset_name):
        pos = None
        if self.types == self.data.ASSET_BACKTEST:
            for pos_i in self.bt_info.index_position:
                if pos_i.index_name == asset_name:
                    pos = pos_i
            if pos is None:
                pos = BtElm(index_name=asset_name, volume=0,amount=0,types=self.types)
                self.bt_info.index_position.append(pos)

        elif self.types == self.data.FUNDS_BACKTEST:
            for pos_i in self.bt_info.position:
                if pos_i.fundid == asset_name:
                    pos = pos_i
            if pos is None:
                pos = BtElm(fundid=asset_name, volume=0,amount=0,types=self.types)
                self.bt_info.position.append(pos)
    
        return pos 

    def compare_target_and_last_weights(self):
        self.asset_pool = list(set([*self.targets_w, *self.lastday_w ]))
        self.diff_w = {} 
        for a_i in self.asset_pool:
            self.diff_w[a_i] = round(self.targets_w.get(a_i, 0) - self.lastday_w.get(a_i, 0),6)

    def judge_rebalance(self):
        # rebalance base on last day weight and target weights
        # rebalance if the max of weight different exceed EXCHANGE_LIMIT
        # TODO try other rebalance logic such as the difference between weights exceed some value
        self.rebalance =  max(list(self.diff_w.values())) > self.EXCHANGE_LIMIT

    def cash_delay_receive(self):
        self.bt_info.cash_wait_list_new = []
        # update cash info, if wait day = 1, cash received 
        for c_i in self.bt_info.cash_wait_list:  
            if c_i.wait_day >1:
                c_i.wait_day -= 1
                self.bt_info.cash_wait_list_new.append(c_i)
            else:
                self.bt_info.cash += c_i.cash
        self.bt_info.cash_wait_list = self.bt_info.cash_wait_list_new.copy()

    def cash_delay_trade(self,a_real,sign):
        ## if buy, cash decrease immediately
        ## if sel, cash save in wait list
        if sign == self.BUY_INT:
            self.bt_info.cash -= a_real
        elif sign == self.SEL_INT:
            c_i = BtElm(cash=-a_real,wait_day=self.CASH_WAIT_DAY,types='index')
            self.bt_info.cash_wait_list.append(c_i)
        
    def update_bt_info(self, d):
        if self.types == self.data.ASSET_BACKTEST:
            for pos_i in self.bt_info.index_position:
                pos_i.index_value = self.get_price(d, pos_i.index_name)
                pos_i.amount = pos_i.index_value * pos_i.volume
            
            #update position history and market value
            self.bt_info.index_position_history[d] = [copy.deepcopy(pos_i) for pos_i in self.bt_info.index_position if pos_i.volume >0]
            self.bt_info.index_market_value_history[d] = sum([ pos.amount for pos in self.bt_info.index_position_history[d]]) + self.bt_info.cash
            self.lastday_w  = { pos_i.index_name: pos_i.amount/ self.bt_info.index_market_value_history[d] for pos_i in self.bt_info.index_position}
            self.bt_info.index_weights_history[d] = self.lastday_w
            self.bt_info.cash_history[d] = self.bt_info.cash
            self.last_trade_day = d

        elif self.types == self.data.FUNDS_BACKTEST:
            for pos_i in self.bt_info.position:
                pos_i.fund_price = self.get_price(d, pos_i.fundid)
                pos_i.amount = pos_i.fund_price * pos_i.volume

            #update position history and market value
            self.bt_info.position_history[d] = [copy.deepcopy(pos_i) for pos_i in self.bt_info.position if pos_i.volume >0]
            self.bt_info.market_value_history[d] = sum([ pos.amount for pos in self.bt_info.position_history[d]]) + self.bt_info.cash
            self.lastday_w  = { pos_i.fundid: pos_i.amount/ (self.bt_info.market_value_history[d] + self.bt_info.cash) for pos_i in self.bt_info.position}
            self.bt_info.weights_history[d] = self.lastday_w 
            self.bt_info.cash_history[d] = round(self.bt_info.cash,4)
            self.last_trade_day = d

    def if_cash_enough(self, sign, t_i):
        # if have cash more than RESERVE RATE trade, else buy on next day
        posi_amount = sum([_.amount for _ in self.bt_info.index_position if _.amount >= 0]) 
        cash_rate = self.bt_info.cash /(posi_amount + self.bt_info.cash)
        if cash_rate <=  (self.RESERVE - self.ADJUSTED) and sign == self.BUY_INT:
            #print(f'not enough cash {t_i} cash_rate {cash_rate}')
            self.bt_info.order_list_new.append(t_i)
            return True
        return False
    
    def order_update(self):
        self.bt_info.order_list = self.bt_info.order_list_new.copy()
        self.bt_info.order_list_new = []

    def backtest(self):
        if self.types == self.data.ASSET_BACKTEST:
            self.asset_backtest()
        elif self.types == self.data.FUNDS_BACKTEST:
            self.fund_backtest()

    def calculate_fund_hold_fee(self, t_i, direc, f_i, p ,d):
        pair_volume =  copy.deepcopy(t_i.volume)
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
        return hold_fee_i  


    def asset_backtest(self):
        self.bt_info = BacktestInfo(cash = 1e8, weights = self.weights)
        for d in self.data.date_list:
            
            self.get_tradable_asset(d)
            self.compare_target_and_last_weights()
            self.judge_rebalance()
    
            if self.cash_delay_con:
                self.cash_delay_receive()

            if self.rebalance:
                self.bt_info.rebalance_date.append(d)
                last_mv = self.bt_info.index_market_value_history.get(self.last_trade_day, self.bt_info.cash)
                for a_i in self.asset_pool:
                    amount = last_mv *(1 -self.RESERVE )* self.diff_w[a_i]
                    
                    volume = amount / self.data.index_data.loc[d, a_i] 
                    
                    o = BtElm(index_name=a_i,date=d,volume = volume,amount=0,types=self.types)
                    self.bt_info.order_list.append(o)

            
            self.bt_info.fee_history[d] = {}

            for t_i in self.bt_info.order_list:
                pos_i = self.get_pos(t_i.index_name)
                sign = self.get_sign(t_i.volume)

                if self.enough_cash_trade:
                    if self.if_cash_enough(sign, t_i):
                        continue

                direc = self.BUY if sign > 0 else self.SEL
                index_v = self.data.index_data.loc[d, t_i.index_name] 
                a_book = t_i.volume * index_v
                a_real = t_i.volume * index_v * (1+ (sign* self.data.INDEX_FEE))
                
                self.bt_info.fee_history[d][t_i.index_name] =    t_i.volume * index_v *(sign* self.data.INDEX_FEE)
                self.bt_info.fee_total += t_i.volume * index_v *(sign* self.data.INDEX_FEE)
                pos_i.volume += t_i.volume
                pos_i.amount += a_book
                
                if self.cash_delay_con:
                    self.cash_delay_trade(a_real,sign)
                else:
                    self.bt_info.cash -= a_real
            
                t = BtElm(index_name=t_i.index_name,volume=abs(t_i.volume),direction=direc,date=d,index_value=index_v,amount=a_book,types=self.types)
  
                self.bt_info.trade_history.append(t)
            
            self.order_update()
            self.update_bt_info(d)
    
    def fund_backtest(self):
        self.bt_info = BacktestInfo(cash = 1e8, weights = self.weights)
        for d in self.data.date_list:
            self.get_tradable_asset(d)
            self.compare_target_and_last_weights()
            self.judge_rebalance()
    
            if self.cash_delay_con:
                self.cash_delay_receive()

            if self.rebalance:
                self.bt_info.rebalance_date.append(d)
                last_mv = self.bt_info.market_value_history.get(self.last_trade_day, self.bt_info.cash)
                for a_i in self.asset_pool:
                    f_i = self.data.fund_fee[a_i]
                    sign = self.get_sign(self.diff_w[a_i])
                    trade_fee = f_i.buy_fee if sign > 0 else f_i.sel_fee
                    amount = last_mv *(1 -self.RESERVE )* self.diff_w[a_i]
                    volume = amount / self.get_price(d, a_i) / ( 1 + sign* trade_fee)
                    o = BtElm(fundid=a_i,date=d,volume = volume,amount=0,types=self.types)
                    self.bt_info.order_list.append(o)

            # every day trade  
            self.bt_info.fee_history[d] = {}

            ## fund trade fee and hold fee
            wait_tmp = self.bt_info.wait_sel_list
            self.bt_info.wait_sel_list = []    
            for t_i in self.bt_info.order_list + wait_tmp:
                pos_i = self.get_pos(t_i.fundid)
                sign = self.get_sign(t_i.volume)

                if self.enough_cash_trade:
                    if self.if_cash_enough(sign, t_i):
                        continue

                f_i = self.data.fund_fee[t_i.fundid]
                direc = self.BUY if sign > 0 else self.SEL
                ## if forbiden sell today, put order in wait sell list
                if direc == self.data.SEL:
                    if t_i.fundid in self.data.suspend_sel[d]:
                        self.wait_sel_list.append(t_i)
                        continue
            
                p = self.get_price(d, t_i.fundid)
                trade_fee = f_i.buy_fee if sign > 0 else f_i.sel_fee
                a_book = t_i.volume * p
                a_real = t_i.volume * p * (1+ (sign* trade_fee))
                self.bt_info.fee_history[d][t_i.fundid] =  t_i.volume * p *(sign* trade_fee)
                self.bt_info.fee_total += t_i.volume * p *(sign* trade_fee)
                pos_i.volume += t_i.volume
                pos_i.amount += a_book
                
                ## if sell, pay hold fee
                hold_fee_i = self.calculate_fund_hold_fee(t_i,direc,f_i,p,d)
                self.bt_info.hold_fee_total += hold_fee_i
                if self.cash_delay_con:
                    self.cash_delay_trade((a_real + hold_fee_i),sign)
                else:
                    self.bt_info.cash -= (a_real + hold_fee_i)
            
                t = BtElm(fundid=t_i.fundid, volume=t_i.volume,direction=direc,date=d,fund_price=p,amount=a_book, paired=False,sel_part=0,types=self.types)
                self.bt_info.trade_history.append(t)
            
            self.order_update()
            self.update_bt_info(d)    

    def backtest_report(self):
        self.mv_df = pd.DataFrame([ {'date':k, 'mv':v} for k,v in self.bt_info.index_market_value_history.items()]).set_index('date')
        year = len(self.data.date_list)/self.data.YEAR
        total_return = self.mv_df['mv'][-1] / self.mv_df['mv'][0]
        
        five_year_return = (self.mv_df['mv'][-1] / self.mv_df['mv'][-(5 * self.data.YEAR)] - 1)
        annualized_return = np.exp(np.log(total_return)/year) - 1
        annualized_volatiltity = (self.mv_df['mv'].shift(1) / self.mv_df['mv']).std() * np.sqrt((len(self.data.date_list) - 1) / year)
        sharpe = annualized_return / annualized_volatiltity
        mdd = 1 - (self.mv_df.loc[:, 'mv'] / self.mv_df.loc[:, 'mv'].rolling(10000, min_periods=1).max()).min()
        
        mdd_part1 = (self.mv_df.loc[:, 'mv'] / self.mv_df.loc[:, 'mv'].rolling(10000, min_periods=1).max())
        self.mdd_date1 = self.mv_df.loc[:mdd_part1.idxmin(),'mv'].idxmax()
        self.mdd_date2 = mdd_part1.idxmin()

    
        w = copy.deepcopy(self.weights)
        w['mdd'] = mdd
        w['annual_ret'] = annualized_return
        w['sharpe'] = sharpe
        w['5_year_ret'] = five_year_return
        w['annual_vol'] = annualized_volatiltity
        w['mdd_d1'] = self.mdd_date1
        w['mdd_d2'] = self.mdd_date2
        return w
        
    def backtest_plot(self):
        self.plot_asset_weights()
        self.plot_market_value()
        self.plot_individual_asset_market_value()
        self.plot_mdd_period_assets()
        
    def plot_asset_weights(self):
        res = []
        for d,k in self.bt_info.index_weights_history.items():
            k['date'] = d
            res.append(k)
        weights_df  = pd.DataFrame(res)
        weights_df.plot.area(figsize=(18,9),legend=False,fontsize = 13)
        l = pl.legend(loc='lower left',fontsize = 13)
        s = pl.title('asset weights', fontsize=20)

    def plot_market_value(self):    
        self.mv_df.plot.line(figsize=(18,9),legend=False,fontsize = 13)
        l = pl.legend(loc='lower left',fontsize = 13)
        s = pl.title('market value', fontsize=20)

    def plot_individual_asset_market_value(self):
        df = self.mv_df.join(self.data.index_data[[k for k, v in self.weights.items() ]]).fillna(method='bfill')
        (df /df.iloc[0]).plot.line(figsize=(18,9),legend=False,fontsize = 13)
        l = pl.legend(loc='lower left',fontsize = 13)
        s = pl.title('portfolio individual asset market value', fontsize=20)

    def plot_mdd_period_assets(self): 
        df = self.data.index_data.loc[self.mdd_date1:self.mdd_date2].fillna(method='bfill')
        (df /df.iloc[0]).plot.line(figsize=(18,9),legend=False,fontsize = 13)
        l = pl.legend(loc='lower left',fontsize = 13)
        s = pl.title('during mdd period  market value of all assets', fontsize=20)    


    def trade_history(self):
        
        if self.types == self.data.ASSET_BACKTEST:
            self.data.index_data.to_csv('index_data.csv',encoding='utf_8_sig')
            res = []
            for t_i in self.bt_info.trade_history:            
                dic = {'date':t_i.date,
                'volume':t_i.volume,
                'direction':t_i.direction,
                'index':t_i.fundid}
                res.append(dic)
            
            pd.DataFrame(res).to_csv('trade_history.csv',encoding='utf_8_sig')
            self.mv_df.to_csv('mv_result.csv',encoding='utf_8_sig')
        
        elif self.types == self.data.FUNDS_BACKTEST:
            self.mv_df = pd.DataFrame([ {'date':k, 'mv':v} for k,v in self.bt_info.market_value_history.items()]).set_index('date')
            self.mv_df.to_csv('mv_result1.csv',encoding='utf_8_sig')
            res = []
            for t_i in self.bt_info.trade_history:            
                dic = {'date':t_i.date,
                'volume':t_i.volume,
                'direction':t_i.direction,
                'index':t_i.fundid}
                res.append(dic)
            pd.DataFrame(res).to_csv('trade_history1.csv',encoding='utf_8_sig')
            res = []
            for f in self.data.fund_list:
                res.append(self.data.fund_nav[f].copy())
            pd.concat(res).to_csv('index_data1.csv',encoding='utf_8_sig')

    def plot_asset_values(self, df):
        '''
        dics = [{'annual_ret': 0.034514806571704026,
        'mdd': -0.07623285805103985,
        'asset': '国债指数'},
        {'annual_ret': 0.12193365001822731,
        'mdd': 0.679400930736562,
        'asset': '中证500'},
        {'annual_ret': 0.12886295097116807,
        'mdd': 0.7424266813566274,
        'asset': '房地产指数'},
        {'annual_ret': 0.097897023970132,
        'mdd': 0.7127346242058766,
        'asset': '沪深300'},
        {'annual_ret': 0.03988807981364406,
        'mdd': 0.30051710910407814,
        'asset': '黄金'},
        {'annual_ret': 0.048866700137312646,
        'mdd': -0.12132796780684085,
        'asset': '中证信用'},
        {'annual_ret': 0.0711921508500355,
        'mdd': 0.5031621107175719,
        'asset': '标普500人民币'},
        {'annual_ret': 0.03433924557450441,
        'mdd': 0.5627526169928608,
        'asset': '德标30人民币'},
        {'annual_ret': -0.006431133508941644,
        'mdd': 0.5356248109745954,
        'asset': '日经225人民币'}]
        df = pd.DataFrame(dics)
        '''
        colorlist = list(colors.ColorConverter.colors.keys())
        fig, ax = plt.subplots()
        [df.iloc[[i]].plot.scatter('mdd', 'annual_ret', ax=ax, s=200, label=l,
                                color=colorlist[15*i+20]) #% len(colorlist)])
        for i,l in enumerate(df.asset)]
        plt.title('asset annual_ret& mdd', fontsize=20)
        plt.legend(loc=2,fontsize=30)# prop={'fontsize': 20})

        ax.legend()
        plt.show()



if __name__ == "__main__":
    '''
    w = {
        '标普500人民币': 2/100,
        '国债指数':22/100,
        '中证500':16/100,
        '中证信用':60/100,
        }
    
    # asset allocation backtest
    begin_date = '20050101'
    bk = BacktestEngine(begin_date=begin_date,weights=w,types=DefaultData.ASSET_BACKTEST)
    bk.backtest()
    w = bk.backtest_report()
    print(w)
    '''
    w = {
        '标普500人民币': 2/100,
        '国债指数':22/100,
        '中证500':16/100,
        '中证信用':60/100,
        }
    begin_date = '20180402'
    bk = BacktestEngine(begin_date=begin_date,weights=w,types=DefaultData.FUNDS_BACKTEST)
    bk.backtest()




