import numpy as np
import pandas as pd

class CleanBase:
    
    METHOD_MAP = {
        'candle'    :   'bars',
        'ticker'    :   'ticks',
        'trade'     :   'trades',
        'depth'     :   'depths',
        'bar'       :   'bars',
        'ticks'     :   'ticks',
        'trades'    :   'trades',
        'depths'    :   'depths',
    }
    def __init__(self, msg=None):
        self.msg = msg

    def remove(self, column_list): 
        try:
            for i in self.DROP_COLUMN:
                column_list.remove(i)
        except:
            content =  'origin column    : {} \
                        delete column    : {}'.format(column_list,self.DROP_COLUMN)
            self.msg.send(content = content, is_error = True, chat_con = True)
            raise SystemExit
            
        return column_list
    
    def replace(self, match_dict, lists):
        return [self.match(match_dict, i) for i in lists]

    def columns(self):
        return [i[0] for i in self.datatype]
    
    def match(self, match_dict, i):
        try:
            return match_dict[i]
        except Exception as e:
            self.msg.send(content = '{} not in match'.format(e), is_error = True, chat_con = True)
            raise SystemExit
            
    def sorted_datatype(self, datatype):
        return datatype.sort(key= lambda k:k[0])

    def format_time(self, i):
        return i.replace('-','')

    def seperate_input(self, i, source):
        if source == 'btcta':
            start_date = i[0]
            end_date   = i[1]
            ticker     = i[2]
            exchange   = i[3]
        else:          
            start_date = self.format_time(i[0])
            end_date   = self.format_time(i[1])
            ticker     = i[2].split('/')[1]
            exchange   = i[2].split('/')[0]
        return start_date, end_date, ticker, exchange

    def clean_element(self, data_class, df):
        dc = data_class()
        column_removed = dc.remove(list(df.columns.copy()))
        column_replaced = dc.replace(dc.MATCH_DICT, column_removed)
        df = df[column_removed].copy()
        df.columns = column_replaced
        df = df[sorted(column_replaced)]
        df = dc.change_time(df)
        df = [tuple(x) for x in df.values]
        df = np.array(df, dtype = self.sorted_datatype(dc.DATA_TYPE)) 
        return df

    def clean_tick(self, source, exchange, method, ticker, start_date, end_date, data_class, uti):
        date_list = [i.strftime("%Y-%m-%d") for i in list(pd.date_range(start_date, end_date))]
        self.msg.send(content = '     clean {} {}'.format(method,ticker), is_error = False, chat_con = True)
        for date in date_list:
            key = '{}/{}/{}/{}/{}.gz'.format(source, exchange, self.METHOD_MAP[method], ticker, date)
            self.msg.send(content = 'clean {} data with key: {}'.format(date, key), is_error = False, chat_con = True)
            try:
                df = uti.load_raw(uti.RAW_BUCKET_NAME, key)
            except:
                self.msg.send(content = '     fail key: {}'.format(key), is_error = True, chat_con = True)
                continue
            data = self.clean_element(data_class, df)
            path = uti.normal_save(data)
            uti.upload_file(path, uti.CLEAN_BUCKET_NAME, key)
            
    def clean_group(self, source=None, download_inputs=None, method=None, data_class=None, s3_uti_class=None):
        self.msg.send(content = '##########start  clean###########', is_error = False, chat_con = True)
        uti = s3_uti_class()
        for i in download_inputs:
            start_date, end_date, ticker, exchange = self.seperate_input(i, source)
            self.clean_tick(source, exchange, method, ticker, start_date, end_date, data_class, uti)
        self.msg.send(content = '##########finish clean###########', is_error = False, chat_con = True)
