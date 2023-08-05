import numpy as np
import pandas as pd
import rqdatac as rq
from rqdatac import fund
import datetime
from pprint import pprint 
import pymysql
import sqlalchemy
from sqlalchemy import create_engine
import time

engine = create_engine('mysql+pymysql://huyunfan:Huyunfan123456@fundinfo.cq1tbd5lkqzo.rds.cn-northwest-1.amazonaws.com.cn:3306/quant_data')

class FundDownloadUtility:

    def __init__(self, path='rice_data/fund/', date_s='20191201', date_e='20200120'):
        rq.init()
        self.object_tb = rq.all_instruments()

        self.LOF_list = [x.split('.')[0] for x in self.object_tb[self.object_tb['type'] == 'LOF']['order_book_id'].values]
        self.ETF_list = [x.split('.')[0] for x in self.object_tb[self.object_tb['type'] == 'ETF']['order_book_id'].values]
        self.fund_list = np.concatenate((self.LOF_list, self.ETF_list))
        self.path = path
        self.date_s = date_s
        self.date_e = date_e
        self.manager_list = []
        self.money_fund_list = []
        
        self.date_list = self.get_date_list()
    
    def get_date_list(self):
        index_close = rq.get_price(order_book_ids='000016.XSHG', start_date=self.date_s, end_date=self.date_e, frequency='1d')['close']
        return index_close.index.tolist()

    def date_yielder(self, step=10):
        lenth = len(self.date_list)
        if step > lenth:
            print('Invalid step number')
            return
        pre = 0
        index = step
        while True:
            yield self.date_list[pre:index]
            pre = index
            index += step
            if index > lenth:
                index = lenth
                yield self.date_list[pre:index]
                break
        return


    def df_to_sqltable(self, df, name, if_exists='append', set_datetime=False):
        if not set_datetime:
            if 'datetime' in df.columns:
                df.drop(columns=['datetime'], inplace=True)
        df.to_sql(name, engine, index=False, if_exists=if_exists)



    def get_nav(self, download=True, set_date=False, date_s=None, date_e=None):
        cur_start = self.date_s
        cur_end = self.date_e
        if set_date:
            cur_start = date_s
            cur_end = date_e
        for d in reversed(self.date_list):
            pd_list = []
            t0 = time.time()
            print(d)
            for f in self.fund_list:
                cur_pd = fund.get_nav(f, d, d, expect_df=True)
                if cur_pd is None:
                    continue
                cur_pd.reset_index(inplace=True)
                pd_list.append(cur_pd)
            if len(pd_list) < 1:
                continue
            full_tb = pd.concat(pd_list)
            full_tb['datetime'] = full_tb['datetime'].map(lambda x: x.strftime('%Y%m%d'))
            #self.df_to_sqltable(full_tb, 'nav', set_datetime=True)
            print('finish date: ' , d, 'cost time :  ', time.time() - t0)

if __name__ == "__main__":
    path   = '/Users/huangkejia/data/rq_fund'
    date_s = '20041201'
    date_e = '20041217'
    fund_data = FundDownloadUtility(path=path,date_s=date_s,date_e=date_e)
    fund_data.get_nav()
    