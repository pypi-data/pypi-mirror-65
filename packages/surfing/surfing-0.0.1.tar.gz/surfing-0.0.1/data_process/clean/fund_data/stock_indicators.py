import numpy as np
import pandas as pd
from load_and_update_data.get_fund_data import DataLoader
import datetime
from pandas.core.common import SettingWithCopyError
from scipy.stats import pearsonr
import pymysql
import sqlalchemy
from sqlalchemy import create_engine
import time
pd.options.mode.chained_assignment = 'raise'

class Stock_Indicators:
    
    
    '''
    ###
    主要输入：
    测试的因子数据： 为米筐市值因子：market_cap
    
    按照研报估值可以采用PE 或者PB ，对应米筐为以下五个
    pe_ratio_lyr pe_ratio_ttm pb_ratio_lyr pb_ratio_ttm pb_ratio_lf
    当前测试估值为pe_ratio_lyr

    long_method short_method 表示多头空头时，因子取大或者取小

    rank 可表示多空头的比例或者只数 如 '10%' 100
    time_windows  pairwise_correlation long_term_factor_ret factor_volatility 算三个因子时的回溯时间窗口大小

    corr_time_windows 最后算因子拥挤和未来因子收益时的 时间窗口

    ret_method 选择'LONG_SHORT' 或者 'LONG_AVERAGE'
        LONG_SHORT 因子当日收益为 多头选股收益均值 - 空头选股收益均值
        LONG_AVERAGE 因子当日收益为 多头选股收益均值 - 当日所有股票收益均值

    ###
    4种估值 方法计算
    valuation_spread(date)   当日 log(多头估值和 / 空头估值和)
    
    pairwise_correlation(date,time_windows)  当前向之前推time_windows日的收益序列， 
    因子多头收益均值 和 多头选股i收益 的 pearsonr 相关系数 的均值
    减去 因子空头收益均值 和 空头选股i收益 的 pearsonr 相关系数 的均值

    long_term_factor_ret(date,time_windows)  当前向之前推time_windows日的收益序列，
    每日因子多头收益的总和

    factor_volatility(date,time_windows)  当前向之前推time_windows日的收益序列，
    vol(因子多头收益) / vol（因子空头收益）

    ###
    因子拥挤与未来收益的相关性
    val_ret_corr(date,corr_time_windows)
        因子拥挤选取上述4种， 分别算出当日向前推corr_time_windows 时间窗口的因子序列，
        算当前向未来推corr_time_windows时间窗口的因子收益
        算pearsonr correlation
    

    '''

    
    def __init__(self, username, password, database, start_date, end_date,long_method,short_method,factor_name,valuation_name,rank,time_windows,corr_time_windows,ret_method):
        self.dl = DataLoader(username, password, database_name=database)
        self.start_date = start_date
        self.end_date = end_date
        self.long = long_method
        self.short = short_method
        self.factor_name = factor_name
        self.valuation_name = valuation_name
        self.rank = rank
        self.time_windows = time_windows
        self.corr_time_windows = corr_time_windows
        self.ret_method = ret_method

        self.valuation = self.dl.get_data('stock_valuation', 
                                       column_names=[self.valuation_name, 'date', 'order_book_id'],
                                       aim_values=[self.start_date, self.end_date], 
                                       select_columns=['date', 'date'],
                                       operator=['>=', '<=']) 
        self.valuation[self.valuation_name] = self.valuation[self.valuation_name].astype(float)
        self.valuation = self.valuation.pivot_table(index='date', columns='order_book_id',values=self.valuation_name)
        self.valuation = self.valuation.fillna(method='ffill').fillna(method='bfill')
        
        self.stock_price = self.dl.get_data('stock_daily_price',
                                           column_names=['order_book_id', 'date', 'ret'],
                                           aim_values=[self.start_date.replace('-',''), self.end_date.replace('-','')], 
                                           select_columns=['date', 'date'],
                                           operator=['>=', '<=']
                                           )
        self.stock_price['ret'] = self.stock_price['ret'].astype(float)
        self.stock_price = self.stock_price.pivot_table(index='date', columns='order_book_id',values='ret')
        
        self.date_list = sorted(self.stock_price.index.tolist())
        if isinstance(self.rank, int):
           
            self.rank = self.rank
            
        elif isinstance(self.rank, str):
            self.rank = int(self.rank.split('%')[0])
            self.rank_pct = self.rank/100
            self.rank = int(self.stock_price.shape[1] / self.rank)
            
    def input_factor(self, test_df):
        self.factor = test_df
        self.factor = self.factor.pivot_table(index='date', columns='order_book_id',values='factor_value')
        self.factor = self.factor.fillna(method='ffill').fillna(method='bfill')
        fac_data = []
        for index, row in self.factor.iterrows():
            today_ret = self.stock_price.loc[index, : ]
            today_trade = today_ret.dropna().index
            rank_tmp = int(len(today_trade) * self.rank_pct)
            row = row[~np.isnan(row)].sort_values()
            row = row[row.index.isin(today_trade)]
            dic= {} 
            dic['date'] = index
            dic['BIG'] = row.index[-rank_tmp:].values
            dic['SMALL'] = row.index[:rank_tmp].values

            dic['longs_rets'] = today_ret[today_ret.index.isin(dic[self.long])].fillna(0).values
            dic['longs_ret'] = dic['longs_rets'].mean()
            dic['short_rets'] = today_ret[today_ret.index.isin(dic[self.short])].fillna(0).values
            dic['short_ret'] = dic['short_rets'].mean()

            dic['LONG_SHORT'] = dic['longs_ret'] - dic['short_ret']
            dic['LONG_AVERAGE'] = dic['short_ret'] - today_ret.fillna(0).mean()

            fac_data.append(dic)
        self.fac_df = pd.DataFrame(fac_data)
        self.fac_df.index = self.fac_df['date']
    
    
    def find_data_date(self, df, date):
        return df[df['date'] == date].copy()
                        
    def get_factor_side(self, df, side):
        df.loc[:,self.factor_name] = df[self.factor_name].astype(float).copy()
        df = df.dropna()       
        if isinstance(self.rank, int):
            pass
        elif isinstance(self.rank, str):
            self.rank = int(self.rank.split('%')[0])
            self.rank = int(df.shape[0] / self.rank)
        if side == 'BIG':
            return df.sort_values([self.factor_name])['order_book_id'][:self.rank].values
        elif side == 'SMALL':
            return df.sort_values([self.factor_name])['order_book_id'][-self.rank:].values
    
    def valuation_spread(self, date):

        factor_df = self.find_data_date(self.factor, date)
        longs_stock = self.get_factor_side(factor_df.copy(), self.long)
        short_stock = self.get_factor_side(factor_df.copy(), self.short)
        long_val = self.valuation[self.valuation.index==date][longs_stock].sum(axis=1).values[0]
        short_val = self.valuation[self.valuation.index==date][short_stock].sum(axis=1).values[0]
        return np.log(long_val/short_val)
    
    def factor_ret(self, date):
        factor_df = self.find_data_date(self.factor, date)
        ret_df = self.find_data_date(self.stock_price, date.replace('-',''))
        longs_stock = self.get_factor_side(factor_df.copy(), self.long)
        long_ret = ret_df[ret_df['order_book_id'].isin(longs_stock)].ret.mean()
        if self.ret_method == 'LONG_SHORT':
            short_stock = self.get_factor_side(factor_df.copy(), self.short)
            short_ret = ret_df[ret_df['order_book_id'].isin(short_stock)].ret.mean()
            return long_ret - short_ret
        elif self.ret_method == 'LONG_AVERAGE':
            average_ret = ret_df.ret.mean()
            return long_ret - average_ret
    
    def factor_ret_group(self, date):
        factor_df = self.find_data_date(self.factor, date)
        ret_df = self.find_data_date(self.stock_price, date)
        longs_stock = self.get_factor_side(factor_df.copy(), self.long)
        long_rets = ret_df[ret_df['order_book_id'].isin(longs_stock)].ret
        long_rets_list = long_rets.tolist()
        long_ret = long_rets.mean()
        
        short_stock = self.get_factor_side(factor_df.copy(), self.short)
        short_rets = ret_df[ret_df['order_book_id'].isin(short_stock)].ret
        short_rets_list = short_rets.tolist()
        short_ret = short_rets.mean()
        return [long_ret,long_rets_list, short_ret, short_rets_list]
    
    def pairwise_correlation(self, date):
        d_list = self.date_list[self.date_list.index(date) - self.time_windows+1 :self.date_list.index(date)+1]
        dic = {
            'longs_ret' : [],
            'short_ret' : [],
            'longs_rets' : [],
            'short_rets' : [],
        }
        for d in d_list:
            lr, lrs, sr, srl = self.factor_ret_group(d)
            dic['longs_ret' ].append(lr)
            dic['longs_rets'].append(lrs)
            dic['short_ret' ].append(sr)
            dic['short_rets'].append(srl)
        longs_corr = []
        short_corr = []
        for i in range(len(lrs)):
            longs_ret_i = [_[0] for _ in dic['longs_rets']]
            longs_corr.append(pearsonr(longs_ret_i,dic['longs_ret'])[0])

            short_ret_i = [_[0] for _ in dic['short_rets']]
            short_corr.append(pearsonr(short_ret_i,dic['short_ret'])[0])
        return np.mean(longs_corr) - np.mean(short_corr)
    
    def long_term_factor_ret(self, date):
        d_list = self.date_list[self.date_list.index(date) - self.time_windows+1 :self.date_list.index(date)+1]
        long_ret = []
        for d in d_list:
            long_ret.append(self.factor_ret( d))
        return np.sum(long_ret)
        
    def factor_volatility(self, date):
        d_list = self.date_list[self.date_list.index(date) - self.time_windows+1 :self.date_list.index(date)+1]
        longs_ret = []
        short_ret = []

        for d in d_list:
            lr, lrs, sr, srl = self.factor_ret_group(d)
            longs_ret.append(lr)
            short_ret.append(sr)
        return np.std(longs_ret) / np.std(short_ret)
    
    def val_ret_corr(self, date):
        d_list1 = self.date_list[self.date_list.index(date) - self.corr_time_windows+1 :self.date_list.index(date)+1]
        d_list2 = self.date_list[self.date_list.index(date) +1 :self.date_list.index(date)+1+self.corr_time_windows]
        
        dic = {'valuation_spread' : [],
               'pairwise_correlation': [],
               'long_term_factor_ret':[],
               'factor_volatility' :[]}
        for d in d_list1:
            dic['valuation_spread'].append(self.valuation_spread(d))
            dic['pairwise_correlation'].append(self.pairwise_correlation(d))
            dic['long_term_factor_ret'].append(self.long_term_factor_ret(d))
            dic['factor_volatility'].append(self.factor_volatility(d))
        
        rets = [self.factor_ret(d) for d in d_list2]

        corr_val_spread_ret = pearsonr(dic['valuation_spread'], rets)[0]
        corr_pairwise_ret = pearsonr(dic['pairwise_correlation'], rets)[0]
        corr_long_factor_ret_ret = pearsonr(dic['long_term_factor_ret'], rets)[0]
        corr_fac_vol_ret = pearsonr(dic['factor_volatility'], rets)[0]
        return   corr_val_spread_ret, corr_pairwise_ret, corr_long_factor_ret_ret, corr_fac_vol_ret 

    def get_all(self):
        res = []
        for d in self.date_list[self.time_windows:]:
            if d > self.fac_df.date.max():
                continue
            dic = {}
            fac_today = self.fac_df.loc[d,:]
            val_today = self.valuation.loc[d,:]
            longs_stock = fac_today[self.long]
            short_stock = fac_today[self.short]
            longs_val_mean = val_today[val_today.index.isin(longs_stock)].mean()
            short_val_mean = val_today[val_today.index.isin(short_stock)].mean()
            dic['date'] = d
            dic['valuation_spread']  = longs_val_mean - short_val_mean
            begin_d = self.date_list[self.date_list.index(d)-self.time_windows+1]
            df_range = self.fac_df.loc[begin_d:d,:]
            longs_corr = []
            short_corr = []
            range_1 = min([len(i) for i in df_range['longs_rets']])
            range_2 = min([len(i) for i in df_range['short_rets']])
            range_i = min(range_1,range_2)
            if range_i < 0.5* self.rank:
                dic['pairwise_correlation'] = np.nan
            else:
                for i in range(range_i):
                    longs_ret_i = [j[i] for j in df_range['longs_rets']]
                    longs_corr.append(pearsonr(pd.Series(longs_ret_i).fillna(0),df_range['longs_ret'].fillna(0))[0])
                    short_ret_i = [j[i] for j in df_range['short_rets']]
                    short_corr.append(pearsonr(pd.Series(short_ret_i).fillna(0),df_range['short_ret'].fillna(0))[0])
                dic['pairwise_correlation'] = np.mean(pd.Series(longs_corr).fillna(0)) - np.mean(pd.Series(short_corr).fillna(0))
            dic['long_term_factor_ret'] = df_range[self.ret_method].sum()
            dic['factor_volatility'] = (np.std(df_range['longs_ret']) + 0.001) / (np.std(df_range['short_ret'])+ 0.001)
            res.append(dic)
        return pd.DataFrame(res).replace(1, np.nan)

