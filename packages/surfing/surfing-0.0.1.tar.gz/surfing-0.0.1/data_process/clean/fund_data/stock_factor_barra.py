import numpy as np
import pandas as pd
from load_and_update_data.get_fund_data import DataLoader
import datetime
from pandas.core.common import SettingWithCopyError
from scipy.stats import pearsonr
from pyfinance.ols import PandasRollingOLS
import pymysql
import sqlalchemy
from sqlalchemy import create_engine
pd.options.mode.chained_assignment = 'raise'
import time

class Stock_Factor_Barra:
    
    MONTH = 20
    THREE_MONTH = 60
    YEAR = 242
    THREE_YEAR = 242 * 3
    
    def __init__(self, username, password, database, start_date, end_date):
        self.dl = DataLoader(username, password, database_name=database)
        self.start_date = start_date
        self.end_date = end_date
        self.start_date_q = self.get_date_q(start_date)
        self.end_date_q = self.get_date_q(end_date)
        self.market_index_id = '000300.XSHG'
        self.load_data()
        
        self.date_list = sorted(self.data_ret.index.tolist())
        self.fac_d_list = self.date_list[self.THREE_YEAR:]
        
    def load_data(self):
        self.data_size = self.dl.get_data('stock_valuation', 
                                       column_names=['market_cap_2', 'date', 'order_book_id'],
                                       aim_values=[self.start_date, self.end_date], 
                                       select_columns=['date', 'date'],
                                       operator=['>=', '<=']) 
        self.data_value = self.dl.get_data('stock_valuation', 
                                       column_names=['ep_ratio_ttm', 'date', 'order_book_id'],
                                       aim_values=[self.start_date, self.end_date], 
                                       select_columns=['date', 'date'],
                                       operator=['>=', '<=']) 
        self.data_turnover = self.dl.get_data('stock_turnover', 
                                       column_names=['year', 'date', 'order_book_id'],
                                       aim_values=[self.start_date, self.end_date], 
                                       select_columns=['date', 'date'],
                                       operator=['>=', '<='])
        self.data_quality = self.dl.get_data('stock_financial_indicator',
                                        column_names=['order_book_id','quarter','return_on_equity'],
                                        aim_values=[self.start_date_q, self.end_date_q], 
                                        select_columns=['quarter', 'quarter'],
                                        operator=['>=', '<='])
        
        self.data_hs300_ret = self.dl.get_data('index_price', column_names=['ret', 'date', 'close'], 
                                select_columns=['date', 'date', 'order_book_id'], 
                                aim_values=[self.start_date, end_date, self.market_index_id], 
                                operator=['>=', '<=', '='])
        
        self.data_quality = self.dl.get_data('stock_financial_indicator',
                                        column_names=['order_book_id','quarter','return_on_equity'],
                                        aim_values=[self.start_date_q, self.end_date_q], 
                                        select_columns=['quarter', 'quarter'],
                                        operator=['>=', '<='])
        self.data_leverage = self.dl.get_data('stock_balance_sheet',
                                              column_names = ['order_book_id','quarter','total_assets','total_equity'],
                                              aim_values=[self.start_date_q, self.end_date_q], 
                                                select_columns=['quarter', 'quarter'],
                                                operator=['>=', '<='])
        self.data_ret = self.dl.get_data('stock_daily_price',
                                                        column_names=['order_book_id','date','ret'],
                                                        aim_values=[self.start_date, self.end_date], 
                                                        select_columns=['date', 'date'],
                                                        operator=['>=', '<='])
        self.data_ret['ret'] = self.data_ret['ret'].astype('float')
        self.data_ret = self.data_ret.pivot_table(index='date', columns='order_book_id',values='ret')
        
        
        
    def get_date_q(self, date):
        q = int((int(date[4:6])-1 )/ 3)
        return date[:4]+'q'+str(q+1)
    
    def get_seasonal_data(self, df, fac_name, columns_name):
        # make seasonal data to date data 
        # 2010q1 -> 20100101~20100331
        season_dic = {
            '1' : ['0100','0332'],
            '2' : ['0400','0632'],
            '3' : ['0700','0932'],
            '4' : ['1000','1232'],
        }
        def filter_date(n):
            return n>date_range[0] and n<date_range[1]

        res = []
        f = fac_name
        
        dic_list = df.to_dict('records')
        for dic in dic_list:
            year = dic['quarter'].split('q')[0]
            season = dic['quarter'].split('q')[1]
            date_range = [year + _ for _ in season_dic[season]]
            season_d_list = list(filter(filter_date, self.date_list))
            res.extend([{f:dic[f],'date':_,'order_book_id':dic['order_book_id']}for _ in season_d_list])
        df = pd.DataFrame(res)
        df.columns = columns_name
        return df

    def factor_process(self, df):
 
        df.columns = ['factor_value','date','order_book_id'] 
        df['factor_value'] = df['factor_value'].astype(float)
        df['factor_value'] = df['factor_value'].replace(np.nan, 'None')
        df['factor_value'] = df['factor_value'].map(lambda x: str(round(x,4)) if not isinstance(x, str) else x)  
        return df
    
    def get_barra_size(self):
        #Size: log(market_cap_2)
        self.fac_size = self.data_size.copy()
        self.fac_size.columns = ['factor_value','date','order_book_id']
        self.fac_size['factor_value'] = np.log(self.fac_size['factor_value'].astype(float))
        self.fac_size['factor_value'] = self.fac_size['factor_value'].replace(np.nan, 'None')
        self.fac_size['factor_value'] = self.fac_size['factor_value'].map(lambda x: str(round(x,4)) if not isinstance(x, str) else x)  

    def get_barra_value(self): 
        #Value: ep_ratio_ttm
        self.fac_value = self.factor_process(self.data_value.copy())
        
    def get_barra_turnover(self):
        #TurnOver: last year turnover
        self.fac_turnover = self.factor_process(self.data_turnover.copy())
        
    def get_barra_quality(self):
        #Quality： return_on_equity
        self.data_quality['return_on_equity'] = self.data_quality['return_on_equity'].astype(float)
        self.data_quality = self.data_quality.pivot_table(index='quarter', columns='order_book_id',values='return_on_equity').fillna(method='ffill').stack().reset_index(level=[0,1])
        self.data_quality.columns = ['quarter','order_book_id','return_on_equity']
        
        self.fac_quality = self.get_seasonal_data(self.data_quality, 'return_on_equity', ['factor_value','date','order_book_id'])
        self.fac_quality['factor_value'] = self.fac_quality['factor_value'].astype(float).map(lambda x: str(round(x,4)) if not np.isnan(x) else 'None')  

    def get_barra_volatility(self):
        #Volatility: ret std
        self.fac_volatility = self.data_ret.rolling(self.YEAR, min_periods=self.YEAR).std()
        self.fac_volatility = self.fac_volatility[self.YEAR:].replace(np.nan, 'None')
        self.fac_volatility = self.fac_volatility.stack().reset_index(level=[0,1])
        self.fac_volatility.columns = ['date','order_book_id','factor_value']
        self.fac_volatility['factor_value'] = self.fac_volatility['factor_value'].map(lambda x: str(round(x,4)) if isinstance(x, float) else x)  

    def get_barra_shortmomentum(self):
        #ShortMomentum ： price change of 1 month
        self.fac_shortMomentum = self.data_ret.rolling(self.MONTH, min_periods=self.MONTH).sum()
        self.fac_shortMomentum = self.fac_shortMomentum[self.MONTH:].replace(np.nan, 'None')
        self.fac_shortMomentum = self.fac_shortMomentum.stack().reset_index(level=[0,1])
        self.fac_shortMomentum.columns = ['date','order_book_id','factor_value']
        self.fac_shortMomentum['factor_value'] = self.fac_shortMomentum['factor_value'].map(lambda x: str(round(x,4)) if isinstance(x, float) else x) 

    def get_barra_longmomentum(self):
        #LongMomentum：  price change of 3 years
        self.fac_longMomentum = self.data_ret.rolling(self.THREE_YEAR, min_periods=self.THREE_YEAR).sum()
        self.fac_longMomentum = self.fac_longMomentum[self.THREE_YEAR:].replace(np.nan, 'None')
        self.fac_longMomentum = self.fac_longMomentum.stack().reset_index(level=[0,1])
        self.fac_longMomentum.columns = ['date','order_book_id','factor_value']
        self.fac_longMomentum['factor_value'] = self.fac_longMomentum['factor_value'].map(lambda x: str(round(x,4)) if isinstance(x, float) else x)

    def get_barra_leverage(self):
        #Leverage  total_assets/total_equity
        self.data_leverage['leverage'] = self.data_leverage['total_assets'] / self.data_leverage['total_equity']
        self.data_leverage['leverage'] = self.data_leverage['leverage'].astype(float)
        self.data_leverage = self.data_leverage.pivot_table(index='quarter', columns='order_book_id',values='leverage').fillna(method='ffill').stack().reset_index(level=[0,1])
        self.data_leverage.columns = ['quarter','order_book_id','leverage']
        self.fac_leverage = self.get_seasonal_data(self.data_leverage, 'leverage', ['factor_value','date','order_book_id'])
        self.fac_leverage = self.fac_leverage.replace(np.nan, 'None')
        self.fac_leverage['factor_value'] = self.fac_leverage['factor_value'].map(lambda x: str(round(x,4)) if isinstance(x, float) else x)


    def get_barra_beta(self):
        #Beta passed 242days  linear regresion coef  y: stock ret  x hs300 ret 
        self.data_hs300_ret['ret'] = self.data_hs300_ret['ret'].astype(float)
        id_list = self.data_ret.columns.tolist()
        res = []
        for i in id_list:
            x = self.data_hs300_ret['ret']
            y = self.data_ret[i]
            model = PandasRollingOLS(y=y, x=x, window=self.YEAR)
            res_i = model.beta['feature1'].values.tolist()
            res.append(res_i)
            if id_list.index(i) == 0:
                date_list =  model.beta.index.tolist()
        self.fac_beta = pd.DataFrame(res).T
        self.fac_beta.columns = id_list
        self.fac_beta.index = date_list
        self.fac_beta = self.fac_beta.replace(np.nan, 'None')
        self.fac_beta = self.fac_beta.stack().reset_index(level=[0,1])
        self.fac_beta.columns = ['date','order_book_id','factor_value']
        self.fac_beta['factor_value'] = self.fac_beta['factor_value'].map(lambda x: str(round(x,4)) if isinstance(x, float) else x)

    def get_history(self):
        self.get_barra_size()
        self.get_barra_value()
        self.get_barra_turnover()
        self.get_barra_quality()
        self.get_barra_volatility()
        self.get_barra_shortmomentum()
        self.get_barra_longmomentum()
        self.get_barra_leverage()
        self.get_barra_beta()

