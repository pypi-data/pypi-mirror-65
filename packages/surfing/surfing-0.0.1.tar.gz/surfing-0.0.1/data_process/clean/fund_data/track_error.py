import numpy as np
import pandas as pd
from load_and_update_data.get_fund_data import DataLoader
import pymysql
import sqlalchemy
from sqlalchemy import create_engine
import datetime
import calendar

class Track_Error_Loader:
    def __init__(self, start_year, start_quarter, end_year, end_quarter, interval_list, fund_list=None, dl=None, engine=None):
        self.start_year = start_year
        self.start_quarter = start_quarter
        self.end_year = end_year
        self.end_quarter = end_quarter
        if dl is None:
            self.dl = DataLoader('huyunfan', 'Huyunfan123456')
        else:
            self.dl = dl
        self.year_co = 242
        self.interval_list = interval_list
        max_interval = max(interval_list)
        
        print("load_data")
        if fund_list is None:
            sql = 'select fund_id, asset_type from quant_data.fund_tag where asset_type is not null'
            self.fund_df = self.dl.get_data_from_sql(sql)
        else:
            strlist = ','.join(["'" + fund_id + "'" for fund_id in fund_list])
            sql = "select fund_id, asset_type from quant_data.fund_tag \
            where fund_id in ({}) and asset_type is not null".format(strlist)
            self.fund_df = self.dl.get_data_from_sql(sql)
        
        data_date_s = self.get_date_str(start_year - max_interval, start_quarter)
        data_date_e = self.get_date_str(end_year, end_quarter)
        
        self.fund_list = self.fund_df['fund_id'].values
        str_fund = ','.join(["'" + fund_id + "'" for fund_id in self.fund_list])
        sql_price = "select change_rate, `datetime`, fund_id from quant_data.nav \
        where fund_id in ({}) and `datetime`>={} and `datetime`<={}".format(str_fund, data_date_s, data_date_e)
        self.fund_price = self.dl.get_data_from_sql(sql_price)
        
        sql_index = "select * from quant_data.index_ret where `date`>={} and `date`<={}".format(data_date_s, data_date_e)
        self.index_df = self.dl.get_data_from_sql(sql_index)
        
        if engine is None:
            print('load engine')
            self.engine = create_engine('mysql+pymysql://zhangyunfan:Zhangyunfan123456@fundinfo.cq1tbd5lkqzo.rds.cn-northwest-1.amazonaws.com.cn:3306/derived_data', pool_recycle=1)
        else:
            self.engine = engine

    def get_date_str(self, year=None, quarter=None):

            if quarter == 1:
                q_str = '0331'
            elif quarter == 2:
                q_str = '0630'
            elif quarter == 3:
                q_str = '0930'
            elif quarter == 4:
                q_str = '1231'
            else:
                return None

            if year is not None:
                return str(year) + q_str
            return q_str

    def quarter_upload(self):
        cur_year = self.start_year
        cur_quarter = self.start_quarter
        while cur_year <= self.end_year and cur_quarter <= self.end_quarter:

            print('calcalate:' + str(cur_year) + 'q' + str(cur_quarter))
            for intv in self.interval_list:
                print(intv)
                cur_df = self.track_cal(cur_year, cur_quarter, intv)
                print('upload')
                while True:
                    try:
                        cur_df.to_sql('track_error', self.engine, index=False, if_exists='append')
                        break
                    except Exception as e:
                        print(e)
                        continue

            cur_quarter += 1
            if cur_quarter > 4:
                cur_year += 1
                cur_quarter = 1
    
    @staticmethod
    def at2col(asset_type):
        if asset_type == 'A股大盘':
            return '沪深300'
        elif asset_type == 'A股中盘':
            return '中证500'
        elif asset_type == '美股大盘':
            return '标普500人民币'
        elif asset_type == '创业板':
            return '创业板指'
        elif asset_type == '德国大盘':
            return '德标30人民币'
        elif asset_type == '日本大盘':
            return '日经225人民币'
        elif asset_type == '利率债':
            return '国债指数'
        elif asset_type == '信用债':
            return '中证信用'
        elif asset_type == '黄金':
            return '黄金'
        elif asset_type == '原油':
            return '石油'
        elif asset_type == '房地产':
            return '房地产指数'
    
    def track_cal(self, cur_year, cur_quarter, interval):
        cur_date = self.get_date_str(cur_year, cur_quarter)
        pre_date = self.get_date_str(cur_year - interval, cur_quarter)

        te_list = []
        for fund_id, asset_type in self.fund_df.values:

            cur_fund_tb = self.fund_price[(self.fund_price['fund_id'] == fund_id) & 
            (self.fund_price['datetime'] >= pre_date) & (self.fund_price['datetime'] <= cur_date)].drop(columns=['fund_id'])
            cur_fund_tb['change_rate'] = cur_fund_tb['change_rate'].astype(float)

            cur_idx_col = self.at2col(asset_type)
            cur_index_tb = self.index_df[(self.index_df['date'] >= pre_date) & 
            (self.index_df['date'] <= cur_date)][[cur_idx_col, 'date']]
            cur_index_full = cur_index_tb[[x is not None for x in cur_index_tb[cur_idx_col].values]]

            merged_tb = cur_fund_tb.merge(cur_index_full, how='inner', left_on='datetime', right_on='date').drop(columns=['date'])
            cur_len = merged_tb.shape[0]
            if cur_len <= 0:
                continue
            te = (self.year_co * ((merged_tb['change_rate'] - merged_tb[cur_idx_col]) ** 2).sum() / cur_len) ** 0.5
            
            te_list.append([fund_id, te])
        
        te_tb = pd.DataFrame(te_list, columns=['fund_id', 'track_error'])
        te_tb['datetime'] = cur_date
        te_tb['timespan'] = interval

        te_tb.drop_duplicates(['fund_id', 'datetime'], inplace=True)

        return te_tb


if __name__ == '__main__':
    # 从不同间隔计算基础指标
    tel = Track_Error_Loader(2018, 1, 2019, 4, [1, 3, 5])
    tel.quarter_upload()
