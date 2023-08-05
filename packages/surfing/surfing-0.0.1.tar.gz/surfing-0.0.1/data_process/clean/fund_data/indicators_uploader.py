import numpy as np
import pandas as pd
from fund_indicators import fund_indicators
from index_indicators import index_indicators
from load_and_update_data.get_fund_data import DataLoader
import pymysql
import sqlalchemy
from sqlalchemy import create_engine
import datetime
import calendar
from track_error import Track_Error_Loader


class Indicators_Uploader:
    def __init__(self, start_year, start_quarter, end_year, end_quarter, table, interval=1, fund_list=None):
        self.start_year = start_year
        self.start_quarter = start_quarter
        self.end_year = end_year
        self.end_quarter = end_quarter
        self.dl = DataLoader('huyunfan', 'Huyunfan123456')
        self.market_index_id = '000300.XSHG'
        self.interval = interval
        self.table = table
        if start_quarter == 1:
            data_date_s = self.get_date_str(start_year - (self.interval + 1), 3)
        else:
            data_date_s = self.get_date_str(start_year - self.interval, start_quarter - 1)
        data_date_e = self.get_date_str(end_year, end_quarter)
        print('load data')
        if fund_list is None:
            self.fund_price_info = self.dl.get_data('nav', column_names=['change_rate', 'datetime', 'adjusted_net_value', 'fund_id'], 
                            select_columns=['datetime', 'datetime'], 
                            aim_values=[data_date_s, data_date_e], 
                            operator=['>=', '<=']).sort_values(by=['datetime'], ignore_index=True, ascending=True)
            self.fund_list = self.fund_price_info['fund_id'].unique()
        else:
            self.fund_list = fund_list
            strlist = ','.join(["'" + fund_id + "'" for fund_id in self.fund_list])
            sql = "select change_rate, `datetime`, adjusted_net_value, fund_id from quant_data.nav \
                    where `datetime`>={} and `datetime`<={} and fund_id in ({})".format(data_date_s, data_date_e, strlist)
            self.fund_price_info = self.dl.get_data_from_sql(sql)

        self.index_price_info = self.dl.get_data('index_price', column_names=['ret', 'date', 'close'], 
                                    select_columns=['date', 'date', 'order_book_id'], 
                                    aim_values=[data_date_s, data_date_e, self.market_index_id], 
                                    operator=['>=', '<=', '=']).sort_values(by=['date'], ignore_index=True, ascending=True)
        self.trading_date = self.index_price_info['date'].to_frame()
        print('load indicators class')
        self.indicators = {}
        fund_start_date = self.get_date_str(start_year - self.interval, start_quarter)
        fund_end_date = data_date_e
        for fund_id in self.fund_list:
            cur_fund_tb = self.fund_price_info[self.fund_price_info['fund_id'] == fund_id].drop(columns=['fund_id'])
            new_fi = fund_indicators(fund_start_date, fund_end_date, fund_id, 
            trans_data=(self.trading_date, cur_fund_tb, self.index_price_info),
            dataloader=self.dl)
            self.indicators[fund_id] = new_fi
        print('load engine')
        self.engine = create_engine('mysql+pymysql://zhangyunfan:Zhangyunfan123456@fundinfo.cq1tbd5lkqzo.rds.cn-northwest-1.amazonaws.com.cn:3306/derived_data', pool_recycle=1)
        self.tb_columns = ['fund_id', 'datetime', 'beta', 'alpha', 'treynor_ratio', 'max_dd', 
        'downside_risk', 'return_over_period', 'annualized_average_daily_return', 'volatility', 'm_square',
        'time_return', 'value_at_risk', 'r_square', 'sharp_ratio', 'treynor_mazuy_coefficient', 'fee_rate']
        print('load track error class')
        self.te = Track_Error_Loader(self.start_year, self.start_quarter, self.end_year, self.end_quarter, 
                                    [self.interval], dl=self.dl, fund_list=self.fund_list, engine=self.engine)


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
        print('interval: ' + str(self.interval))
        print('table: ' + str(self.table))
        while cur_year <= self.end_year and cur_quarter <= self.end_quarter:
            
            print('calcalate:' + str(cur_year) + 'q' + str(cur_quarter))
            cur_df = self.indicators_df(cur_year, cur_quarter)
            track_error_df = self.te.track_cal(cur_year, cur_quarter, self.interval)
            merged_df = cur_df.merge(track_error_df, how='left', on=['fund_id', 'datetime']).drop_duplicates(['fund_id', 'datetime'])
            print('upload')
            while True:
                try:
                    merged_df.to_sql(self.table, self.engine, index=False, if_exists='append')
                    break
                except Exception as e:
                    print(e)
                    continue

            cur_quarter += 1
            if cur_quarter > 4:
                cur_year += 1
                cur_quarter = 1
            
    
    def indicators_df(self, cur_year, cur_quarter):
        cur_date = self.get_date_str(cur_year, cur_quarter)
        pre_date = self.get_date_str(cur_year - self.interval, cur_quarter)

        new_df_list = []
        for fund_id in self.fund_list:
            new_row = []
            new_row.append(fund_id)
            new_row.append(cur_date)
            
            fi = self.indicators[fund_id]
            beta_fund = fi.get_Beta(set_new=True, start_date=pre_date, end_date=cur_date, fund_id=fund_id)
            new_row.append(beta_fund)
            new_row.append(fi.get_Alpha(set_new=True, start_date=pre_date, end_date=cur_date, fund_id=fund_id))
            new_row.append(fi.get_Treynor_Ratio(set_new=True, start_date=pre_date, end_date=cur_date, fund_id=fund_id, beta=beta_fund))
            new_row.append(fi.get_Max_DD(set_new=True, start_date=pre_date, end_date=cur_date, fund_id=fund_id))
            new_row.append(fi.get_Downside_Risk(set_new=True, start_date=pre_date, end_date=cur_date, fund_id=fund_id))
            new_row.append(fi.get_Return_Over_Period(set_new=True, start_date=pre_date, end_date=cur_date, fund_id=fund_id))
            new_row.append(fi.get_Annualized_Average_Daily_Return(set_new=True, start_date=pre_date, end_date=cur_date, fund_id=fund_id))
            new_row.append(fi.get_Volatility(set_new=True, start_date=pre_date, end_date=cur_date, fund_id=fund_id))
            new_row.append(fi.get_M_square(set_new=True, start_date=pre_date, end_date=cur_date, fund_id=fund_id))
            new_row.append(fi.get_Time_Return(set_new=True, start_date=pre_date, end_date=cur_date, fund_id=fund_id))
            new_row.append(fi.get_Value_at_Risk(set_new=True, start_date=pre_date, end_date=cur_date, fund_id=fund_id))
            new_row.append(fi.get_R_square(set_new=True, start_date=pre_date, end_date=cur_date, fund_id=fund_id))
            new_row.append(fi.get_Sharp_Ratio(set_new=True, start_date=pre_date, end_date=cur_date, fund_id=fund_id))
            new_row.append(fi.get_Treynor_Mazuy_Coefficient(set_new=True, start_date=pre_date, end_date=cur_date, fund_id=fund_id))
            new_row.append(fi.get_Fee_Rate(fi.dl, fi.actual_start, fi.actual_end, fi.fund_id))

            new_df_list.append(new_row)
        
        df_indicators = pd.DataFrame(new_df_list, columns=self.tb_columns)
        return df_indicators

if __name__ == '__main__':
    # 从不同间隔计算基础指标
    iu = Indicators_Uploader(2013, 1, 2017, 4, 'fund_indicator', interval=3)
    iu.quarter_upload()

    # iu.interval = 3
    # iu.table = 'fund_indicator_3'
    # iu.quarter_upload()

    # iu.interval = 1
    # iu.table = 'fund_indicator_1'
    # iu.quarter_upload()