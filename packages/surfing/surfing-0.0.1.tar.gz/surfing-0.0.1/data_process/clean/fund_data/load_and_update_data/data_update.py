import pymysql
import pandas as pd
import datetime as dt
import numpy as np
from get_fund_data import LoadDataFromDB
from sqlalchemy import create_engine
import sys
from download_rqdata_fund import FundDownloadUtility
from download_index_stock import stock_downloader, index_downloader

class DataUpdate():

    def __init__(self, user_name, password, update_rules, url = 'fundinfo.cq1tbd5lkqzo.rds.cn-northwest-1.amazonaws.com.cn', database_name = 'quant_data', encode = 'utf8'):
        
        
        
        self.url = url
        self.user_name = user_name
        self.password = password
        self.database_name = database_name
        self.encode = encode
        self.date_list = []
        self.update_rules = {}
        self.origin_update_rules = update_rules
        self._load_update_rules()
        self.data_loader = LoadDataFromDB(url = url, user_name = user_name, password = password, database_name = database_name, encode = 'utf8')
        self.connect = pymysql.connect(
                            host = self.url,
                            user = self.user_name,
                            password = self.password,
                            database = self.database_name,
                            charset = self.encode
                            )
        self.engine = create_engine('mysql+pymysql://%s:%s@%s:3306/%s'%(self.user_name, self.password, self.url, self.database_name))

    def check_timely_run(self, table_name):
        if self.update_rules[table_name]['depend_column']:
            pass
        else:
            pass

    # 自动更新主函数
    def data_update(self):
        for table_name in self.update_rules:
            if table_name != 'stock_daily_price':
                self._init_table(table_name)
                old_data = self._get_single_last_data_from_DB(table_name)
                new_data = self._get_new_data(table_name)
                self.data_update_routine(table_name, old_data, new_data)
            else:
                self._init_table(table_name)
                begin_date_string = self._get_recent_update_date(table_name)
                begin_date_datetime = self._trans_string_to_datetime(begin_date_string).date()
                curent_datetime = self._get_current_date()
                def date_generation(begin_datetime, end_datetime):
                    while True:
                        if begin_datetime < end_datetime:
                            begin_datetime += dt.timedelta(days = 2)
                            yield begin_datetime
                        else:
                            return end_datetime
                date_generator = date_generation(begin_date_datetime, curent_datetime)
                for date_datetime in date_generator:
                    date_string = self._trans_datetime_to_string(date_datetime)
                    old_data = self._get_single_last_data_from_DB(table_name)
                    new_data = self._get_new_data(table_name, date_string)
                    self.data_update_routine(table_name, old_data, new_data)
                    print('%s 数据更新完毕'%(date_string))

    def data_update_routine(self, table_name, old_data, new_data):
        old_data, new_data = self._check_df(old_data, new_data)
        old_data, new_data = self.deal_data_type(old_data, new_data)
        new_data = new_data.astype('object')
        old_data = old_data.astype('object')
        data_append, data_replace, data_assert = self.filter_df(table_name, old_data, new_data)
        self.append_data(table_name, data_append)
        self.replace_data(table_name, data_replace)
        self.assert_data(table_name, data_assert)



    # 加载自动更新规则
    def _load_update_rules(self):
        self._parse_update_rules(self.origin_update_rules)
        print('自动更新规则已加载')

    def _parse_update_rules(self, update_rules):
        for key in update_rules.keys():
            self.update_rules[key] = {}
            if update_rules[key]['column']:
                self.update_rules[key]['depend_column'] = update_rules[key]['column']
            else:
                self.update_rules[key]['depend_column'] = False
            self.update_rules[key]['frequency'] = update_rules[key]['frequency']
            self.update_rules[key]['primary_key'] = update_rules[key]['primary_key']
            self.update_rules[key]['mode'] = update_rules[key]['mode']
            self.update_rules[key]['download_resource'] = update_rules[key]['download_resource']

    # 时间、字符串处理工具函数
    def _trans_datetime_to_string(self, datetime):
        return dt.datetime.strftime(datetime, '%Y%m%d')

    def _trans_string_to_datetime(self, string):
        return dt.datetime.strptime(string, '%Y%m%d')

    def _get_current_date(self):
        return dt.datetime.now().date()

