import io
import os
import gzip
import numpy as np
import pandas as pd
import boto3
import json
from .clean_base import CleanBase

class Load:
    
    RAW_BUCKET_NAME = 'll-raw-data'
    CLEANED_BUCKET_NAME = 'll-cleaned-data'
    DAILY_DATA_PREFIX = 'rqdata/daily/'
    BITE_FILE_SIZE = 70 # backtest load data file size 70M npy 
    DEFALUT_FOLDER = './backtest_data'

    def __init__(self,begin_date=None,end_date=None,ticker=None,exchange=None,data_type=None,source=None,daily_or_monthly=None,folder_name=None,asset_type=None,daily_stock=None):
        self.s3_client = boto3.Session(profile_name='default').client('s3')
        self.s3_resource = boto3.resource('s3')
        self.begin_date = begin_date
        self.end_date = end_date
        self.ticker = ticker
        self.exchange = exchange
        self.data_type = data_type
        self.source = source
        self.daily_or_monthly = daily_or_monthly
        self.folder_name = folder_name
        self.asset_type = asset_type
        self.daily_stock =  daily_stock
        self.clean_bucket_name =  self.CLEANED_BUCKET_NAME
        self.clean_base_class = CleanBase()
        self.bite_file_size = self.BITE_FILE_SIZE
        if not os.path.exists(self.DEFALUT_FOLDER):
            os.makedirs(self.DEFALUT_FOLDER)

    def save_meta_info(self):
        # append meta info if exited
        fsize = os.path.getsize(self.meta_path)
        fsize = int(fsize/float(1000*1000))# equal with the size of file in mac
        data_bite = round(self.bite_file_size/fsize*len(self.ticker_time_list),1)
        if self.daily_or_monthly == 'daily':
            data_bite = min(1, data_bite)
        ticker_info = {
            'data_bite' :  data_bite,
            'data_list' : [i.replace('-','') for i in self.whole_time_list],
        }
        meta_path_js = self.folder_name + '/.meta_data.json' 
        try: 
            with open(meta_path_js,'r') as load_f:
                meta_info = json.load(load_f)
        except:
            meta_info = {}
        meta_info[self.ticker_i] = ticker_info
        with open(self.meta_path,'w') as file:
            file.write(json.dumps(meta_info))

    def load_tick(self):
        for date in self.ticker_time_list:
            print(date)
            key = '{}/{}/{}/{}/{}.gz'.format(self.source, self.exchange_i, self.data_type, self.ticker_i, date)
            retr = self.s3_client.get_object(Bucket=self.clean_bucket_name, Key=key)
            bytestream = io.BytesIO(retr['Body'].read())
            data = gzip.GzipFile(None, 'rb', fileobj=bytestream)       
            data = np.load(data, allow_pickle=True)
            if self.ticker_time_list.index(date) == 0:
                res = data
            else:
                res = np.concatenate((res, data))
            if self.daily_or_monthly == 'daily':
                break
        file_path = '{}/{}.npy'.format(self.path_i, self.ticker_i)
        np.save(file_path, res)
        print(file_path,'  finish')
        self.meta_path =  file_path

    def load_group(self):    
        print('daily_or_monthly :', self.daily_or_monthly)
        for input_i in self.download_inputs:
            print('##### {} start #####'.format(input_i))
            start_date, end_date, self.ticker_i, self.exchange_i =  self.clean_base_class.seperate_input(input_i, self.source)
            self.whole_time_list = [i.strftime("%Y-%m-%d") for i in list(pd.date_range(start_date, end_date))]    
            self.date_list = self.whole_time_list
            if self.daily_or_monthly == 'monthly':
                self.whole_time_list = sorted(list(set([i[:7] for i in self.whole_time_list])))
            for time_i in self.whole_time_list:
                self.path_i = '{}'.format(self.folder_name+'/'+time_i.replace('-',''))
                if not os.path.exists(self.path_i):
                    os.makedirs(self.path_i)
                if self.daily_or_monthly == 'monthly':
                    self.ticker_time_list = [i for i in self.date_list if i[:7] == time_i]
                elif self.daily_or_monthly == 'daily':
                    self.ticker_time_list = [time_i]
                self.load_tick()
                if self.whole_time_list.index(time_i) == 0:
                    self.save_meta_info()

    def load_clean_from_s3(self):
        if self.ticker is isinstance(str):
            self.download_inputs = [(self.begin_date, self.end_date, self.ticker)]
        elif self.ticker is isinstance(list):
            self.download_input = [(self.begin_date, self.end_date, i) for i in self.ticker]        
        else:
            print('ticker type not valid, plz input others')
        self.load_group()

    def load_daily_backtest_data(self):
        for data_i in self.daily_stock:
            if data_i.split('/')[0] == 'stock_pool':
                data_folder = os.path.join(self.DEFALUT_FOLDER, data_i.split('/')[0])
            else:
                data_folder = os.path.join(self.DEFALUT_FOLDER, data_i)
            if not os.path.exists(data_folder):
                os.makedirs(data_folder)
        for data_i in self.daily_stock:
            if data_i.split('/')[0] == 'stock_pool':
                data_folder = os.path.join(self.DEFALUT_FOLDER, data_i.split('/')[0])
            else:
                data_folder = os.path.join(self.DEFALUT_FOLDER, data_i)
            prefix_i = self.DAILY_DATA_PREFIX + data_i
            key_list = self.s3_client.list_objects_v2(Bucket = self.RAW_BUCKET_NAME, Prefix = prefix_i)['Contents']
            for key_i in key_list:
                file_name = os.path.join(self.DEFALUT_FOLDER, key_i['Key'].replace(self.DAILY_DATA_PREFIX, ''))
                self.s3_resource.meta.client.download_file(self.RAW_BUCKET_NAME, key_i['Key'], file_name)
            print(f'finish load {data_i}')