if __name__ == "__main__":
    username = 'huangkejia'
    password = 'Huangkejia123456'
    database = 'quant_data'

    # barra_longmomentum needs data range at least 3 year
    # if test start_date = '20170101' end_date='20200201' 
    start_date = '20150101'
    end_date = '20200201'
    engine = create_engine('mysql+pymysql://huangkejia:Huangkejia123456@fundinfo.cq1tbd5lkqzo.rds.cn-northwest-1.amazonaws.com.cn:3306/factor')

    barra = Stock_Factor_Barra(username = username,
                   password = password,
                   database = database,
                   start_date = start_date,
                   end_date = end_date,
                   )
    barra.get_history()

    # save data to mysql    
    barra.fac_size.to_sql('stock_barra_size', engine, index=False)
    barra.fac_value.to_sql('stock_barra_value', engine, index=False)
    barra.fac_turnover.to_sql('stock_barra_turnover', engine, index=False)
    barra.fac_quality.to_sql('stock_barra_quality', engine, index=False)
    barra.fac_volatility.to_sql('stock_barra_volatility', engine, index=False)
    barra.fac_shortMomentum.to_sql('stock_barra_shortMomentum', engine, index=False)
    barra.fac_longMomentum.to_sql('stock_barra_longMomentum', engine, index=False)
    barra.fac_leverage.to_sql('stock_barra_leverage', engine, index=False)
    barra.fac_beta.to_sql('stock_barra_beta', engine, index=False)