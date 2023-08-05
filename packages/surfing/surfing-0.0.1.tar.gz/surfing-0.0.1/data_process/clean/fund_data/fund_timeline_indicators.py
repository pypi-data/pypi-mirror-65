import numpy as np
import pandas as pd
from load_and_update_data.get_fund_data import DataLoader
from fund_indicators import fund_indicators
from index_indicators import index_indicators
from track_error import Track_Error_Loader
import datetime
import calendar

class fund_timeline_indicators:
    def __init__(self, fund_list, start_date, end_date, index_list=[], asset_idx=[]):
        self.fund_list = fund_list
        self.index_list = index_list
        self.start_date = start_date
        self.end_date = end_date
        self.dl = DataLoader('huyunfan', 'Huyunfan123456', database_name='quant_data')
        self.month_pairs = self.get_month_list()
        self.year_pairs = self.get_year_list()

        self.fund_indicators = {}
        self.index_indicators = {}
        for fund_id in self.fund_list:
            self.fund_indicators[fund_id] = fund_indicators(self.start_date, self.end_date, fund_id, dataloader=self.dl, load_idx=False)
        for index_id in self.index_list:
            self.index_indicators[index_id] = index_indicators(self.start_date, self.end_date, index_id, dataloader=self.dl)

        self.asset_list = [Track_Error_Loader.at2col(x) for x in asset_idx]
        strlist = ','.join(["`" + col + "`" for col in self.asset_list])
        sql = "select `date`,{} from quant_data.active_asset_index \
        where `date`>={} and `date`<={}".format(strlist, self.start_date, self.end_date)
        self.asset_tb = self.dl.get_data_from_sql(sql)

    def get_month_list(self):
        start_date = self.start_date
        end_date = self.end_date

        start_year = start_date[:4]
        start_month = start_date[4:6]

        month_pair = []
        month_pair.append((start_date, start_year + start_month + str(calendar.monthrange(int(start_year), int(start_month))[1])))
        cur_year = int(start_year)
        cur_month = int(start_month) + 1
        while True:
            if cur_month > 12:
                cur_month = 1
                cur_year += 1
            
            cur_month_range = calendar.monthrange(cur_year, cur_month)[1]
            cur_start_date = datetime.datetime(cur_year, cur_month, 1).strftime('%Y%m%d')
            cur_end_date = datetime.datetime(cur_year, cur_month, cur_month_range).strftime('%Y%m%d')
            
            if cur_end_date >= end_date:
                month_pair.append((cur_start_date, end_date))
                break
            
            month_pair.append((cur_start_date, cur_end_date))
            cur_month += 1
        return month_pair
    
    def get_year_list(self):
        start_date = self.start_date
        end_date = self.end_date

        start_year = start_date[:4]
        # start_month = start_date[4:6]
        end_year = end_date[:4]

        year_pair = []
        if end_date > start_year + '1231':
            year_pair.append((start_date, start_year + '1231'))
        else:
            year_pair.append((start_date, end_date))
            return year_pair

        cur_year = int(start_year)
        for y in range(cur_year, int(end_year)):
            cur_start_date = datetime.datetime(y, 1, 1).strftime('%Y%m%d')
            cur_end_date = datetime.datetime(y, 12, 31).strftime('%Y%m%d')
            year_pair.append((cur_start_date, cur_end_date))

        year_pair.append((end_year + '0101', end_date))
        return year_pair
    
    def recent_date_list(self):
        cur_year = int(self.end_date[:4])
        cur_month = int(self.end_date[4:6])
        cur_day = int(self.end_date[6:])
        cur_date = datetime.datetime(cur_year, cur_month, cur_day)

        recent_pairs = []
        new_start = (cur_date - datetime.timedelta(days=3 * 30)).strftime('%Y%m%d')
        recent_pairs.append((new_start, self.end_date))
        new_start = (cur_date - datetime.timedelta(days=6 * 30)).strftime('%Y%m%d')
        recent_pairs.append((new_start, self.end_date))
        new_start = (cur_date - datetime.timedelta(days=365)).strftime('%Y%m%d')
        recent_pairs.append((new_start, self.end_date))
        new_start = (cur_date - datetime.timedelta(days=2 * 365)).strftime('%Y%m%d')
        recent_pairs.append((new_start, self.end_date))
        new_start = (cur_date - datetime.timedelta(days=3 * 365)).strftime('%Y%m%d')
        recent_pairs.append((new_start, self.end_date))
        new_start = (cur_date - datetime.timedelta(days=5 * 365)).strftime('%Y%m%d')
        recent_pairs.append((new_start, self.end_date))
        recent_pairs.append((self.start_date, self.end_date))

        return recent_pairs
    
    # 从终止的日期往前推，最远5年，如果没有5年，就近原则
    # 没有同类排名
    def get_recent_performance(self):
        fund_dict = {}
        index_dict = {}
        recent_pairs = self.recent_date_list()

        for fund_id in self.fund_list:
            fund_dict[fund_id] = {}
            new_indicators = self.fund_indicators[fund_id]

            fund_dict[fund_id]['YTD'] = new_indicators.get_Return_Over_Period(
                    set_new=True, start_date=self.year_pairs[-1][0], end_date=self.year_pairs[-1][1], fund_id=fund_id
                )
            fund_dict[fund_id]['recent_list'] = []
            for s, e in recent_pairs:
                fund_dict[fund_id]['recent_list'].append(new_indicators.get_Return_Over_Period(
                    set_new=True, start_date=s, end_date=e, fund_id=fund_id
                ))
        
        for index_id in self.index_list:
            index_dict[index_id] = {}
            new_indicators = self.index_indicators[index_id]

            index_dict[index_id]['YTD'] = new_indicators.get_Return_Over_Period(
                    set_new=True, start_date=self.year_pairs[-1][0], end_date=self.year_pairs[-1][1], index_id=index_id
                )
            index_dict[index_id]['recent_list'] = []
            for s, e in recent_pairs:
                index_dict[index_id]['recent_list'].append(new_indicators.get_Return_Over_Period(
                    set_new=True, start_date=s, end_date=e, index_id=index_id
                ))
        
        return fund_dict, index_dict, recent_pairs
    
    # 年度回报表，差市场综合评级，同类排名
    # 从起始的那年到终止的那年
    def get_year_perfomance(self):
        fund_dict = {}
        index_dict = {}
        for fund_id in self.fund_list:
            fund_dict[fund_id] = {}
            new_indicators = self.fund_indicators[fund_id]

            fund_dict[fund_id]['year_ret'] = []
            for year_start_date, year_end_date in self.year_pairs:
                fund_dict[fund_id]['year_ret'].append(new_indicators.get_Return_Over_Period(
                    set_new=True, start_date=year_start_date, end_date=year_end_date, fund_id=fund_id
                ))
        
        for index_id in self.index_list:
            index_dict[index_id] = {}
            new_indicators = self.index_indicators[index_id]

            index_dict[index_id]['year_ret'] = []
            for year_start_date, year_end_date in self.year_pairs:
                index_dict[index_id]['year_ret'].append(new_indicators.get_Return_Over_Period(
                    set_new=True, start_date=year_start_date, end_date=year_end_date, index_id=index_id
                ))
        
        return fund_dict, index_dict, self.year_pairs

    # 300价值表都可以从这里
    def get_300_indicators(self):
        fund_dict = {}
        index_dict = {}
        for fund_id in self.fund_list:
            fund_dict[fund_id] = {}
            new_indicators = self.fund_indicators[fund_id]
            fund_dict[fund_id]['AADR'] = new_indicators.get_Annualized_Average_Daily_Return()
            fund_dict[fund_id]['Volatility'] = new_indicators.get_Volatility()
            fund_dict[fund_id]['MDD'] = new_indicators.get_Max_DD()
            fund_dict[fund_id]['SR'] = new_indicators.get_Sharp_Ratio()
            fund_dict[fund_id]['month_ret'] = []
            for month_start_date, month_end_date in self.month_pairs:
                fund_dict[fund_id]['month_ret'].append(new_indicators.get_Return_Over_Period(
                    set_new=True, start_date=month_start_date, end_date=month_end_date, fund_id=fund_id))
            fund_dict[fund_id]['year_ret'] = []
            for year_start_date, year_end_date in self.year_pairs:
                fund_dict[fund_id]['year_ret'].append(new_indicators.get_Return_Over_Period(
                    set_new=True, start_date=year_start_date, end_date=year_end_date, fund_id=fund_id
                ))
        
        for index_id in self.index_list:
            index_dict[index_id] = {}
            new_indicators = self.index_indicators[index_id]
            index_dict[index_id]['AADR'] = new_indicators.get_Annualized_Average_Daily_Return()
            index_dict[index_id]['Volatility'] = new_indicators.get_Volatility()
            index_dict[index_id]['MDD'] = new_indicators.get_Max_DD()
            index_dict[index_id]['SR'] = new_indicators.get_Sharp_Ratio()
            index_dict[index_id]['month_ret'] = []
            for month_start_date, month_end_date in self.month_pairs:
                index_dict[index_id]['month_ret'].append(new_indicators.get_Return_Over_Period(
                    set_new=True, start_date=month_start_date, end_date=month_end_date, index_id=index_id))
            index_dict[index_id]['year_ret'] = []
            for year_start_date, year_end_date in self.year_pairs:
                index_dict[index_id]['year_ret'].append(new_indicators.get_Return_Over_Period(
                    set_new=True, start_date=year_start_date, end_date=year_end_date, index_id=index_id
                ))
        
        return fund_dict, index_dict, self.month_pairs, self.year_pairs

    def price_comp(self):
        final_result = []

        for fund_id in self.fund_indicators:
            for index_id in self.index_indicators:
                fund_nav_tb = self.fund_indicators[fund_id].fund_price_info[['datetime', 'adjusted_net_value']]
                index_nav_tb = self.index_indicators[index_id].index_price_info[['date', 'close']]

                merged_table = fund_nav_tb.merge(index_nav_tb, how='inner', left_on='datetime', right_on='date')
                merged_table['PR'] = merged_table['adjusted_net_value'] / merged_table['close']
                merged_table['PR_final'] = merged_table['PR'] / merged_table['PR'][0]

                final_result.append((fund_id, index_id, merged_table))
        
        for fund_id in self.fund_indicators:
            for asset_symbol in self.asset_list:
                fund_nav_tb = self.fund_indicators[fund_id].fund_price_info[['datetime', 'adjusted_net_value']]
                index_nav_tb = self.asset_tb[['date', asset_symbol]]
                merged_table = fund_nav_tb.merge(index_nav_tb, how='inner', left_on='datetime', right_on='date')
                merged_table['close'] = merged_table[asset_symbol].astype(float)
                merged_table['PR'] = merged_table['adjusted_net_value'] / merged_table['close']
                merged_table['PR_final'] = merged_table['PR'] / merged_table['PR'][0]

                final_result.append((fund_id, asset_symbol, merged_table))

        return final_result 
