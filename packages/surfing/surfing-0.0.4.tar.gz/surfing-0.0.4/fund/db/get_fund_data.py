
import pymysql
import pandas as pd
import numpy as np
from pprint import pprint
import sys

'''
Load data from database and transhfer data to dataframe
'''


class LoadDataFromDB():

    def __init__(self, user_name, password, url='fundinfo.cq1tbd5lkqzo.rds.cn-northwest-1.amazonaws.com.cn',
                 database_name='quant_data', encode='utf8'):
        self.url = url
        self.user_name = user_name
        self.password = password
        self.database_name = database_name
        self.encode = encode
        try:
            self.connect = pymysql.connect(
                                host = self.url, 
                                user = self.user_name,
                                password = self.password,
                                database = self.database_name,
                                charset = self.encode 
                                )
            # print('成功链接数据库 %s'%(self.database_name))
            
        except:
            print('连接数据库失败')
        
    def construct_sql(self, table_name, column_names = None, select_columns = None, aim_values = None, operator = '=', mode = 'and', count = None):
        if column_names != None:
            column_names = ["`" + i + "`" for i in column_names]
        if select_columns != None:
            select_columns = ["`" + i + "`" for i in select_columns]
        table_name = self.database_name + '.' + table_name
        sql = ''
        if column_names:
            sql = 'select %s from %s' % (''.join([(i + ',') for i in column_names])[:-1], table_name)
            if select_columns:
                if len(select_columns) == 1:
                    sql = 'select %s from %s where %s%s%s'%(''.join([(i + ',') for i in column_names])[:-1], table_name, select_columns[0], operator[0], "'" + aim_values[0] + "'")
                elif len(select_columns) >1:
                    if isinstance(operator, str):
                        sql = 'select %s from %s where %s%s%s'%(''.join([(i + ',') for i in column_names])[:-1], table_name, select_columns[0], operator, "'" + aim_values[0] + "'")
                    
                        if isinstance(mode, str):
                            for i in range(1, len(select_columns)):
                                sql += ' %s %s%s%s'%(mode, select_columns[i], operator, "'" + aim_values[i] + "'")
                        elif isinstance(mode, list):
                            for i in range(1, len(select_columns)):
                                sql += ' %s %s%s%s'%(mode[i - 1], select_columns[i], operator, "'" + aim_values[i] + "'")
                            sql = sql[:-1]
                    elif isinstance(operator, list):
                        sql = 'select %s from %s where %s%s%s'%(''.join([(i + ',') for i in column_names])[:-1], table_name, select_columns[0], operator[0], "'" + aim_values[0] + "'")
                        if isinstance(mode, str):
                            for i in range(1, len(select_columns)):
                                sql += ' %s %s%s%s'%(mode, select_columns[i], operator[i], "'" + aim_values[i] + "'")
                        elif isinstance(mode, list):
                            for i in range(1, len(select_columns)):
                                sql += ' %s %s%s%s'%(mode[i - 1], select_columns[i], operator[i], "'" + aim_values[i] + "'")
            elif select_columns == None:
                pass
        elif column_names == None:
            if select_columns == None:
                sql = 'select * from %s' % (table_name)
            if select_columns:
                if len(select_columns) == 1:
                    sql = 'select * from %s where %s%s%s'%(table_name, select_columns[0], operator[0], "'" + aim_values[0] + "'")
                elif len(select_columns) >1:
                    if isinstance(operator, str):
                        sql = 'select * from %s where %s%s%s'%(table_name, select_columns[0], operator, "'" + aim_values[0] + "'")
                    
                        if isinstance(mode, str):
                            for i in range(1, len(select_columns)):
                                sql += ' %s %s%s%s'%(mode, select_columns[i], operator, "'" + aim_values[i] + "'")
                        elif isinstance(mode, list):
                            for i in range(1, len(select_columns)):
                                sql += ' %s %s%s%s'%(mode[i-1], select_columns[i], operator, "'" + aim_values[i] + "'")
                    elif isinstance(operator, list):
                        sql = 'select * from %s where %s%s%s'%(table_name, select_columns[0], operator[0], "'" + aim_values[0] + "'")
                        if isinstance(mode, str):
                            for i in range(1, len(select_columns)):
                                sql += ' %s %s%s%s'%(mode, select_columns[i], operator[i], "'" + aim_values[i] + "'")
                        elif isinstance(mode, list):
                            for i in range(1, len(select_columns)):
                                sql += ' %s %s%s%s'%(mode[i - 1], select_columns[i], operator[i], "'" + aim_values[i] + "'")
        if count == None:
            pass
        else:
            sql += ' limit %s' % (count)
        return sql

    def get_data_columns(self, cursor):
        return [i[0] for i in cursor.description]

    def transfer_data_to_df(self, data_tuple, cursor):
        columns = self.get_data_columns(cursor)
        data_df = pd.DataFrame(np.array([list(i) for i in data_tuple]))
        if data_df.shape[0] >0 and data_df.shape[1] > 0:
            data_df.columns = columns
            return data_df
        else:
            return None
                               
    def get_data(self, table_name, column_names = None, select_columns = None, aim_values = None, operator = '=', mode = 'and', count = None):
        sql = self.construct_sql(table_name, column_names, select_columns, aim_values, operator, mode, count)
        with self.connect.cursor() as cu:
            cu.execute(sql)
            result = cu.fetchall()
            return self.transfer_data_to_df(result, cu)
    
    def get_data_from_sql(self, sql):
        with self.connect.cursor() as cu:
            cu.execute(sql)
            result = cu.fetchall()
            return self.transfer_data_to_df(result, cu)


class DataLoader(LoadDataFromDB):

    def __init__(self, user_name, password, url='fundinfo.cq1tbd5lkqzo.rds.cn-northwest-1.amazonaws.com.cn',
                 database_name='quant_data', encode='utf8'):
        super(DataLoader, self).__init__(user_name, password, url, database_name, encode)
        # self.mappin_function()

    def get_all_table_names(self):
        with self.connect.cursor() as cu:
            cu.execute('show tables')
            table_name_list = cu.fetchall()
        return [i[0] for i in table_name_list]

    def mappin_function(self):
        all_table_names = self.get_all_table_names()
        for table_name in all_table_names:
            tmp = "self.get_%s = self.defind('%s', depend_date_columns = '%s')" % (table_name, table_name, 'datetime')
            exec(tmp)

    def defind(self, table_name, depend_date_columns=None):
        function = None
        if depend_date_columns:
            def data_load(start_time=None, end_time=None, count=10):
                if start_time and end_time:
                    return self.get_data(table_name=table_name, count=count,
                                         select_columns=[depend_date_columns, depend_date_columns],
                                         aim_values=[start_time, end_time], operator=['>=', '<='])
                else:
                    return self.get_data(table_name, count)

            function = data_load
            return function
        else:
            def data_load(count=10):
                return self.get_data(table_name, count)

            function = data_load
            return function



