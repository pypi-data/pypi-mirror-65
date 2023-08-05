import numpy as np
import pandas as pd
from load_and_update_data.get_fund_data import DataLoader
import datetime

class fund_indicators:
    def __init__(self, start_date, end_date, fund_id, 
    dataloader=None, username=None, password=None, database=None, 
    load_idx=True, trans_data=None):
        if dataloader is None:
            self.dl = DataLoader(username, password, database_name=database)
        else:
            self.dl = dataloader
        self.market_index_id = '000300.XSHG'
        self.no_risk_return = 0.03
        self.year_coefficient = 242
        self.fund_id = fund_id
        self.start_date = start_date
        self.end_date = end_date
        
        if trans_data is None:
            self.previous_date = self.date_retriever(start_date, check_trading_date=False)
            self.trading_date_tb = self.dl.get_data('index_price', column_names=['date'], 
                        select_columns=['date', 'date', 'order_book_id'], 
                        aim_values=[self.previous_date, end_date, self.market_index_id], 
                        operator=['>=', '<=', '=']).sort_values(by=['date'], ignore_index=True, ascending=True)
            self.fund_price_info = self.dl.get_data('nav', column_names=['change_rate', 'datetime', 'adjusted_net_value'], 
                        select_columns=['datetime', 'datetime', 'fund_id'], 
                        aim_values=[self.previous_date, end_date, fund_id], 
                        operator=['>=', '<=', '='])
            if self.fund_price_info is not None:
                self.fund_price_info = self.fund_price_info.sort_values(by=['datetime'], ignore_index=True, ascending=True)
                self.fund_price_info[['change_rate', 'adjusted_net_value']] = self.fund_price_info[['change_rate', 'adjusted_net_value']].apply(pd.to_numeric)
            if load_idx:
                self.index_price_info = self.dl.get_data('index_price', column_names=['ret', 'date', 'close'], 
                                    select_columns=['date', 'date', 'order_book_id'], 
                                    aim_values=[self.previous_date, end_date, self.market_index_id], 
                                    operator=['>=', '<=', '='])
                if self.index_price_info is not None:
                    self.index_price_info = self.index_price_info.sort_values(by=['date'], ignore_index=True, ascending=True)
                    self.index_price_info[['ret', 'close']] = self.index_price_info[['ret', 'close']].apply(pd.to_numeric)
            else:
                self.index_price_info = None
        else:
            self.trading_date_tb, self.fund_price_info, self.index_price_info = trans_data
            self.previous_date = self.date_retriever(start_date)
        
        tmp = self.fund_price_info[(self.fund_price_info['datetime'] >= self.previous_date) & (self.fund_price_info['datetime'] <= self.end_date)]
        self.actual_start = tmp['datetime'].min()
        self.actual_end = tmp['datetime'].max()
    
    def date_retriever(self, adj_time, check_trading_date=True):
        if check_trading_date:
            sub_datetime = self.trading_date_tb[self.trading_date_tb['date'] < adj_time].values.flatten()
            if len(sub_datetime) > 0:
                return sub_datetime[-1]
        
        sql = 'select `date` from quant_data.index_price where `date` < {} order by `date` desc limit 1;'.format(adj_time)
        with self.dl.connect.cursor() as cu:
            cu.execute(sql)
            result = cu.fetchall()
            return self.dl.transfer_data_to_df(result, cu).values.flatten()[0]
    
    def get_fund_id(self, set_new=False, start_date=None, end_date=None, miquant_id=None):
        if set_new is False:
            start_date = self.start_date
            end_date = self.end_date
            miquant_id = self.fund_id

        fund_fee_tb = self.dl.get_data('fundlist_wind', column_names=['fund_id', 'found_date', 'end_date'], 
                       select_columns=['order_book_id'], 
                       aim_values=[miquant_id], 
                       operator=['='])
        if fund_fee_tb is None:
            return None
        for fund_id, found_date, delisted_date in fund_fee_tb.values:
            if start_date >= found_date and (delisted_date >= end_date or delisted_date == '00000000'):
                return fund_id
        
        return None

    def get_Treynor_Ratio(self, set_new=False, start_date=None, end_date=None, fund_id=None, beta=None):
        if not set_new:
            start_date = self.start_date
            end_date = self.end_date
            fund_id = self.fund_id
        # fetch fund ret
        if start_date >= self.start_date and end_date <= self.end_date and fund_id == self.fund_id:
            fund_nav = self.fund_price_info[(self.fund_price_info['datetime'] >= start_date) &
                                            (self.fund_price_info['datetime'] <= end_date)][['change_rate', 'datetime']]
        else:
            fund_nav = self.dl.get_data('nav', column_names=['change_rate', 'datetime'], 
                        select_columns=['datetime', 'datetime', 'fund_id'], 
                        aim_values=[start_date, end_date, fund_id], 
                        operator=['>=', '<=', '='])
        ret_fund = pd.to_numeric(fund_nav['change_rate']).mean() * self.year_coefficient

        if beta is not None:
            beta_fund = beta
            TR = (ret_fund - self.no_risk_return) / beta_fund
            return TR
        # beta cal
        # 暂时没有交易日的表，先t-400，然后找到以start_date为截止时间的self.year_coefficient列
        previous_year = datetime.datetime.strptime(start_date, '%Y%m%d') - datetime.timedelta(days=400)
        pre_date = previous_year.strftime("%Y%m%d")
        if pre_date >= self.start_date and end_date <= self.end_date and self.index_price_info is not None:
            index_ret = self.index_price_info[(self.index_price_info['date'] >= pre_date) & 
            (self.index_price_info['date'] <= end_date)][['ret', 'date']]
        else:
            index_ret = self.dl.get_data('index_price', column_names=['ret', 'date'], 
                                select_columns=['date', 'date', 'order_book_id'], 
                                aim_values=[pre_date, start_date, self.market_index_id], 
                                operator=['>=', '<=', '='])
        # fund previous data
        if pre_date >= self.start_date and end_date <= self.end_date and fund_id == self.fund_id:
            fund_ret = self.fund_price_info[(self.fund_price_info['datetime'] >= pre_date) &
            (self.fund_price_info['datetime'] <= end_date)][['change_rate', 'datetime']]
        else:
            fund_ret = self.dl.get_data('nav', column_names=['change_rate', 'datetime'], 
                        select_columns=['datetime', 'datetime', 'fund_id'], 
                        aim_values=[pre_date, end_date, fund_id], 
                        operator=['>=', '<=', '='])
        # merge to compare
        comp_table = index_ret.merge(fund_ret, left_on='date', right_on='datetime', how='inner').sort_values(by=['date'], ascending=False)
        comp_table[['ret', 'change_rate']] = comp_table[['ret', 'change_rate']].apply(pd.to_numeric)
        # get self.year_coefficient row
        corr_table = comp_table[:self.year_coefficient].drop(columns=['date', 'datetime'])
        corr = corr_table.corr()['ret']['change_rate']
        # get tr
        std_index = corr_table['ret'].std()
        std_fund = corr_table['change_rate'].std()
        beta_fund = corr * std_fund / std_index
        TR = (ret_fund - self.no_risk_return) / beta_fund
        return TR
    
    def get_Alpha(self, set_new=False, start_date=None, end_date=None, fund_id=None):
        if not set_new:
            start_date = self.start_date
            end_date = self.end_date
            fund_id = self.fund_id
        # fetch fund ret
        if start_date >= self.start_date and end_date <= self.end_date and fund_id == self.fund_id:
            fund_ret_tb = self.fund_price_info[(self.fund_price_info['datetime'] >= start_date) &
            (self.fund_price_info['datetime'] <= end_date)][['change_rate', 'datetime']]
        else:
            fund_ret_tb = self.dl.get_data('nav', column_names=['change_rate', 'datetime'], 
                                select_columns=['datetime', 'datetime', 'fund_id'], 
                                aim_values=[start_date, end_date, fund_id], 
                                operator=['>=', '<=', '='])
        fund_ret_tb['change_rate'] = pd.to_numeric(fund_ret_tb['change_rate'])
        ret_fund = fund_ret_tb['change_rate'].mean()
        # fetch index ret
        if start_date >= self.start_date and end_date <= self.end_date and self.index_price_info is not None:
            index_ret_tb = self.index_price_info[(self.index_price_info['date'] >= start_date) & 
            (self.index_price_info['date'] <= end_date)][['ret', 'date']]
        else:
            index_ret_tb = self.dl.get_data('index_price', column_names=['ret', 'date'], 
                                        select_columns=['date', 'date', 'order_book_id'], 
                                        aim_values=[start_date, end_date, self.market_index_id], 
                                        operator=['>=', '<=', '='])
        index_ret_tb['ret'] = pd.to_numeric(index_ret_tb['ret'])
        ret_index = index_ret_tb['ret'].mean()
        # get beta
        comp_table = index_ret_tb.merge(fund_ret_tb, left_on='date', right_on='datetime', how='inner').sort_values(by=['date'], ascending=False)
        corr_table = comp_table.drop(columns=['date', 'datetime'])
        corr = corr_table.corr()['ret']['change_rate']

        std_index = corr_table['ret'].std()
        std_fund = corr_table['change_rate'].std()
        beta_fund = corr * std_fund / std_index
        # get alpha
        no_risk_return_day = self.no_risk_return / self.year_coefficient
        alpha = (ret_fund - no_risk_return_day - beta_fund * (ret_index - no_risk_return_day)) * self.year_coefficient

        return alpha
    
    def get_Max_DD(self, set_new=False, start_date=None, end_date=None, fund_id=None):
        if not set_new:
            start_date = self.start_date
            end_date = self.end_date
            fund_id = self.fund_id
        
        previous_date = self.date_retriever(start_date)
        start_date = previous_date
        if fund_id == self.fund_id and self.fund_price_info is not None:
            fund_nav_tb = self.fund_price_info[(self.fund_price_info['datetime'] >= start_date) &
            (self.fund_price_info['datetime'] <= end_date)][['adjusted_net_value', 'datetime']]
        else:
            fund_nav_tb = self.dl.get_data('nav', column_names=['adjusted_net_value', 'datetime'], 
                        select_columns=['datetime', 'datetime', 'fund_id'], 
                        aim_values=[start_date, end_date, fund_id], 
                        operator=['>=', '<=', '=']).sort_values(by=['datetime'], ignore_index=True, ascending=True)

        fund_nav_tb['adjusted_net_value'] = pd.to_numeric(fund_nav_tb['adjusted_net_value'])

        fund_nav_list = fund_nav_tb['adjusted_net_value'].values
        lenth = fund_nav_list.shape[0]
        if lenth == 0:
            return np.nan
        max_dd = 0
        for s in range(lenth - 1):
            for t in range(s + 1, lenth):
                cur_dd = -(fund_nav_list[t] / fund_nav_list[s] - 1)
                if cur_dd > max_dd:
                    max_dd = cur_dd
        
        return max_dd
    
    def get_Downside_Risk(self, set_new=False, start_date=None, end_date=None, fund_id=None):
        if not set_new:
            start_date = self.start_date
            end_date = self.end_date
            fund_id = self.fund_id
        
        if start_date >= self.start_date and end_date <= self.end_date and fund_id == self.fund_id:
            fund_ret_tb = self.fund_price_info[(self.fund_price_info['datetime'] >= start_date) &
            (self.fund_price_info['datetime'] <= end_date)][['change_rate', 'datetime']]
        else:
            fund_ret_tb = self.dl.get_data('nav', column_names=['change_rate', 'datetime'], 
                        select_columns=['datetime', 'datetime', 'fund_id'], 
                        aim_values=[start_date, end_date, fund_id], 
                        operator=['>=', '<=', '=']).sort_values(by=['datetime'], ignore_index=True, ascending=True)
        fund_ret_tb['change_rate'] = pd.to_numeric(fund_ret_tb['change_rate'])

        fund_ret_list = fund_ret_tb['change_rate'].values
        lenth = fund_ret_list.shape[0]
        no_risk_return_day = self.no_risk_return / self.year_coefficient
        downside_risk = 0
        for t in range(lenth):
            cur_risk = abs(min(0, fund_ret_list[t] - no_risk_return_day))
            downside_risk += cur_risk
        return downside_risk

    def get_Return_Over_Period(self, set_new=False, start_date=None, end_date=None, fund_id=None):
        if not set_new:
            start_date = self.start_date
            end_date = self.end_date
            fund_id = self.fund_id
        
        previous_date = self.date_retriever(start_date)
        start_date = previous_date

        if fund_id == self.fund_id and self.fund_price_info is not None:
            fund_nav_tb = self.fund_price_info[(self.fund_price_info['datetime'] >= start_date) &
            (self.fund_price_info['datetime'] <= end_date)][['adjusted_net_value', 'datetime']]
        else:
            fund_nav_tb = self.dl.get_data('nav', column_names=['adjusted_net_value', 'datetime'], 
                        select_columns=['datetime', 'datetime', 'fund_id'], 
                        aim_values=[start_date, end_date, fund_id], 
                        operator=['>=', '<=', '=']).sort_values(by=['datetime'], ignore_index=True, ascending=True)
        
        fund_nav_tb['adjusted_net_value'] = pd.to_numeric(fund_nav_tb['adjusted_net_value'])
        fund_nav_list = fund_nav_tb['adjusted_net_value'].values
        lenth = fund_nav_list.shape[0]
        if lenth == 0:
            return np.nan
        return_over_period = fund_nav_list[-1] / fund_nav_list[0] - 1

        return return_over_period
    
    def get_Annualized_Average_Daily_Return(self, set_new=False, start_date=None, end_date=None, fund_id=None):
        if not set_new:
            start_date = self.start_date
            end_date = self.end_date
            fund_id = self.fund_id
        
        if start_date >= self.start_date and end_date <= self.end_date and fund_id == self.fund_id:
            fund_ret_tb = self.fund_price_info[(self.fund_price_info['datetime'] >= start_date) &
            (self.fund_price_info['datetime'] <= end_date)][['change_rate', 'datetime']]
        else:
            fund_ret_tb = self.dl.get_data('nav', column_names=['change_rate', 'datetime'], 
                        select_columns=['datetime', 'datetime', 'fund_id'], 
                        aim_values=[start_date, end_date, fund_id], 
                        operator=['>=', '<=', '=']).sort_values(by=['datetime'], ignore_index=True, ascending=True)
        
        fund_ret_tb['change_rate'] = pd.to_numeric(fund_ret_tb['change_rate'])
        fund_ret_list = fund_ret_tb['change_rate'].values

        lenth = fund_ret_list.shape[0]
        if lenth <= 0:
            return np.nan
        sum_ret = fund_ret_list.sum()
        Annualized_Average_Daily_Return = sum_ret * self.year_coefficient / lenth

        return Annualized_Average_Daily_Return
    
    def get_Volatility(self, set_new=False, start_date=None, end_date=None, fund_id=None):
        if not set_new:
            start_date = self.start_date
            end_date = self.end_date
            fund_id = self.fund_id

        if start_date >= self.start_date and end_date <= self.end_date and fund_id == self.fund_id:
            fund_ret_tb = self.fund_price_info[(self.fund_price_info['datetime'] >= start_date) &
            (self.fund_price_info['datetime'] <= end_date)][['change_rate', 'datetime']]
        else:
            fund_ret_tb = self.dl.get_data('nav', column_names=['change_rate', 'datetime'], 
                        select_columns=['datetime', 'datetime', 'fund_id'], 
                        aim_values=[start_date, end_date, fund_id], 
                        operator=['>=', '<=', '=']).sort_values(by=['datetime'], ignore_index=True, ascending=True)
        fund_ret_tb['change_rate'] = pd.to_numeric(fund_ret_tb['change_rate'])
        fund_ret_list = fund_ret_tb['change_rate'].values
        lenth = fund_ret_list.shape[0]
        if lenth <= 0:
            return np.nan
        mean_ret = fund_ret_list.mean()
        lenth = fund_ret_list.shape[0]

        sum_ds = 0
        for i in range(lenth):
            cur_ret = fund_ret_list[i]
            cur_ds = (cur_ret - mean_ret) ** 2
            sum_ds += cur_ds
        
        if lenth - 1 == 0:
            return np.nan
        volatility = (self.year_coefficient / (lenth - 1) * sum_ds) ** 0.5

        return volatility
    
    def get_M_square(self, set_new=False, start_date=None, end_date=None, fund_id=None):
        if not set_new:
            start_date = self.start_date
            end_date = self.end_date
            fund_id = self.fund_id

        if start_date >= self.start_date and end_date <= self.end_date and fund_id == self.fund_id:
            fund_ret_tb = self.fund_price_info[(self.fund_price_info['datetime'] >= start_date) &
            (self.fund_price_info['datetime'] <= end_date)][['change_rate', 'datetime']]
        else:
            fund_ret_tb = self.dl.get_data('nav', column_names=['change_rate', 'datetime'], 
                        select_columns=['datetime', 'datetime', 'fund_id'], 
                        aim_values=[start_date, end_date, fund_id], 
                        operator=['>=', '<=', '='])
        fund_ret_tb['change_rate'] = pd.to_numeric(fund_ret_tb['change_rate'])
        lenth = fund_ret_tb.shape[0]
        if lenth <= 0:
            return np.nan
        ret_fund = fund_ret_tb['change_rate'].mean() * self.year_coefficient
        std_fund = fund_ret_tb['change_rate'].std() * (self.year_coefficient ** 0.5)
        # fetch index ret
        if start_date >= self.start_date and end_date <= self.end_date and self.index_price_info is not None:
            index_ret_tb = self.index_price_info[(self.index_price_info['date'] >= start_date) & 
            (self.index_price_info['date'] <= end_date)][['ret', 'date']]
        else:
            index_ret_tb = self.dl.get_data('index_price', column_names=['ret', 'date'], 
                                        select_columns=['date', 'date', 'order_book_id'], 
                                        aim_values=[start_date, end_date, self.market_index_id], 
                                        operator=['>=', '<=', '='])
        index_ret_tb['ret'] = pd.to_numeric(index_ret_tb['ret'])
        ret_index = index_ret_tb['ret'].mean() * self.year_coefficient
        std_index = index_ret_tb['ret'].std() * (self.year_coefficient ** 0.5)

        if std_fund == 0:
            return np.nan
        M_square = (std_index / std_fund * (ret_fund - self.no_risk_return) + self.no_risk_return) - ret_index
        return M_square
    
    def get_Time_Return(self, set_new=False, start_date=None, end_date=None, fund_id=None, interval=60):
        if not set_new:
            start_date = self.start_date
            end_date = self.end_date
            fund_id = self.fund_id
        # fetch fund ret
        if start_date >= self.start_date and end_date <= self.end_date and fund_id == self.fund_id:
            fund_ret_tb = self.fund_price_info[(self.fund_price_info['datetime'] >= start_date) &
            (self.fund_price_info['datetime'] <= end_date)][['change_rate', 'datetime']]
        else:
            fund_ret_tb = self.dl.get_data('nav', column_names=['change_rate', 'datetime'], 
                                select_columns=['datetime', 'datetime', 'fund_id'], 
                                aim_values=[start_date, end_date, fund_id], 
                                operator=['>=', '<=', '='])
        fund_ret_tb['change_rate'] = pd.to_numeric(fund_ret_tb['change_rate'])
        # fetch index ret and close
        if start_date >= self.start_date and end_date <= self.end_date and self.index_price_info is not None: 
            index_ret_tb = self.index_price_info[(self.index_price_info['date'] >= start_date) & 
            (self.index_price_info['date'] <= end_date)][['ret', 'date', 'close']]
        else:
            index_ret_tb = self.dl.get_data('index_price', column_names=['ret', 'date', 'close'], 
                                        select_columns=['date', 'date', 'order_book_id'], 
                                        aim_values=[start_date, end_date, self.market_index_id], 
                                        operator=['>=', '<=', '='])
        index_ret_tb[['ret', 'close']] = index_ret_tb[['ret', 'close']].apply(pd.to_numeric)
        # merge table
        comp_table = index_ret_tb.merge(fund_ret_tb, left_on='date', right_on='datetime', how='inner').sort_values(by=['date'], ascending=True)
        # get beta_0
        corr_table = comp_table.drop(columns=['date', 'datetime', 'close'])
        corr = corr_table.corr()['ret']['change_rate']
        std_index = corr_table['ret'].std()
        std_fund = corr_table['change_rate'].std()
        beta_fund = corr * std_fund / std_index
        # get m interval values
        lenth = comp_table.shape[0]
        pre_index = 0
        index = 0
        sum_tr = 0
        while True:
            if index >= lenth:
                break
            if index + interval > lenth:
                index = lenth
            else:
                index += interval
            
            cur_tb = comp_table[pre_index:index]
            cur_len = index - pre_index
            
            index_ret_list = cur_tb['close'].values
            ret_index_m = index_ret_list[-1] / index_ret_list[0] - 1
            no_risk_return_m = self.no_risk_return / self.year_coefficient * (cur_len - 1)
            
            cur_corr_table = cur_tb.drop(columns=['date', 'datetime', 'close'])
            corr_m = cur_corr_table.corr()['ret']['change_rate']
            std_fund_m = cur_corr_table['change_rate'].std()
            std_index_m = cur_corr_table['ret'].std()
            beta_fund_m = corr_m * std_fund_m / std_index_m
            
            cur_tr = (beta_fund_m - beta_fund) * (ret_index_m - no_risk_return_m)
            sum_tr += cur_tr

            pre_index = index
        
        return sum_tr
    
    def get_Value_at_Risk(self, set_new=False, start_date=None, end_date=None, fund_id=None):
        if not set_new:
            start_date = self.start_date
            end_date = self.end_date
            fund_id = self.fund_id
        if start_date >= self.start_date and end_date <= self.end_date and fund_id == self.fund_id:
            fund_ret_tb = self.fund_price_info[(self.fund_price_info['datetime'] >= start_date) &
            (self.fund_price_info['datetime'] <= end_date)][['change_rate', 'datetime']]
        else:
            fund_ret_tb = self.dl.get_data('nav', column_names=['change_rate', 'datetime'], 
                        select_columns=['datetime', 'datetime', 'fund_id'], 
                        aim_values=[start_date, end_date, fund_id], 
                        operator=['>=', '<=', '=']).sort_values(by=['datetime'], ignore_index=True, ascending=True)
        fund_ret_tb['change_rate'] = pd.to_numeric(fund_ret_tb['change_rate'])
        sorted_ret = fund_ret_tb.sort_values(by=['change_rate'], ignore_index=True, ascending=False)['change_rate']
        q95 = sorted_ret.quantile(0.05)
        VaR = -min(0, q95)
        return VaR
    
    def get_Beta(self, set_new=False, start_date=None, end_date=None, fund_id=None):
        if not set_new:
            start_date = self.start_date
            end_date = self.end_date
            fund_id = self.fund_id

        if start_date >= self.start_date and end_date <= self.end_date and fund_id == self.fund_id:
            fund_ret_tb = self.fund_price_info[(self.fund_price_info['datetime'] >= start_date) &
            (self.fund_price_info['datetime'] <= end_date)][['change_rate', 'datetime']]
        else:
            fund_ret_tb = self.dl.get_data('nav', column_names=['change_rate', 'datetime'], 
                        select_columns=['datetime', 'datetime', 'fund_id'], 
                        aim_values=[start_date, end_date, fund_id], 
                        operator=['>=', '<=', '='])
        fund_ret_tb['change_rate'] = pd.to_numeric(fund_ret_tb['change_rate'])
        # fetch index ret
        if start_date >= self.start_date and end_date <= self.end_date and self.index_price_info is not None:
            index_ret_tb = self.index_price_info[(self.index_price_info['date'] >= start_date) & 
            (self.index_price_info['date'] <= end_date)][['ret', 'date']]
        else:
            index_ret_tb = self.dl.get_data('index_price', column_names=['ret', 'date'], 
                                        select_columns=['date', 'date', 'order_book_id'], 
                                        aim_values=[start_date, end_date, self.market_index_id], 
                                        operator=['>=', '<=', '='])
        index_ret_tb['ret'] = pd.to_numeric(index_ret_tb['ret'])
        comp_table = index_ret_tb.merge(fund_ret_tb, left_on='date', right_on='datetime', how='inner').sort_values(by=['date'], ascending=False)
        corr_table = comp_table.drop(columns=['date', 'datetime'])
        corr = corr_table.corr()['ret']['change_rate']

        std_index = corr_table['ret'].std()
        std_fund = corr_table['change_rate'].std()
        beta_fund = corr * std_fund / std_index
        return beta_fund
    
    def get_R_square(self, set_new=False, start_date=None, end_date=None, fund_id=None):
        if not set_new:
            start_date = self.start_date
            end_date = self.end_date
            fund_id = self.fund_id
        # fetch fund ret
        if start_date >= self.start_date and end_date <= self.end_date and fund_id == self.fund_id:
            fund_ret_tb = self.fund_price_info[(self.fund_price_info['datetime'] >= start_date) &
            (self.fund_price_info['datetime'] <= end_date)][['change_rate', 'datetime']]
        else:
            fund_ret_tb = self.dl.get_data('nav', column_names=['change_rate', 'datetime'], 
                                select_columns=['datetime', 'datetime', 'fund_id'], 
                                aim_values=[start_date, end_date, fund_id], 
                                operator=['>=', '<=', '='])
        fund_ret_tb['change_rate'] = pd.to_numeric(fund_ret_tb['change_rate'])
        # fetch index ret
        if start_date >= self.start_date and end_date <= self.end_date and self.index_price_info is not None:
            index_ret_tb = self.index_price_info[(self.index_price_info['date'] >= start_date) & 
            (self.index_price_info['date'] <= end_date)][['ret', 'date']]
        else:
            index_ret_tb = self.dl.get_data('index_price', column_names=['ret', 'date'], 
                                        select_columns=['date', 'date', 'order_book_id'], 
                                        aim_values=[start_date, end_date, self.market_index_id], 
                                        operator=['>=', '<=', '='])
        index_ret_tb['ret'] = pd.to_numeric(index_ret_tb['ret'])

        comp_table = index_ret_tb.merge(fund_ret_tb, left_on='date', right_on='datetime', how='inner').sort_values(by=['date'], ascending=True)
        # get x and y
        ret_fund_list = comp_table['change_rate'].values
        ret_index_list = comp_table['ret'].values
        ret_f = self.no_risk_return / self.year_coefficient

        y = ret_fund_list - ret_f
        x = ret_index_list - ret_f
        if len(x) <= 0:
            return np.nan
        # get y = ax + b and y hat
        coeffs = np.polyfit(x, y, 1)
        p = np.poly1d(coeffs)
        yhat = p(x)
        # get r^2
        y_mean = y.mean()
        ssr = ((yhat - y_mean) **2 ).sum()
        sst = ((y - y_mean) ** 2).sum()

        if sst == 0:
            return np.nan

        r_square = ssr / sst
        return r_square

    def get_Sharp_Ratio(self, set_new=False, start_date=None, end_date=None, fund_id=None):
        if not set_new:
            start_date = self.start_date
            end_date = self.end_date
            fund_id = self.fund_id

        if start_date >= self.start_date and end_date <= self.end_date and fund_id == self.fund_id:
            fund_ret_tb = self.fund_price_info[(self.fund_price_info['datetime'] >= start_date) &
            (self.fund_price_info['datetime'] <= end_date)][['change_rate', 'datetime']]
        else:
            fund_ret_tb = self.dl.get_data('nav', column_names=['change_rate', 'datetime'], 
                        select_columns=['datetime', 'datetime', 'fund_id'], 
                        aim_values=[start_date, end_date, fund_id], 
                        operator=['>=', '<=', '='])
        fund_ret_tb['change_rate'] = pd.to_numeric(fund_ret_tb['change_rate'])
        ret_fund_mean = fund_ret_tb['change_rate'].mean() * self.year_coefficient
        ret_fund_std = fund_ret_tb['change_rate'].std() * (self.year_coefficient ** 0.5)

        if ret_fund_std == 0:
            return np.nan

        sr = (ret_fund_mean - self.no_risk_return) / ret_fund_std

        return sr
    
    def get_Treynor_Mazuy_Coefficient(self, set_new=False, start_date=None, end_date=None, fund_id=None):
        if not set_new:
            start_date = self.start_date
            end_date = self.end_date
            fund_id = self.fund_id

        if start_date >= self.start_date and end_date <= self.end_date and fund_id == self.fund_id:
            fund_ret_tb = self.fund_price_info[(self.fund_price_info['datetime'] >= start_date) &
            (self.fund_price_info['datetime'] <= end_date)][['change_rate', 'datetime']]
        else:
            fund_ret_tb = self.dl.get_data('nav', column_names=['change_rate', 'datetime'], 
                        select_columns=['datetime', 'datetime', 'fund_id'], 
                        aim_values=[start_date, end_date, fund_id], 
                        operator=['>=', '<=', '='])
        fund_ret_tb['change_rate'] = pd.to_numeric(fund_ret_tb['change_rate'])

        if start_date >= self.start_date and end_date <= self.end_date and self.index_price_info is not None:
            index_ret_tb = self.index_price_info[(self.index_price_info['date'] >= start_date) & 
            (self.index_price_info['date'] <= end_date)][['ret', 'date']]
        else:
            index_ret_tb = self.dl.get_data('index_price', column_names=['ret', 'date'], 
                                        select_columns=['date', 'date', 'order_book_id'], 
                                        aim_values=[start_date, end_date, self.market_index_id], 
                                        operator=['>=', '<=', '='])
        index_ret_tb['ret'] = pd.to_numeric(index_ret_tb['ret'])

        comp_table = index_ret_tb.merge(fund_ret_tb, left_on='date', right_on='datetime', how='inner').sort_values(by=['date'], ascending=True)
        ret_fund_list = comp_table['change_rate'].values
        ret_index_list = comp_table['ret'].values
        ret_f = self.no_risk_return / self.year_coefficient
        y = ret_fund_list - ret_f
        x = ret_index_list - ret_f
        if len(x) <= 0:
            return np.nan
        coeffs = np.polyfit(x, y, 2)
        TM = coeffs[0]
        return TM
    
    @staticmethod
    def get_Fee_Rate(dl, start_date, end_date, fund_id):
        fund_fee_tb = dl.get_data('fund_fee_info', column_names=['manage_fee', 'trustee_fee'], 
                       select_columns=['fund_id'], 
                       aim_values=[fund_id], 
                       operator=['='])
        if fund_fee_tb is None:
            return np.nan
        fee_rate = fund_fee_tb.values.flatten().sum()
        return fee_rate / 100
