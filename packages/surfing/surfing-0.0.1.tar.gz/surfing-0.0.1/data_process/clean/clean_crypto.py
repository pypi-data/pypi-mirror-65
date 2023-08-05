import os
import io
import zipfile
import json
import gzip
import datetime
import pandas as pd
import numpy as np
from .clean_method import CryptoBarsClean, CryptoTicksClean, CryptoTradesClean
import boto3

class CryptoClean:
    
    EXCHANGE = ['binance', 'bitmex', 'huobi', 'okex']
    DATATYPE = ['trade', 'bar', 'snap']
    PROFILE_MAINLAND = 'default' 
    PROFILE_OVERSEAS = 'overseas'
    RAW_BUCKET_NAME = 'll-raw-data-ap-1'
    CLEAN_BUCKET_NAME = 'll-cleaned-data'
    SOURCE = 'crypto'
    MATCH_MAP = {
        'bar'   :   'bars',
        'snap'  :   'ticks',
        'trade' :   'trades',
    }
    
    def __init__(self,msg=None,surfboard=None,data_type=None):
        if surfboard:
            self.CLIENT_AP = self.get_surfboard()
            self.CLIENT_CN = boto3.client('s3')  
        else:
            self.CLIENT_AP = boto3.Session(profile_name=self.PROFILE_OVERSEAS).client('s3')
            self.CLIENT_CN = boto3.Session(profile_name=self.PROFILE_MAINLAND).client('s3')
        self.msg = msg
        self.data_type = data_type
        self.data_columns= {
            'ticks'  : self.get_column(CryptoTicksClean),
            'trades' : self.get_column(CryptoTradesClean)
        }
        self.check_data_folder()

    def get_surfboard(self):
        bucket_name = 'surfboard'
        key = 'aws/surfboard.json'
        s3 = boto3.client('s3')
        retr = s3.get_object(Bucket = bucket_name, Key = key)
        bytestream = io.BytesIO(retr['Body'].read())
        surfboard_json = json.load(bytestream)
        s3_client_ap = boto3.Session(
                                        region_name             =  surfboard_json['region'],
                                        aws_access_key_id       =  surfboard_json['apak'],
                                        aws_secret_access_key   =  surfboard_json['apsk'],
                    ).client('s3')
        return s3_client_ap
    
    def check_data_folder(self):
        path = 'data'
        if not os.path.exists(path):
            os.makedirs(path)

    def get_column(self, data_class):
        return sorted([i[0] for i in data_class.DATA_TYPE])

    def get_dic_keys(self, dic):
        return sorted(list(dic.keys()))

    def load_s3_zip_obj(self, bucket_name, key):
        retr = self.CLIENT_AP.get_object(Bucket=bucket_name,Key=key)
        bytestream = io.BytesIO((retr['Body'].read()))
        zf = zipfile.ZipFile(file=bytestream)
        content = zf.open(zf.namelist()[0])
        df = pd.read_csv(content)
        return df

    def download_zip_get_df(self, bucket_name, key):
        zip_file_path = 'data.zip'
        self.CLIENT_AP.download_file(   Bucket=bucket_name,
                                        Key=key, 
                                        Filename=zip_file_path,
                                        Config = boto3.s3.transfer.TransferConfig(
                                                num_download_attempts   =   20,
                                                max_io_queue            =   500,
                                                io_chunksize            =   524288,
                                            )
                                    )
        zf = zipfile.ZipFile(file=zip_file_path)
        content = zf.open(zf.namelist()[0])
        df = pd.read_csv(content)
        df = self.change_tz(df, 'time')
        df = self.change_tz(df, 'frame_dt')
        return df
    
    def cleaned_obj_date_list(self, exchange, data_type):
        prefix = '{}/{}/{}'.format(self.SOURCE, exchange, data_type)
        res = self.CLIENT_CN.list_objects_v2(Bucket = self.CLEAN_BUCKET_NAME, Prefix = prefix)
        res = [i['Key'].split('/')[-1].split('.')[0] for i in res['Contents']]
        res = sorted(list(set(res)))
        return res

    def existed_obj_raw(self):        
        existed_obj = {}
        for exchange in self.EXCHANGE:
            existed_obj[exchange] = {}
            for datatype in self.DATATYPE:
                existed_obj[exchange][datatype] = {}
                prefix = '{}/{}/{}'.format(self.SOURCE, exchange, datatype)
                res = self.CLIENT_AP.list_objects_v2(Bucket = self.RAW_BUCKET_NAME, Prefix = prefix)
                existed_obj[exchange][datatype] = {}
                try:
                    for con_i in res['Contents']:
                        key_date = con_i['Key'].split('/')[3]
                        if key_date in list(existed_obj[exchange][datatype].keys()):
                            existed_obj[exchange][datatype][key_date].append(con_i['Key'])
                        else:
                            existed_obj[exchange][datatype][key_date] = [con_i['Key']]
                except:
                    continue
        return existed_obj

    def update_obj(self):
        exsited_obj = self.existed_obj_raw()
        exchange_list = self.get_dic_keys(exsited_obj) 
        for exchange in exchange_list:
            data_type_list = self.get_dic_keys(exsited_obj[exchange])
            for data_type in data_type_list:
                try:
                    cleaned_date_list = self.cleaned_obj_date_list(exchange,data_type)
                except:
                    continue
                key_list = list(exsited_obj[exchange][data_type].keys())
                delete_list = list(set(cleaned_date_list) & set(key_list))
                for delete_key in delete_list:
                    del exsited_obj[exchange][data_type][delete_key]
        return exsited_obj
                
    def process_hour_data_to_date(self, key_list, data_type):
        df_list = [] 
        for key in key_list:
            if data_type == 'snap':
                content = f'snap: {key}'
                self.msg.send(content, is_error = False, chat_con=True)
            try:
                df = self.download_zip_get_df(self.RAW_BUCKET_NAME, key)
            except Exception as ex:
                content = 'download and clean key error: {}, exception: {}'.format(key, ex)
                self.msg.send(content, is_error = True, chat_con=True)
                continue
            df_list.append(df)
        df_date = pd.concat(df_list).sort_values(by='time')
        return df_date

    def loop_download_raw(self, key):
        zip_file_path = 'data/data_{}.zip'.format(key.split('_')[-1].split('.')[0])
        self.CLIENT_AP.download_file(   Bucket=self.RAW_BUCKET_NAME,
                                        Key=key, 
                                        Filename=zip_file_path,
                                        Config = boto3.s3.transfer.TransferConfig(
                                                num_download_attempts   =   20,
                                                max_io_queue            =   500,
                                                io_chunksize            =   524288,
                                            )
                                    )
        print('download finish: {}'.format(key))
        return zip_file_path

    def process_hour_zip(self, res, keylist):
        df_list = []
        for i in res:
            try:
                zf = zipfile.ZipFile(file=i)
                content = zf.open(zf.namelist()[0])
                df = pd.read_csv(content)
                df_list.append(df)
            except Exception as ex:
                content = 'clean key error: {} exception: {}'.format(keylist[res.index(i)], ex)
                self.msg.send(content, is_error = True, chat_con=True)
                continue
        df_date = pd.concat(df_list).sort_values(by='time')
        return df_date

    def process_hour_data_to_date_v2(self, key_list, data_type):
        zip_file_list = []
        key_list_res = []
        for key in key_list:
            try:
                zip_file_path = 'data/data_{}.zip'.format(key.split('_')[-1].split('.')[0])
                self.CLIENT_AP.download_file(   
                    Bucket=self.RAW_BUCKET_NAME,
                    Key=key, 
                    Filename=zip_file_path,
                    Config = boto3.s3.transfer.TransferConfig(
                        num_download_attempts   =   20,
                        max_io_queue            =   500,
                        io_chunksize            =   524288,
                        )
                    )
                zip_file_list.append(zip_file_path)
                if data_type == 'snap':
                    content = f'snap: {key} downloaded'
                    self.msg.send(content, is_error = False, chat_con=True)
                key_list_res.append(key)
            except Exception as ex:
                content = 'download key error: {}, exception: {}'.format(key, ex)
                self.msg.send(content, is_error = True, chat_con=True)
                continue
        df_data = self.process_hour_zip(sorted(zip_file_list),sorted(key_list_res))
        return df_data

    def separate_data_by_ticker(self, df):
        ticker_list  = sorted(list(set(df.ticker.tolist())))
        df_list = [df[df['ticker'] == i].copy() for i in ticker_list]
        return ticker_list, df_list

    def existed_clean_obj(self, source):
        existed_obj = {}
        for exchange in self.EXCHANGE:
            existed_obj[exchange] = {}
            for data_type in ['trades', 'ticks']:
                existed_obj[exchange][data_type] = {}
                prefix = '{}/{}/{}'.format(source, exchange, data_type)
                res = self.CLIENT_CN.list_objects_v2(Bucket = self.CLEAN_BUCKET_NAME, Prefix = prefix)
                existed_obj[exchange][data_type] = {}
                try:
                    for con_i in res['Contents']:
                        ticker = con_i['Key'].split('/')[3]
                        if ticker in list(existed_obj[exchange][data_type].keys()):
                            existed_obj[exchange][data_type][ticker].append(con_i['Key'])
                        else:
                            existed_obj[exchange][data_type][ticker] = [con_i['Key']]
                except Exception as e:
                    content = f"Exception as {e}"
                    print(content)
                    continue
        return existed_obj

    def today_next_day_from_str_day(self, today):
        today = datetime.datetime.strptime(today, "%Y-%m-%d")
        next_day = today + datetime.timedelta(days=1)
        today = pd.to_datetime(today, format='%Y-%m-%dT%H:%M:%S.%fZ').tz_localize('Asia/Shanghai')
        next_day = pd.to_datetime(next_day, format='%Y-%m-%dT%H:%M:%S.%fZ').tz_localize('Asia/Shanghai')
        return today, next_day
               
    def get_mktime_from_key(self, key, data_type):
        retr = self.CLIENT_CN.get_object(Bucket=self.CLEAN_BUCKET_NAME, Key=key)
        bytestream = io.BytesIO(retr['Body'].read())
        data = gzip.GzipFile(None, 'rb', fileobj=bytestream)       
        data = np.load(data, allow_pickle=True)
        df = pd.DataFrame(data, columns = self.data_columns[data_type])
        df_time = pd.to_datetime(df['mkt_time'], unit='ns')
        df_time = df_time.dt.tz_localize('UTC').dt.tz_convert('Asia/Shanghai')
        df_time = pd.to_datetime(df_time, format='%Y-%m-%dT%H:%M:%S.%fZ')
        today = key.split('/')[-1].split('.')[0]
        today, next_day = self.today_next_day_from_str_day(today)
        df_time = pd.Series(today).append(df_time).append(pd.Series(next_day))
        df_time = df_time.reset_index(drop=True)
        return df_time

    def clean_check_all(self, minutes):
        source = 'crypto'
        exsited_obj = self.existed_clean_obj(source)
        result = {}
        for exchange in self.EXCHANGE:
            result[exchange] = {}
            for data_type in ['trades', 'ticks']:
                result[exchange][data_type] = {}
                ticker_list = exsited_obj[exchange][data_type]
                for ticker in ticker_list:
                    key_list = sorted(exsited_obj[exchange][data_type][ticker])
                    for key in key_list:
                        df_time = self.get_mktime_from_key(key, data_type)
                        df_time_dif = df_time.diff(1)
                        con_list = df_time_dif > datetime.timedelta(minutes=minutes)
                        if True in con_list:
                            res = []
                            for i in df_time[con_list].index.tolist():
                                res.append([df_time[i-1], df_time[i]])
                            if ticker in list(result[exchange][data_type].keys()):
                                result[exchange][data_type][ticker].extend(res)
                            else:
                                result[exchange][data_type][ticker] = [res]
        return result

    def clean_check_element(self, key, data_type, minutes):
        df_time = self.get_mktime_from_key(key, data_type)
        df_time_dif = df_time.diff(1)
        con_list = df_time_dif > datetime.timedelta(minutes=minutes)
        if True in con_list:
            res = []
            for i in df_time[con_list].index.tolist():
                res.append([df_time[i-1], df_time[i]])
        return res

    def clean_process(self, clean_class_name, s3_class_name):
        clean_class = clean_class_name()
        s3_class = s3_class_name()       
        updating_obj = self.update_obj()
        exchange_list = self.get_dic_keys(updating_obj)
        for exchange in exchange_list:
            self.msg.send(content= '     {}'.format(exchange), is_error = False, chat_con=True)
            data_type_list = self.get_dic_keys(updating_obj[exchange])
            if self.data_type and self.data_type in data_type_list:
                data_type_list = [self.data_type]  
            for data_type in data_type_list:
                self.msg.send(content = '     {}'.format(data_type), is_error = False, chat_con=True)
                date_list = self.get_dic_keys(updating_obj[exchange][data_type])
                for date in date_list:
                    key_list = updating_obj[exchange][data_type][date]
                    try:
                        df_date = self.process_hour_data_to_date_v2(key_list, data_type)
                    except:
                        continue
                    ticker_list, df_list = self.separate_data_by_ticker(df_date)
                    for ticker, df in zip(ticker_list, df_list):
                        if data_type == 'bar':
                            data = clean_class.clean_element(CryptoBarsClean, df)
                        elif data_type == 'snap':
                            data = clean_class.clean_element(CryptoTicksClean, df)
                        elif data_type == 'trade':
                            data = clean_class.clean_element(CryptoTradesClean, df)
                        else:
                            assert False, 'wrong data type :{}'.format(data_type)
                        path = s3_class.normal_save(data)
                        key = '{}/{}/{}/{}/{}.gz'.format(self.SOURCE, exchange, self.MATCH_MAP[data_type], ticker.replace('/','.'), date)
                        s3_class.upload_file(path, s3_class.CLEAN_BUCKET_NAME, key)
                    self.msg.send(content = '     {}  {} finish'.format(date, data_type), is_error = False, chat_con=True)

    def clean_debug(self):
        key_list = ['crypto/binance/snap/2019-11-01/snap-binance-2019-11-01_04.zip']
        key_list = []
        bucket_name = self.RAW_BUCKET_NAME
        for key in key_list:
            self.download_zip_get_df(bucket_name, key)

    def clean_process_test(self):    
        updating_obj = self.existed_obj_raw()
        data_type = 'bar'
        key_list = updating_obj['binance']['bar']['2019-11-24']          
        df_date = self.process_hour_data_to_date_v2(key_list, data_type)
        print(df_date.head())

    def clean_process_quick_test(self, clean_class_name, s3_class_name):
        clean_class = clean_class_name() 
        s3_class = s3_class_name()
        exchange_list = ['binance']
        for exchange in exchange_list:
            self.msg.send(content= '     {}'.format(exchange), is_error = False, chat_con=True)
            data_type_list = ['bar']
            for data_type in data_type_list:
                date_list = ['2019-11-06']
                for date in date_list:
                    self.msg.send(content = '     {}'.format(date), is_error = False, chat_con=True)
                    key_list = ['crypto/binance/bar/2019-11-06/bar-binance-2019-11-06_00.zip', 
                                'crypto/binance/bar/2019-11-06/bar-binance-2019-11-06_01.zip']
                    df_date = self.process_hour_data_to_date_v2(key_list, data_type)
                    ticker_list, df_list = self.separate_data_by_ticker(df_date)
                    for ticker, df in zip(ticker_list[:3], df_list[:3]):
                        if data_type == 'bar':
                            data = clean_class.clean_element(CryptoBarsClean, df)
                        elif data_type == 'snap':
                            data = clean_class.clean_element(CryptoTicksClean, df)
                        elif data_type == 'trade':
                            data = clean_class.clean_element(CryptoTradesClean, df)
                        else:
                            assert False, 'wrong data type :{}'.format(data_type)
                        path = s3_class.normal_save(data)
                        key = '{}/{}/{}/{}/{}.gz'.format(self.SOURCE, exchange, self.MATCH_MAP[data_type], ticker.replace('/','.'), date)
                        s3_class.upload_file(path, s3_class.CLEAN_BUCKET_NAME, key)
                    self.msg.send(content = '     {}  {} finish'.format(date, data_type), is_error = False, chat_con=True)


    