if __name__ == "__main__":
    
    username = 'huangkejia'
    password = 'Huangkejia123456'
    database = 'quant_data'
    factorbase = 'factor'
    start_date = '20170101'
    end_date = '20200123'
    factor_name_list = ['stock_barra_beta','stock_barra_longMomentum','stock_barra_leverage','stock_barra_quality','stock_barra_shortMomentum','stock_barra_size','stock_barra_turnover','stock_barra_value','stock_barra_volatility']
    # pe_ratio_lyr pe_ratio_ttm pb_ratio_lyr pb_ratio_ttm pb_ratio_lf    
    valuation_name = 'ep_ratio_lyr'
    long_method  =  'BIG'
    short_method =  'SMALL'
    # input string  or int  '10%' or 100
    rank = '10%'
    time_windows = 20*3
    corr_time_windows = 20*3
    # LONG_SHORT LONG_AVERAGE
    ret_method = 'LONG_SHORT'
    factor_name_input = 'factor_value'
    si = Stock_Indicators(username=username,
                        password=password, 
                        database=database,
                        start_date=start_date,
                        end_date=end_date,
                        long_method=long_method,
                        short_method=short_method,
                        factor_name=factor_name_input,
                        valuation_name=valuation_name,
                        rank=rank,
                        time_windows=time_windows,
                        corr_time_windows=corr_time_windows,
                        ret_method = ret_method) 

    engine = create_engine('mysql+pymysql://huangkejia:Huangkejia123456@fundinfo.cq1tbd5lkqzo.rds.cn-northwest-1.amazonaws.com.cn:3306/derived_data')

    for factor_name in factor_name_list:
        test_factor = DataLoader(username, password, database_name=factorbase).get_data(factor_name, 
                                            aim_values=[start_date, end_date], 
                                            select_columns=['date', 'date'],
                                            operator=['>=', '<='])

        test_factor['factor_value'] = test_factor['factor_value'].map(lambda x: np.nan if x == 'None' else float(x))
        test_factor = test_factor.fillna(method='ffill').fillna(method='bfill')
        si.input_factor(test_factor)
        df_factor = si.get_all()
        table_name = 'factor_crowding_'+factor_name
        df_factor.to_sql(table_name, engine, index=False)
        print(factor_name, ' finished')
        