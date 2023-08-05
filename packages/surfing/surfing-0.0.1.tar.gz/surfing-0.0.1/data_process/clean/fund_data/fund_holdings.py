import numpy as np
import pandas as pd
from load_and_update_data.get_fund_data import DataLoader
import datetime
from pandas.core.common import SettingWithCopyError
from scipy.stats import pearsonr
from pyfinance.ols import PandasRollingOLS
pd.options.mode.chained_assignment = 'raise'
import rqdatac as rq
import time
import numpy as np
import pandas as pd
import pymysql
import sqlalchemy
from sqlalchemy import create_engine
import time
engine = create_engine('mysql+pymysql://huangkejia:Huangkejia123456@fundinfo.cq1tbd5lkqzo.rds.cn-northwest-1.amazonaws.com.cn:3306/derived_data')


class Fund_Holds:
    
    def __init__(self, username, password, database, start_date, end_date):
        self.dl = DataLoader(username, password, database_name=database)
        self.start_date = start_date
        self.end_date = end_date
        self.load_data()
        
    def load_data(self):
        self.fund_holds = self.dl.get_data('holdings', 
                                   column_names=['order_book_id','share_order_book_id','type','weight','category','release_date'],
                                   aim_values=[self.start_date, self.end_date], 
                                   select_columns=['release_date', 'release_date'],
                                   operator=['>=', '<=']) 
        self.stock_value = self.dl.get_data('stock_valuation', 
                                       column_names=['market_cap_2', 'date', 'order_book_id'],
                                       aim_values=[self.start_date, self.end_date], 
                                       select_columns=['date', 'date'],
                                       operator=['>=', '<=']) 
        self.date_list = np.array(sorted(list(set(self.stock_value.date))))
        self.fund_share = self.fund_holds[self.fund_holds['type'] == 'Share']
        self.fund_bond = self.fund_holds[self.fund_holds['type'] == 'Bond']
        
    def find_recent_date(self, date_i):
        return self.date_list[self.date_list<=date_i].tolist()[-1]
    
    
    def find_style(self, cap):
        barrier = [300, 50]
        if cap >= barrier[0]:
            return 'big'
        elif cap < barrier[1]:
            return 'small'
        else:
            return 'medium'
        
    def find_share_stype(self):
        res = []
        bug = []
        for name, group in self.fund_share.groupby(['order_book_id','release_date']):
            try:
                date_max = self.find_recent_date(name[1])
                df_tmp = self.stock_value[self.stock_value['date'] == date_max]
                df_tmp = df_tmp[df_tmp['order_book_id'].isin(group['share_order_book_id'])].sort_values(['order_book_id'])
                cap = np.dot((df_tmp['market_cap_2'].astype(float))/1e8 , group['weight'].astype('float') / (group['weight'].sum()))
                res.append({
                    'order_book_id':name[0],
                    'date':name[1],
                    'weighted_cap':cap,
                    'style': self.find_style(cap)})
            except:
                # h share 
                bug.append([name,group])
        
        df = pd.DataFrame(res)
        df.to_sql('fund_style', engine, index=False)
        
if __name__ == "__main__":
    username = 'huangkejia'
    password = 'Huangkejia123456'
    database = 'quant_data'
    start_date = '20150201'
    end_date = '20200201'

    fh = Fund_Holds(username, password, database, start_date, end_date)
    fh.find_share_stype()
    