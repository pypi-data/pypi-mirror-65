import matplotlib.pyplot as plt
from fund_timeline_indicators import fund_timeline_indicators
import numpy as np
import pandas as pd

class Display():

    def __init__(self, fti):
        self.fti = fti
        self.fund_symbol = {}
        self.index_symbol = {}
        self.fund_list = self.fti.fund_list
        self.index_list = self.fti.index_list
        self.x_count = 10
        for fund_id in self.fund_list:
            self.fund_symbol[fund_id] = self.fti.dl.get_data('fundlist_wind', column_names=['symbol'], 
                select_columns=['fund_id'], aim_values=[fund_id], operator=['=']).values.flatten()[0]
        for index_id in self.index_list:
            self.index_symbol[index_id] = self.fti.dl.get_data('index_info', column_names=['symbol'], 
                select_columns=['order_book_id'], aim_values=[index_id], operator=['=']).values.flatten()[0]
        
        self.merged_tb = self.get_merged_tb()
    
    def get_merged_tb(self):
        merge_list = []
        for fund_id in self.fund_list:
            origin_pd = self.fti.fund_indicators[fund_id].fund_price_info[['adjusted_net_value', 'datetime']]
            origin_pd['merge_date'] = origin_pd['datetime'].astype('str')
            origin_pd['adjusted_net_value'] = origin_pd['adjusted_net_value'].astype('float')
            origin_pd[fund_id] = origin_pd['adjusted_net_value'] / origin_pd['adjusted_net_value'][0]
            m_pd = origin_pd.drop(columns=['adjusted_net_value', 'datetime'])
            merge_list.append(m_pd)

        for index_id in self.index_list:
            origin_pd = self.fti.index_indicators[index_id].index_price_info[['date', 'close']]
            origin_pd['merge_date'] = origin_pd['date'].astype('str')
            origin_pd['close'] = origin_pd['close'].astype('float')
            origin_pd[index_id] = origin_pd['close'] / origin_pd['close'][0]
            m_pd = origin_pd.drop(columns=['date', 'close'])
            merge_list.append(m_pd)
        
        for asset_name in self.fti.asset_list:
            origin_pd = self.fti.asset_tb[['date', asset_name]]
            origin_pd['merge_date'] = origin_pd['date'].astype('str')
            origin_pd['close'] = origin_pd[asset_name].astype('float')
            origin_pd[asset_name] = origin_pd['close'] / origin_pd['close'][0]
            m_pd = origin_pd.drop(columns=['date', 'close'])
            merge_list.append(m_pd)

        merged_tb = merge_list[0]
        for i in range(1, len(merge_list)):
            merged_tb = merged_tb.merge(merge_list[i], on='merge_date', how='outer')
        merged_tb = merged_tb.sort_values(by=['merge_date'], ignore_index=True, ascending=True)
        
        return merged_tb
    
    def show_300(self):
        fund_results, index_results, month_pairs, year_pairs = self.fti.get_300_indicators()

        indicators_tb_col = ['组合', '年化收益', '年化波动', '夏普率', '最大回撤']
        month_ret_tb_col = ['年']
        for m in range(1, 13):
            month_ret_tb_col.append(str(m) + '月')
        month_ret_tb_col.append('年度收益率')

        indicators_list = []
        for fund_id in self.fund_list:
            new_row = []
            new_row.append(self.fund_symbol[fund_id])
            new_row.append(fund_results[fund_id]['AADR'])
            new_row.append(fund_results[fund_id]['Volatility'])
            new_row.append(fund_results[fund_id]['SR'])
            new_row.append(fund_results[fund_id]['MDD'])
            indicators_list.append(new_row)

        for index_id in self.index_list:
            new_row = []
            new_row.append(self.index_symbol[index_id])
            new_row.append(index_results[index_id]['AADR'])
            new_row.append(index_results[index_id]['Volatility'])
            new_row.append(index_results[index_id]['SR'])
            new_row.append(index_results[index_id]['MDD'])
            indicators_list.append(new_row)

        indicators_tb = pd.DataFrame(indicators_list, columns=indicators_tb_col).set_index('组合')

        mon_tb_list = {}
        for fund_id in self.fund_list:
            start_year = int(year_pairs[0][0][:4])
            end_year = int(year_pairs[-1][-1][:4])
            month_index = 0
            year_index = 0
            mon_len = len(month_pairs)
            month_ret_list = []
            for y in range(start_year, end_year + 1):
                new_row = [y]
                for m in range(1, 13):
                    if month_index >= mon_len:
                        new_row.append(np.nan)
                        continue
                    cur_s, cur_e = month_pairs[month_index]
                    cur_y = int(cur_s[:4])
                    cur_m = int(cur_s[4:6])
                    if cur_y == y and cur_m == m:
                        new_row.append(fund_results[fund_id]['month_ret'][month_index])
                        month_index += 1
                    else:
                        new_row.append(np.nan)
                new_row.append(fund_results[fund_id]['year_ret'][year_index])
                year_index += 1
                month_ret_list.append(new_row)

            month_ret_tb = pd.DataFrame(month_ret_list, columns=month_ret_tb_col).set_index('年')
            mon_tb_list[fund_id] = month_ret_tb
        
        plt.figure(figsize=(15, 5))
        plt.title('300 Value Analysis')
        x = self.merged_tb['merge_date']

        for fund_id in self.fund_list:
            cur_y = self.merged_tb[fund_id].values
            plt.plot(x, cur_y, label=fund_id)
        for index_id in self.   index_list:
            cur_y = self.merged_tb[index_id].values
            plt.plot(x, cur_y, label=index_id)
            
        plt.legend()
        plt.xlabel('Years')
        plt.ylabel('Rate')

        interval = int(len(x) / self.x_count)
        plt.xticks(np.arange(0, len(x), interval), rotation=70)
        plt.show()

        return indicators_tb, mon_tb_list, self.merged_tb
    
    def show_pr(self):
        re = self.fti.price_comp()
        # Draw NET
        plt.figure(figsize=(15, 5))
        plt.title('Net Value')
        x = self.merged_tb['merge_date']

        for fund_id in self.fund_list:
            print(self.fund_symbol[fund_id])
            cur_y = self.merged_tb[fund_id].values
            plt.plot(x, cur_y, label=fund_id)
        
        for index_id in self.index_list:
            print(self.index_symbol['index_id'])
            cur_y = self.merged_tb[index_id].values
            plt.plot(x, cur_y, label=index_id)
        
        for asset_name in self.fti.asset_list:
            print(asset_name)
            cur_y = self.merged_tb[asset_name].values
            plt.plot(x, cur_y, label=asset_name)

        plt.legend()
        plt.xlabel('Years')
        plt.ylabel('Rate')

        interval = int(len(x) / self.x_count)
        if interval <= 0:
            interval = 1
        plt.xticks(np.arange(0, len(x), interval), rotation=70)
        plt.show()
        # DRAW PR
        plt.figure(figsize=(15, 5))
        plt.title('Price Comp')

        date_tb = self.merged_tb.filter(items=['merge_date'])
        for fund_id, index_id, pr_tb in re:
            cur_tb = date_tb.merge(pr_tb, left_on='merge_date', right_on='datetime', how='left')

            x = cur_tb['merge_date']
            cur_y = cur_tb['PR_final'].values
            plt.plot(x, cur_y, label=fund_id + '/' + index_id)

        plt.legend()
        plt.xlabel('Years')
        plt.ylabel('Rate')

        interval = int(len(x) / self.x_count)
        plt.xticks(np.arange(0, len(x), interval), rotation=70)
        plt.show()

        return re, self.merged_tb