# 获取mysql数据库中相关数据工具函数
    def _get_table_columns(self, table_name):
        sql = 'select * from %s.%s limit 5'%(self.database_name, table_name)
        with self.connect.cursor() as cu:
            cu.execute(sql)
            return [i[0] for i in cu.description]

    # 初始化表状态
    def _init_table(self, table_name):
        column_names = self._get_table_columns(table_name)
        current_date_string = self._trans_datetime_to_string(self._get_current_date())
        if self.update_rules[table_name]['depend_column']:
            print('数据表%s具有时间依赖列，无需额外添加'%(table_name))
            if 'update_time' in column_names:
                with self.connect.cursor() as cu:
                    sql = 'alter table {}.{} drop column update_time'.format(self.database_name, table_name)
                    cu.execute(sql)
                    print('错误的在表中添加了update_time, 现已删除')
            if 'manual_operation' in  column_names:
                print('数据表%s已经添加人工修正参考列， 初始化已完成'%(table_name))
            else:
                sql = 'alter table %s.%s add column (manual_operation int (3) default %s)' % (self.database_name, table_name, str(0))
                with self.connect.cursor() as cu:
                    cu.execute(sql)
                print('数据表%s已经添加人工修正参考列， 初始化完成'%(table_name))
        else:
            self.update_rules[table_name]['depend_column'] = 'update_time'
            if 'update_time' not in column_names:
                sql = 'alter table %s.%s add column (update_time varchar(10) default %s)' % (self.database_name, table_name, current_date_string)
                with self.connect.cursor() as cu:
                    cu.execute(sql)
                print("数据表%s无时间参照列， 添加参照列'update_time'"%(table_name))
            else:
                sql_unsafe_mode = 'SET SQL_SAFE_UPDATES = 0'
                sql = 'update %s.%s set update_time=%s'%(self.database_name, table_name, current_date_string)
                sql_safe_mode = 'SET SQL_SAFE_UPDATES = 0'
                with self.connect.cursor() as cu:
                    cu.execute(sql_unsafe_mode)
                    cu.execute(sql)
                    self.connect.commit()
                    cu.execute(sql_safe_mode)
                print('数据表%s时间参考列update_time已更新'%(table_name))
            if 'manual_operation' in column_names:
                print('数据表%s已经添加人工修正参考列， 初始化已完成'%(table_name))
            else:
                sql = 'alter table %s.%s add column (manual_operation int (3) default %s)' % (self.database_name, table_name, str(0))
                with self.connect.cursor() as cu:
                    cu.execute(sql)
                print('数据表%s添加人工修正参考列， 初始化完成'%(table_name))

    # 获取表上次更新的时间
    def _get_recent_update_date(self, table_name):
        time_depend_column = self.update_rules[table_name]['depend_column']
        sql = 'select %s from %s.%s order by %s DESC limit 1' % (time_depend_column, self.database_name, table_name, time_depend_column)
        with self.connect.cursor() as cu:
            cu.execute(sql)
            res = cu.fetchall()
            return res[0][0]
        
        
    # 获取表最早的数据的时间
    def _get_earliest_date(self, table_name):
        pass
    
    

    # 用来更新数据的获取函数
    def _get_single_last_data_from_DB(self, table_name):
        
        if self.update_rules[table_name]['mode'] == 'append':
            if self.update_rules[table_name]['download_resource'] == 'stock_qutar':
                recent_update_time = str(self._get_current_date().years) + 'q1'
                return self.data_loader.get_data(table_name, select_columns=[self.update_rules[table_name]['depend_column']], aim_values=[recent_update_time], operator = '>=')

            else:
                recent_update_time = self._get_recent_update_date(table_name)
                return self.data_loader.get_data(table_name, select_columns=[self.update_rules[table_name]['depend_column']], aim_values=[recent_update_time])
        else:
            return self.data_loader.get_data(table_name)
    
    # 获取用来数据检查的函数
    def _get_single_table_data_from_DB_for_check(self, start_date, end_date):
        pass
    
    
        
    def _get_new_data(self, table_name, end_date_string = None):
        start_time_string = self._get_recent_update_date(table_name)
        current_time = self._get_current_date()
        current_time_string = self._trans_datetime_to_string(current_time)
        if table_name != 'stock_daily_price':
            if self.update_rules[table_name]['depend_column'] != 'update_time':
                if self.update_rules[table_name]['download_resource'] == 'fund':
                    print('新数据get')
                    depend_column = self.update_rules[table_name]['depend_column']
                    fund_data_downloader = FundDownloadUtility(date_s = start_time_string, date_e = current_time_string)
                    new_data = eval('fund_data_downloader.get_'+ table_name + '()')
                    new_data = new_data.loc[new_data[depend_column] >= start_time_string]
                elif self.update_rules[table_name]['download_resource'] == 'index':
                    print('新数据get')
                    depend_column = self.update_rules[table_name]['depend_column']
                    index_data_downloader = index_downloader(date_s = start_time_string, date_e = current_time_string)
                    new_data = eval('index_data_downloader.get_'+ table_name + '()')
                    new_data = new_data.loc[new_data[depend_column] >= start_time_string]
                elif self.update_rules[table_name]['download_resource'] == 'stock':
                    print('新数据get')
                    depend_column = self.update_rules[table_name]['depend_column']
                    index_data_downloader = stock_downloader(date_s = start_time_string, date_e = current_time_string)
                    new_data = eval('index_data_downloader.get_'+ table_name + '()')
                    new_data = new_data.loc[new_data[depend_column] >= start_time_string]
                elif self.update_rules[table_name]['download_resource'] == 'stock_quarter':
                    print('新数据get')
                    recent_update_year = int(start_time_string[:4])
                    current_year = int(current_time_string[:4])
                    gap_num = current_year - recent_update_year
                    quarter_num = str((gap_num + 1) * 4)+'q'
                    current_qurtar_string = str(current_year) + 'q4'
                    start_time_quarter_string = str(recent_update_year) + '0101'
                    current_time_quarter_string = str(current_year) + '1231'
                    index_data_downloader = stock_downloader(date_s = start_time_quarter_string, date_e = current_time_quarter_string)
                    new_data = eval('index_data_downloader.get_'+ table_name + "('%s', '%s')"%(current_qurtar_string, quarter_num))
                    depend_column = self.update_rules[table_name]['depend_column']
                    new_data = new_data.loc[new_data[depend_column] >= start_time_string]
            else:
                if self.update_rules[table_name]['download_resource'] == 'fund':
                    print('新数据get')
                    fund_data_downloader = FundDownloadUtility(date_s = start_time_string, date_e = current_time_string)
                    new_data = eval('fund_data_downloader.get_'+ table_name + '()')
                elif self.update_rules[table_name]['download_resource'] == 'index':
                    print('新数据get')
                    index_data_downloader = index_downloader(date_s = start_time_string, date_e = current_time_string)
                    new_data = eval('index_data_downloader.get_'+ table_name + '()')
                elif self.update_rules[table_name]['download_resource'] == 'stock':
                    print('新数据get')
                    index_data_downloader = stock_downloader(date_s = start_time_string, date_e = current_time_string)
                    new_data = eval('index_data_downloader.get_'+ table_name + '()')
                elif self.update_rules[table_name]['download_resource'] == 'stock_quarter':
                    print('新数据get')
                    recent_update_year = int(start_time_string[:4])
                    current_year = int(current_time_string[:4])
                    gap_num = current_year - recent_update_year
                    quarter_num = str((gap_num + 1) * 4)+'q'
                    current_qurtar_string = str(current_year) + 'q4'
                    start_time_quarter_string = str(recent_update_year) + '0101'
                    current_time_quarter_string = str(current_year) + '1231'
                    index_data_downloader = stock_downloader(date_s = start_time_quarter_string, date_e = current_time_quarter_string)
                    new_data = eval('index_data_downloader.get_'+ table_name + "('%s', '%s')"%(current_qurtar_string, quarter_num))
                new_data['update_time'] = [self._trans_datetime_to_string(self._get_current_date()) for i in range(new_data.shape[0])]
            new_data['manual_operation'] = [0 for i in range(new_data.shape[0])]
            return new_data
        else:
            depend_column = self.update_rules[table_name]['depend_column']
            stock_data_downloader = stock_downloader(date_s = start_time_string, date_e = end_date_string)
            new_data = stock_data_downloader.get_stock_daily_price()
            new_data = new_data.loc[new_data[depend_column] >= start_time_string]
            new_data['manual_operation'] = [0 for i in range(new_data.shape[0])]
            return new_data



    
    def _check_df(self, old_data, new_data):
        old_cols = [i for i in old_data.columns]
        new_cols = [i for i in new_data.columns]
        if old_cols == new_cols:
            pass
        else:
            for column in new_cols:
                if column not in old_cols:
                    new_data.drop(column, inplace = True, axis = 1)
        
        old_cols = [i for i in old_data.columns]
        new_cols = [i for i in new_data.columns]
        if old_cols == new_cols:
            pass
        else:
            for i in old_cols:
                if i not in set(old_cols + new_cols):
                    print(i)
            for i in new_cols:
                if i not in set(old_cols + new_cols):
                    print(i)
        return old_data, new_data
    
    def deal_data_type(self, old_df, new_df):
        data_type = new_df.dtypes
        if set(old_df.columns) == set(new_df.columns):
            for col in data_type.index:
                old_df[col] = old_df[col].astype(data_type[col])
            old_df['manual_operation'] = old_df['manual_operation'].astype('float')
            new_df['manual_operation'] = new_df['manual_operation'].astype('float')
            old_df.fillna('null', inplace = True)
            new_df.fillna('null', inplace = True)
            return old_df, new_df

        else:
            for i in old_df.columns:
                if i not in new_df.columns:
                    print(i)
            raise KeyError('两段数据列名不相等')
        
        
    
    def filter_df(self, table_name, old_data, new_data):
        common_data_df, assert_data_df, retain_data_df = self.splite_old_data(table_name, old_data)
        new_data = self.process_with_confirm_data(table_name, retain_data_df, new_data)
        data_append_directly, data_wait_to_replace = self.process_with_common_old_data(table_name, common_data_df, new_data)
        data_wait_to_assert = self.process_with_assert_data(table_name, assert_data_df, new_data)
        return data_append_directly, data_wait_to_replace, data_wait_to_assert


    def splite_old_data(self, table_name, old_data):
        if 'manual_operation' in old_data.columns:
            retain_data_df = old_data[old_data['manual_operation'] == 2]
            assert_data_df = old_data[old_data['manual_operation'] == 1]
            common_data_df = old_data[old_data['manual_operation'] == 0]
            return common_data_df, assert_data_df, retain_data_df
        else:
            raise KeyError('数据表{}没有经过初始化'.format(table_name))
    
    def process_with_common_old_data(self, table_name, common_old_data, new_data):
        
        if isinstance(self.update_rules[table_name]['primary_key'], list):
            other_data_in_old_df, data_append_directly, primary_key_same_old, primary_key_same_new = self.separate_data(
                                                                                common_old_data, 
                                                                                new_data, 
                                                                                key_list = self.update_rules[table_name]['primary_key'])
            
            pass_data, data_to_replace, pass_data2= self.separate_data(primary_key_same_old, primary_key_same_new)
            return data_append_directly, data_to_replace
            
    def process_with_assert_data(self, table_name, assert_df, new_df):
        columns = [i for i in new_df.columns if i != 'manual_operation']
        assert_df = assert_df[columns].astype('object')
        new_df = new_df[columns].astype('object')
        if isinstance(self.update_rules[table_name]['primary_key'], list):
            other_data_in_old_df, data_append_directly, primary_key_same_old, primary_key_same_new = self.separate_data(
                                                                                assert_df, 
                                                                                new_df, 
                                                                             self.update_rules[table_name]['primary_key'])
            pass_data, data_to_asset, pass_data2= self.separate_data(primary_key_same_old, primary_key_same_new)
            data_append_directly['manual_operation'] = [0 for i in range(data_append_directly.shape[0])]
            data_to_asset['manual_operation'] = [0 for i in range(data_to_asset.shape[0])]
            return data_to_asset
        
        
    def process_with_confirm_data(self, table_name, retain_df, new_df):
        columns = [i for i in new_df.columns if i != 'manual_operation']
        retain_df = retain_df[columns].astype('object')
        new_df = new_df[columns].astype('object')
        if isinstance(self.update_rules[table_name]['primary_key'], list):
            other_data_in_old_df, new_data, primary_key_same_old, primary_key_same_new = self.separate_data(
                                                                                retain_df, 
                                                                                new_df, 
                                                                                key_list = self.update_rules[table_name]['primary_key'])
            
            new_data['manual_operation'] = [0 for i in range(new_data.shape[0])]
            return new_data
        
            
    def separate_data(self, df1, df2, key_list = None):
        if key_list is None:
            same_data = pd.merge(df1, df2, how = 'inner')
            other_data_in_df1 = df1.append(same_data).drop_duplicates(keep = False)
            other_data_in_df2 = df2.append(same_data).drop_duplicates(keep = False)
            return other_data_in_df1, other_data_in_df2, same_data
        elif isinstance(key_list, list):
            same_key_data = pd.merge(df1, df2, left_on = key_list, right_on = key_list, how = 'inner')
            tmp_cols_in_df1 = [i + '_x' if i not in key_list else i for i in df1.columns]
            tmp_cols_in_df2 = [i + '_y' if i not in key_list else i for i in df2.columns]
            tmp_data_df1 = same_key_data[tmp_cols_in_df1]
            tmp_data_df2 = same_key_data[tmp_cols_in_df2]
            tmp_cols1 = [i[:-2] if i[-2:] == '_x' else i for i in tmp_data_df1.columns]
            tmp_cols2 = [i[:-2] if i[-2:] == '_y' else i for i in tmp_data_df2.columns]
            tmp_data_df1.columns = tmp_cols1
            tmp_data_df2.columns = tmp_cols2
            other_data_in_df1 = df1.append(tmp_data_df1).drop_duplicates(keep = False)
            other_data_in_df2 = df2.append(tmp_data_df2).drop_duplicates(keep = False)
            return other_data_in_df1, other_data_in_df2, tmp_data_df1, tmp_data_df2


    def append_data(self, table_name, data_append_directly_data_df):
        if not data_append_directly_data_df.empty:
            data_append_directly_data_df.to_sql(table_name, self.engine, index = False, if_exists = 'append')
            print('新数据已插入')
        else:
            print('没有需要插入的新数据')

    def replace_data(self, table_name, replace_data_df):
        if not replace_data_df.empty:
            column_name = self._get_table_columns(table_name)
            replace_data_array = replace_data_df[column_name].values
            contanct_string = ''
            for name in column_name:
                contanct_string += '`' + name + '`' + ', '
            with self.connect.cursor() as cu:
                sql_str = 'replace into %s.%s (%s) values '%(self.database_name, table_name, contanct_string[:-2])
                for item in replace_data_array:
                    item = [str(i)  if str(i) != 'null' else 'null' for i in item]
                    sql_str_command = sql_str + '(' + str(item)[1:-1] + ')'
                    sql_str_command = sql_str_command.replace("\\", '')
                    sql_str_command = sql_str_command.replace(" 'null'", " null")
                    cu.execute(sql_str_command)
                    self.connect.commit()
            print('校对数据，原始数据已经修改:', replace_data_df)
        else:
            print('无数据需要替换')

    def assert_data(self, table_name, assert_by_human_df):
        if not assert_by_human_df.empty:
            print('以下数据是否确认插入?', assert_by_human_df)
            replace_confirm = input('确认 y 拒绝 n： ')
            if replace_confirm == 'y':
                self.replace_data(table_name, assert_by_human_df)
            elif replace_confirm == 'n':
                pass
        else:
            print('没有需要人工判断的数据')
