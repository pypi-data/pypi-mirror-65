import pandas as pd
import datetime as dt
import math
import numpy as np
from get_fund_data import LoadDataFromDB


class StockFundSelectTool:
    def __init__(self, username, password):
        self.data_loader = LoadDataFromDB(username, password)

    # 初始化选基工具，指定行业指数，基金id， 比对的开始和结束日期
    def set_compare_conditions(self, index_id, fund_list, start_time, end_time):
        self.start_date = self.trans_string_to_datetime(start_time)
        self.end_date = self.trans_string_to_datetime(end_time)
        assert (self.start_date < self.end_date), '请输入正确的起止日期'
        self.index_id = index_id
        self.fund_list = fund_list
        self.ret_index = None
        self.no_nav_list = []
        self.ret_nav = None
        self.symbol_name_fund_dict = {}
        self.no_symbol_name = []
        self.holding_position = None
        self.no_holding_info = []

    # 时间处理函数
    def trans_string_to_datetime(self, datetime):
        return dt.datetime.strptime(datetime, '%Y%m%d')

    def trans_datetime_to_string(self, datetime):
        return dt.datetime.strftime(datetime, '%Y%m%d')

    def init(self):
        self.get_ret_index()
        self.get_holding_position()
        self.get_ret_fund()
        self.get_fund_symbol_name()
        self.cal_trace_bias()
        self.cal_trace_mistake()

    # 数据部分函数，运行在self.init()中避免重复拉取数据

    # 获取指数收益信息
    def get_ret_index(self):
        start_date_string = self.trans_datetime_to_string(self.start_date)
        end_date_string = self.trans_datetime_to_string(self.end_date)

        ret_index = self.data_loader.get_data(table_name='index_price',
                                              column_names=['ret', 'date'],
                                              select_columns=['order_book_id', 'date', 'date'],
                                              aim_values=[self.index_id, start_date_string, end_date_string],
                                              operator=['=', '>=', '<='])
        if ret_index is None:
            print('评估期内未找到{}价格数据').format(self.index_id)
        else:
            ret_index['date'] = pd.to_datetime(ret_index['date'])
            ret_index['ret'] = ret_index['ret'].astype('float')
            dret_index = ret_index.set_index(['date'], drop=True)
            dret_index.columns = [self.index_id]
            self.dret_index = dret_index
            ret_index = (ret_index.set_index(['date'], drop=True) + 1).cumprod(axis=0)
            ret_index.columns = [self.index_id]
            self.ret_index = ret_index

    # 获取基金收益信息
    def get_ret_fund(self):
        # 为了防止当前没有数据，向前多获取十天的数据
        past_ten_days = (self.start_date - dt.timedelta(days=10)).date()
        start_date_string = self.trans_datetime_to_string(past_ten_days)
        end_date_string = self.trans_datetime_to_string(self.end_date)
        past_ten_days_string = self.trans_datetime_to_string(past_ten_days)
        nav_fund = pd.DataFrame()
        for order_book_id in self.fund_list:
            single_nav_fund = self.data_loader.get_data(table_name='nav',
                                                        column_names=['adjusted_net_value', 'datetime'],
                                                        select_columns=['order_book_id', 'datetime', 'datetime'],
                                                        aim_values=[order_book_id, past_ten_days_string,
                                                                    end_date_string],
                                                        operator=['=', '>=', '<='])
            if single_nav_fund is not None:
                single_nav_fund.index = pd.to_datetime(single_nav_fund['datetime'])
                single_nav_fund.set_index(['datetime'], drop=True, inplace=True)
                single_nav_fund['adjusted_net_value'] = single_nav_fund['adjusted_net_value'].astype('float')
                single_nav_fund.columns = [order_book_id]
                nav_fund = pd.concat([nav_fund, single_nav_fund], axis=1, ignore_index=False)
            else:
                self.no_nav_list.append(order_book_id)

        if nav_fund.empty:
            print('评估期内全部基金无净值数据')

        else:
            ret_nav = (nav_fund.diff() / nav_fund.shift(1))
            ret_nav.index = pd.to_datetime(ret_nav.index)
            self.dret_nav = ret_nav.loc[self.ret_index.index]
            self.ret_nav = (ret_nav.loc[self.ret_index.index] + 1).cumprod(axis=0)

    # 获取基金的名称
    def get_fund_symbol_name(self):
        for order_book_id in self.fund_list:
            single_symbol_name = self.data_loader.get_data(table_name='fundlist_wind',
                                                           column_names=['symbol', 'found_date'],
                                                           select_columns=['order_book_id'],
                                                           aim_values=[order_book_id],
                                                           operator=['='])
            if single_symbol_name is not None:
                single_symbol_name['found_date'] = pd.to_datetime(single_symbol_name['found_date'])
                self.symbol_name_fund_dict[order_book_id] = []
                if single_symbol_name.shape[0] > 1:
                    single_symbol_name = single_symbol_name.loc[single_symbol_name['found_date'] < self.end_date]
                    if single_symbol_name.loc[single_symbol_name['found_date'] > self.start_date].shape[0] > 0:
                        self.symbol_name_fund_dict[order_book_id] += list(
                            single_symbol_name.loc[single_symbol_name['found_date'] > self.start_date]['symbol'].values)
                    else:
                        single_symbol_name = single_symbol_name.iloc[-1, :]['symbol']
                        self.symbol_name_fund_dict[order_book_id].append(single_symbol_name[-1])
                else:
                    single_symbol_name = single_symbol_name['symbol'].values
                    self.symbol_name_fund_dict[order_book_id].append(single_symbol_name[-1])
            else:
                self.no_symbol_name.append(order_book_id)

    # 获取指数和基金的持仓比重
    def get_holding_position(self):
        start_date_string = self.trans_datetime_to_string(self.start_date)
        end_date_string = self.trans_datetime_to_string(self.end_date)
        holiding_position = pd.DataFrame()
        for order_book_id in self.fund_list:
            single_fund_position = self.data_loader.get_data(table_name='holdings',
                                                             column_names=['share_order_book_id', 'weight',
                                                                           'release_date'],
                                                             select_columns=['order_book_id', 'release_date',
                                                                             'release_date'],
                                                             aim_values=[order_book_id, start_date_string,
                                                                         end_date_string],
                                                             operator=['=', '>=', '<='])

            if single_fund_position is not None:
                single_fund_position['release_date'] = pd.to_datetime(single_fund_position['release_date'])
                single_fund_position.sort_values(by='release_date', inplace=True)
                last_date = list(single_fund_position['release_date'].values)[-1]
                single_fund_position = single_fund_position[single_fund_position['release_date'] == last_date]
                single_fund_position.set_index(['share_order_book_id'], drop=True, inplace=True)
                single_fund_position.drop(['release_date'], axis=1, inplace=True)
                single_fund_position.columns = [order_book_id]
                holiding_position = pd.concat([holiding_position, single_fund_position], axis=1, ignore_index=False)

            else:
                self.no_holding_info.append(order_book_id)
        index_position = self.data_loader.get_data(table_name='index_weights',
                                                   column_names=['components', 'weights', 'date'],
                                                   select_columns=['order_book_id', 'date', 'date'],
                                                   aim_values=[self.index_id, start_date_string, end_date_string],
                                                   operator=['=', '>=', '<='])
        if index_position is not None:
            index_position['date'] = pd.to_datetime(index_position['date'])
            index_position.sort_values(by='date', inplace=True)
            last_date = list(index_position['date'].values)[-1]
            index_position = index_position[index_position['date'] == last_date]
            components = eval(index_position['components'].values[-1])
            weights = eval(index_position['weights'].values[-1])
            index_weights_df = pd.DataFrame(np.array([components, weights]), index=['share_order_book_id', 'weight']).T
            index_weights_df.set_index(['share_order_book_id'], drop=True, inplace=True)
            index_weights_df.columns = [self.index_id]
            holiding_position = pd.concat([holiding_position, index_weights_df], axis=1, ignore_index=False)

        else:
            self.no_holding_info.append(self.index_id)
        self.holding_position = holiding_position.astype('float')

    def cal_trace_bias(self):
        self.trace_bias = self.dret_nav - self.dret_index.values

    def cal_trace_mistake(self):
        self.trace_mistake = self.trace_bias.std(axis=0) * math.sqrt(242)

    def summary(self):
        self.init()
        if len(self.no_holding_info) > 0:
            print('如下基金没有找到持仓信息', self.no_holding_info)
        if len(self.no_nav_list) > 0:
            print('如下基金没有找到净值信息')
        if len(self.no_symbol_name) > 0:
            print('如下基金没有找到产品名称信息')
        for id in self.symbol_name_fund_dict.keys():
            print('基金' + str(id) + "产品名与曾用名为:", self.symbol_name_fund_dict[id])
        print('评估期内基金年化追踪误差为:', self.trace_mistake)
        print('下图为基金评估期内追踪偏差序列:')
        self.trace_bias.plot(title='trace_bias', figsize=(15, 8))
        print('下图为基金评估期内收益情况:')
        self.ret_nav[self.index_id] = self.ret_index[self.index_id].values
        self.ret_nav.plot(title='fund_return', figsize=(15, 8))
        print('下图为基金评估期内最近持仓比重信息:')
        self.holding_position.plot(title='fund_return', figsize=(15, 8), kind='bar')
        sort_fund_list = self.trace_mistake.sort_values().index
        print('\n按照追踪偏差进行打分后的基金排序为:%s' % (list(sort_fund_list)))

# Api Demo
if __name__ == '__main__':
    testtool = StockFundSelectTool(username='liujiantao', password='Liujiantao123456')
    testtool.set_compare_conditions(index_id='000300.XSHG',
                                    fund_list=['100038', '000311', '000172', '169101', '166002'], start_time='20190620',
                                    end_time='20191202')
    testtool.summary()