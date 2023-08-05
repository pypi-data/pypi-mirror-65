import numpy as np
import pandas as pd
from load_and_update_data.get_fund_data import DataLoader
import datetime

class index_indicators:
    def __init__(self, start_date, end_date, index_id, 
    dataloader=None, username=None, password=None, database=None):
        if dataloader is None:
            self.dl = DataLoader(username, password, database_name=database)
        else:
            self.dl = dataloader
        self.no_risk_return = 0.03
        self.year_coefficient = 242
        self.index_id = index_id
        self.start_date = start_date
        self.previous_date = self.date_retriever(start_date)
        self.end_date = end_date
        
        self.index_price_info = self.dl.get_data('index_price', column_names=['ret', 'date', 'close'], 
                            select_columns=['date', 'date', 'order_book_id'], 
                            aim_values=[self.previous_date, end_date, self.index_id], 
                            operator=['>=', '<=', '='])
        self.index_price_info[['ret', 'close']] = self.index_price_info[['ret', 'close']].apply(pd.to_numeric)

    
    def date_retriever(self, adj_time):
        sql = 'select `datetime` from quant_data.nav where `datetime` < {} order by `datetime` desc limit 1;'.format(adj_time)
        with self.dl.connect.cursor() as cu:
            cu.execute(sql)
            result = cu.fetchall()
            return self.dl.transfer_data_to_df(result, cu).values.flatten()[0]

    def get_Max_DD(self, set_new=False, start_date=None, end_date=None, index_id=None):
        if not set_new:
            start_date = self.start_date
            end_date = self.end_date
            index_id = self.index_id
        previous_date = self.date_retriever(start_date)
        start_date = previous_date
        if start_date >= self.start_date and end_date <= self.end_date:
            index_nav_tb = self.index_price_info[(self.index_price_info['date'] >= start_date) & 
            (self.index_price_info['date'] <= end_date)][['close', 'date']]
        else:
            index_nav_tb = self.dl.get_data('index_price', column_names=['close', 'date'], 
                                        select_columns=['date', 'date', 'order_book_id'], 
                                        aim_values=[start_date, end_date, self.index_id], 
                                        operator=['>=', '<=', '=']).sort_values(by=['date'], ignore_index=True, ascending=True)
            index_nav_tb['close'] = pd.to_numeric(index_nav_tb['close'])

        index_nav_list = index_nav_tb['close'].values
        lenth = index_nav_list.shape[0]
        max_dd = 0
        for s in range(lenth - 1):
            for t in range(s + 1, lenth):
                cur_dd = -(index_nav_list[t] / index_nav_list[s] - 1)
                if cur_dd > max_dd:
                    max_dd = cur_dd
        
        return max_dd

    def get_Return_Over_Period(self, set_new=False, start_date=None, end_date=None, index_id=None):
        if not set_new:
            start_date = self.start_date
            end_date = self.end_date
            index_id = self.index_id
        
        previous_date = self.date_retriever(start_date)
        start_date = previous_date

        if start_date >= self.start_date and end_date <= self.end_date:
            index_nav_tb = self.index_price_info[(self.index_price_info['date'] >= start_date) & 
            (self.index_price_info['date'] <= end_date)][['close', 'date']]
        else:
            index_nav_tb = self.dl.get_data('index_price', column_names=['close', 'date'], 
                                        select_columns=['date', 'date', 'order_book_id'], 
                                        aim_values=[start_date, end_date, self.index_id], 
                                        operator=['>=', '<=', '=']).sort_values(by=['date'], ignore_index=True, ascending=True)
            index_nav_tb['close'] = pd.to_numeric(index_nav_tb['close'])

        index_nav_list = index_nav_tb['close'].values
        return_over_period = index_nav_list[-1] / index_nav_list[0] - 1

        return return_over_period
    
    def get_Annualized_Average_Daily_Return(self, set_new=False, start_date=None, end_date=None, index_id=None):
        if not set_new:
            start_date = self.start_date
            end_date = self.end_date
            index_id = self.index_id
        
        if start_date >= self.start_date and end_date <= self.end_date:
            index_ret_tb = self.index_price_info[(self.index_price_info['date'] >= start_date) & 
            (self.index_price_info['date'] <= end_date)][['ret', 'date']]
        else:
            index_ret_tb = self.dl.get_data('index_price', column_names=['ret', 'date'], 
                                        select_columns=['date', 'date', 'order_book_id'], 
                                        aim_values=[start_date, end_date, self.index_id], 
                                        operator=['>=', '<=', '=']).sort_values(by=['date'], ignore_index=True, ascending=True)
            index_ret_tb['ret'] = pd.to_numeric(index_ret_tb['ret'])

        index_ret_list = index_ret_tb['ret'].values
        sum_ret = index_ret_list.sum()
        lenth = index_ret_list.shape[0]
        Annualized_Average_Daily_Return = sum_ret * self.year_coefficient / lenth

        return Annualized_Average_Daily_Return
    
    def get_Volatility(self, set_new=False, start_date=None, end_date=None, index_id=None):
        if not set_new:
            start_date = self.start_date
            end_date = self.end_date
            index_id = self.index_id

        if start_date >= self.start_date and end_date <= self.end_date:
            index_ret_tb = self.index_price_info[(self.index_price_info['date'] >= start_date) & 
            (self.index_price_info['date'] <= end_date)][['ret', 'date']]
        else:
            index_ret_tb = self.dl.get_data('index_price', column_names=['ret', 'date'], 
                                        select_columns=['date', 'date', 'order_book_id'], 
                                        aim_values=[start_date, end_date, self.index_id], 
                                        operator=['>=', '<=', '=']).sort_values(by=['date'], ignore_index=True, ascending=True)
            index_ret_tb['ret'] = pd.to_numeric(index_ret_tb['ret'])
        
        index_ret_list = index_ret_tb['ret'].values
        mean_ret = index_ret_list.mean()
        lenth = index_ret_list.shape[0]

        sum_ds = 0
        for i in range(lenth):
            cur_ret = index_ret_list[i]
            cur_ds = (cur_ret - mean_ret) ** 2
            sum_ds += cur_ds
        volatility = (self.year_coefficient / (lenth - 1) * sum_ds) ** 0.5

        return volatility
    
    def get_Sharp_Ratio(self, set_new=False, start_date=None, end_date=None, index_id=None):
        if not set_new:
            start_date = self.start_date
            end_date = self.end_date
            index_id = self.index_id

        if start_date >= self.start_date and end_date <= self.end_date:
            index_ret_tb = self.index_price_info[(self.index_price_info['date'] >= start_date) & 
            (self.index_price_info['date'] <= end_date)][['ret', 'date']]
        else:
            index_ret_tb = self.dl.get_data('index_price', column_names=['ret', 'date'], 
                                        select_columns=['date', 'date', 'order_book_id'], 
                                        aim_values=[start_date, end_date, self.index_id], 
                                        operator=['>=', '<=', '=']).sort_values(by=['date'], ignore_index=True, ascending=True)
            index_ret_tb['ret'] = pd.to_numeric(index_ret_tb['ret'])
        
        
        ret_index_mean = index_ret_tb['ret'].mean() * self.year_coefficient
        ret_index_std = index_ret_tb['ret'].std() * (self.year_coefficient ** 0.5)
        sr = (ret_index_mean - self.no_risk_return) / ret_index_std

        return sr
    
    