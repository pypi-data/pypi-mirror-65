import pandas as pd
import datetime as dt
import matplotlib.pyplot as plt
from get_fund_data import LoadDataFromDB



class MMfundSelectToool:
    def __init__(self, username, password):
        self.mm_fund_ret = None
        self.data_loader = LoadDataFromDB(username, password)
        self.fund_symbol_name = {}
        self.past_month_ret = None
        self.past_one_year_ret = None
        self.past_two_year_ret = None
        self.past_three_year_ret = None

    def get_current_date(self):
        return dt.datetime.now().date()

    def trans_string_to_datetime(self, datetime):
        return dt.datetime.strptime(datetime, '%Y%m%d')

    def trans_datetime_to_string(self, datetime):
        return dt.datetime.strftime(datetime, '%Y%m%d')

    def get_target_date(self):
        date_list = [self.end_date - dt.timedelta(days=30)]
        for i in range(1, 4):
            date_list.append(self.end_date - dt.timedelta(days=365 * i))
        return date_list

    def parse_trade_days(self):
        pass

    def set_compare_condition(self, fund_list, end_date=None):
        self.fund_list = fund_list
        if end_date:
            self.end_date = self.trans_string_to_datetime(end_date)
        else:
            self.end_date = self.get_current_date()

    def get_data(self):
        time_list = self.get_target_date()
        first_day_on_order = min(time_list)
        start_str = self.trans_datetime_to_string(first_day_on_order)
        end_str = self.trans_datetime_to_string(self.end_date)
        self.get_fund_symbol_name(start_str, end_str)
        self.get_mony_market_fund_ret_data(start_str, end_str)
        self.past_month_ret = (self.mm_fund_ret.loc[time_list[0]:] / 10000 + 1).cumprod(axis=0)
        self.past_one_year_ret = (self.mm_fund_ret.loc[time_list[1]:] / 10000 + 1).cumprod(axis=0)
        self.past_two_year_ret = (self.mm_fund_ret.loc[time_list[2]:] / 10000 + 1).cumprod(axis=0)
        self.past_three_year_ret = (self.mm_fund_ret / 10000 + 1).cumprod(axis=0)

    def get_fund_symbol_name(self, start_date, end_date):
        for order_book_id in self.fund_list:
            try:
                fund_symbol = self.data_loader.get_data(table_name='fundlist_wind',
                                                        column_names=['order_book_id', 'transition', 'symbol',
                                                                      'found_date'],
                                                        select_columns=['order_book_id', ],
                                                        aim_values=[order_book_id],
                                                        operator=['='])
            except AssertionError:
                print('{}基金代码不存在'.format(order_book_id))
                break
            fund_symbol_name = ''
            if fund_symbol.shape[0] == 1:
                fund_symbol_name = str(fund_symbol['symbol'].values[0])
            else:
                fund_symbol_name = []
                dt_start = self.trans_string_to_datetime(start_date)
                dt_end = self.trans_string_to_datetime(end_date)

                fund_symbol['found_date'] = pd.to_datetime(fund_symbol['found_date'])
                fund_symbol = fund_symbol[fund_symbol['found_date'] < dt_end]
                pre_symbol = fund_symbol[fund_symbol['found_date'] < dt_start]
                after_symbol = fund_symbol[fund_symbol['found_date'] > dt_start]
                if pre_symbol.shape[0] == 1:
                    fund_symbol_name.append(str(pre_symbol.iloc[-1, :]['symbol']))
                else:
                    pre_symbol = pre_symbol.iloc[-1, :]
                    fund_symbol_name.append(str(pre_symbol['symbol']))
                for i in after_symbol['symbol'].values:
                    fund_symbol_name.append(i)
            self.fund_symbol_name[order_book_id] = fund_symbol_name

    def get_mony_market_fund_ret_data(self, start_date, end_date):
        mm_fund_nav_df = pd.DataFrame()
        for order_book_id in self.fund_list:
            try:
                single_mm_fund_nav_df = self.data_loader.get_data(table_name='nav',
                                                                  column_names=['daily_profit', 'datetime'],
                                                                  select_columns=['order_book_id', 'datetime',
                                                                                  'datetime'],
                                                                  aim_values=[order_book_id, start_date, end_date],
                                                                  operator=['=', '>=', '<='])
                if not single_mm_fund_nav_df.empty:
                    single_mm_fund_nav_df['datetime'] = pd.to_datetime(single_mm_fund_nav_df['datetime'])
                    if order_book_id in self.fund_symbol_name.keys():
                        if isinstance(self.fund_symbol_name[order_book_id], str):
                            mm_fund_nav_df[self.fund_symbol_name[order_book_id]] = \
                            single_mm_fund_nav_df.set_index('datetime', drop=True)['daily_profit'].iloc[::-1]
                        elif isinstance(self.fund_symbol_name[order_book_id], list):
                            mm_fund_nav_df[self.fund_symbol_name[order_book_id][-1]] = \
                            single_mm_fund_nav_df.set_index('datetime', drop=True)['daily_profit'].iloc[::-1]

            except:
                print('{}评估期内没有净值信息'.format(order_book_id))
        if mm_fund_nav_df.empty:
            print('未获取到任何净值数据')
        else:
            self.mm_fund_ret = mm_fund_nav_df.astype('float')

    def summary(self):
        self.get_data()
        for fund_id in self.fund_list:
            if fund_id in self.fund_symbol_name.keys():
                new_plot = plt.figure(figsize=(20, 10))
                ax1 = new_plot.add_subplot(2, 2, 1)
                ax2 = new_plot.add_subplot(2, 2, 2)
                ax3 = new_plot.add_subplot(2, 2, 3)
                ax4 = new_plot.add_subplot(2, 2, 4)
                print(('\n产品{}近3年收益为:%.3f%%。' % (
                            self.past_three_year_ret[self.fund_symbol_name[fund_id]][-1] * 100 - 100)).format(
                    self.fund_symbol_name[fund_id]))
                print(('\n产品{}近2年收益为:%.3f%%。' % (
                            self.past_two_year_ret[self.fund_symbol_name[fund_id]][-1] * 100 - 100)).format(
                    self.fund_symbol_name[fund_id]))
                print(('\n产品{}年内收益为:%.3f%%。' % (
                            self.past_one_year_ret[self.fund_symbol_name[fund_id]][-1] * 100 - 100)).format(
                    self.fund_symbol_name[fund_id]))
                print(('\n产品{}本月收益为:%.3f%%。' % (
                            self.past_month_ret[self.fund_symbol_name[fund_id]][-1] * 100 - 100)).format(
                    self.fund_symbol_name[fund_id]))
                self.past_three_year_ret[self.fund_symbol_name[fund_id]].plot(
                    title='The {} fund PnL in recent three years'.format(fund_id), ax=ax1)
                self.past_two_year_ret[self.fund_symbol_name[fund_id]].plot(
                    title='The {} fund PnL in recent two years'.format(fund_id), ax=ax2, )
                self.past_one_year_ret[self.fund_symbol_name[fund_id]].plot(
                    title='The {} fund PnL in recent one years'.format(fund_id), ax=ax3)
                self.past_month_ret[self.fund_symbol_name[fund_id]].plot(
                    title='The {} fund PnL in recent month'.format(fund_id), ax=ax4)

if __name__ == '__main__':
    test_case = ['159001', '159003', '159005', '511600', '511620', '511650', '511660', '511670', '511680', '511690']
    testtool = MMfundSelectToool('liujiantao', 'Liujiantao123456')
    testtool.set_compare_condition(test_case[:3])
    testtool.summary()