# Api Demo
if __name__ == '__main__':

    user_name, password = sys.argv[1], sys.argv[2]


    test_update_rules = {
        'nav': {
            'column': 'datetime',
            'primary_key': ['order_book_id', 'datetime'],
            'mode': 'append',
            'frequency': 'daily',
            'download_resource': 'fund'
        },
        # 'asset_allocation': {
        #     'column': 'release_date',
        #     'primary_key': ['order_book_id', 'release_date'],
        #     'mode': 'append',
        #     'frequency': 'mothly',
        #     'download_resource': 'fund'
        # },
        # 'industry_allocation': {
        #     'column': 'release_date',
        #     'primary_key': ['order_book_id', 'release_date', 'industry'],
        #     'mode': 'append',
        #     'frequency': 'mothly',
        #     'download_resource': 'fund'
        # },
        # 'index_components':{
        #       'column': 'datetime',
        #       'primary_key': ['order_book_id', 'datetime'],
        #       'mode': 'append',
        #       'frequency': 'daily',
        #       'download_resource': 'index'
        # },
        # 'index_price': {
        #     'column': 'date',
        #     'primary_key': ['order_book_id', 'date'],
        #     'mode': 'append',
        #     'frequency': 'daily',
        #     'download_resource': 'index'
        # },
        # 'index_price': {
        #     'column': 'date',
        #     'primary_key': ['order_book_id', 'date'],
        #     'mode': 'append',
        #     'frequency': 'daily',
        #     'download_resource': 'index'
        # },
        # 'stock_cash_flow_statement': {
        #     'column': 'quarter',
        #     'primary_key': ['order_book_id', 'quarter'],
        #     'mode': 'append',
        #     'frequency': 'monthly',
        #     'download_resource': 'stock_quarter'
        # },
        # 'stock_cash_flow_statement_TTM': {
        #     'column': 'quarter',
        #     'primary_key': ['order_book_id', 'quarter'],
        #     'mode': 'append',
        #     'frequency': 'monthly',
        #     'download_resource': 'stock_quarter'
        # },
        # 'stock_balance_sheet': {
        #     'column': 'quarter',
        #     'primary_key': ['order_book_id', 'quarter'],
        #     'mode': 'append',
        #     'frequency': 'monthly',
        #     'download_resource': 'stock_quarter'
        # },
        # 'stock_financial_indicator': {
        #     'column': 'quarter',
        #     'primary_key': ['order_book_id', 'quarter'],
        #     'mode': 'append',
        #     'frequency': 'monthly',
        #     'download_resource': 'stock_quarter'
        # },
        # 'stock_income_statement': {
        #     'column': 'quarter',
        #     'primary_key': ['order_book_id', 'quarter'],
        #     'mode': 'append',
        #     'frequency': 'monthly',
        #     'download_resource': 'stock_quarter'
        # },
        # 'stock_daily_price': {
        #     'column': 'date',
        #     'primary_key': ['order_book_id', 'date'],
        #     'mode': 'append',
        #     'frequency': 'daily',
        #     'download_resource': 'stock'
        # },
        # 'stock_info': {
        #     'column': False,
        #     'primary_key': ['order_book_id'],
        #     'mode': 'update_all',
        #     'frequency': 'monthly',
        #     'download_resource': 'stock'
        # }
    }

    test_station = DataUpdate(user_name = user_name, password = password, 
        url = 'fundinfo.cq1tbd5lkqzo.rds.cn-northwest-1.amazonaws.com.cn', update_rules = test_update_rules, 
        database_name = 'quant_data')

    test_station.data_update()
