import os
import stat
import io
import gzip
import shutil
import json
import zipfile
import pandas as pd
import numpy as np
import boto3

class Utility:
    #TODO split to small pieces  i.g.   s3,  zip gzip date

    RAW_BUCKET_NAME = 'll-raw-data'
    CLEAN_BUCKET_NAME = 'll-cleaned-data'
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
    TICK_COLUMNS_STOCK= [
        'open', 'last', 'high', 'low', 'prev_close', 'volume', 'total_turnover',
        'limit_up', 'limit_down', 'a1', 'a2', 'a3', 'a4', 'a5', 'b1', 'b2',
        'b3', 'b4', 'b5', 'a1_v', 'a2_v', 'a3_v', 'a4_v', 'a5_v', 'b1_v',
        'b2_v', 'b3_v', 'b4_v', 'b5_v', 'change_rate'
    ]

    TICK_COLUMNS_FUTURE = [
        'open', 'last', 'high', 'low', 'prev_settlement', 'prev_close',
        'volume', 'open_interest', 'total_turnover', 'limit_up', 'limit_down',
        'a1', 'a2', 'a3', 'a4', 'a5', 'b1', 'b2', 'b3', 'b4', 'b5', 'a1_v',
        'a2_v', 'a3_v', 'a4_v', 'a5_v', 'b1_v', 'b2_v', 'b3_v', 'b4_v', 'b5_v',
        'change_rate'
    ]

    def __init__(self):
        self.s3_client = boto3.client('s3')
        self.s3 = boto3.resource('s3')

    def init_folder(self, folder_name):
        path = 'data/{}'.format(folder_name)
        if not os.path.exists(path):
            os.makedirs(path)
        return path

    def init_folder_data(self, folder_name):
        path = '/data/{}'.format(folder_name)
        os.chmod('/data', stat.S_IRWXU)
        if not os.path.exists(path):    
            os.makedirs(path)
        return path

    def date_modify(self, date):
        if len(date) == 8:
            date = date[:4]+'-'+date[4:6]+'-'+date[6:8]
        elif len(date) == 10:
            pass
        else:
            assert False, "input date : {} not good, input date as 20190101 or 2019-01-01".format(date)
        return date

    def s3_init(self, bucket_name):
        return self.s3.Bucket(name = bucket_name)

    def s3_obj_exist(self, bucket, key):
        res = bucket.objects.filter(Prefix=key)  
        for obj in res:
            if obj.key == key:
                print('obj: {} exist in bucket {}'.format(key, bucket.name))
                return True
        return False

    def put_object_s3(self, bucket, acl, body, key):
        bucket.put_object(
                ACL     = acl,    
                Body    = body,
                Key     = key,
            )

    def normal_save(self, data):
        path = self.init_folder('last')
        path_npy = path + '/tmp.npy'
        path_gzp = path + '/tmp.gz'
        np.save(path_npy, data)
        with open(path_npy, 'rb') as f_in:
            with gzip.open(path_gzp, 'wb') as f_out:
                shutil.copyfileobj(f_in, f_out)
        return path_gzp

    def gz_json(self, data):
        path = self.init_folder('last')
        path_json = path + '/tmp.json'
        path_gzp = path + '/tmp.gz'
        with open(path_json,'w') as file:
            file.write(json.dumps(data))
        with open(path_json, 'rb') as f_in:
            with gzip.open(path_gzp, 'wb') as f_out:
                shutil.copyfileobj(f_in, f_out)
        return path_gzp


    def upload_file(self, path, bucket_name, key):
        self.s3.meta.client.upload_file(path, bucket_name, key)



    def listdir(self, paths, list_name):  
        for file_i in os.listdir(paths):  
            file_path = os.path.join(paths, file_i)  
            if os.path.isdir(file_path):  
                self.listdir(file_path, list_name)  
            else:  
                list_name.append(file_path)  

    def s3_deploy(self, source, destinationBucket, destinationKeyPrefix):
        list_name = []
        self.listdir(source, list_name) 
        for file_i in list_name:
            key = destinationKeyPrefix + file_i.replace(source, '')
            self.upload_file(file_i, destinationBucket, key)

    def zip(self, start_dir):
        start_dir = start_dir 
        file_news = start_dir + '.zip'  
        z = zipfile.ZipFile(file_news, 'w', zipfile.ZIP_DEFLATED)
        for dir_path, dir_names, file_names in os.walk(start_dir):
            f_path = dir_path.replace(start_dir, '')  
            f_path = f_path and f_path + os.sep or ''  
            for filename in file_names:
                z.write(os.path.join(dir_path, filename), f_path + filename)
        z.close()
        return file_news    

    def fancy_load(self, bucket_name, key):
        retr = self.s3.get_object(Bucket=bucket_name, Key=key)
        bytestream = io.BytesIO(retr['Body'].read())
        data = gzip.GzipFile(None, 'rb', fileobj=bytestream)       
        data = np.load(data, allow_pickle=True)
        print(data)

    def save_clean(self, data):
        path = self.init_folder('clean')
        np.save(path+'/temp.npy', data)
        
    def load_raw(self, bucket_name, key):
        obj = self.s3.Object(bucket_name, key)
        body = obj.get()['Body'].read()
        data = gzip.decompress(body).decode('utf-8')
        if 'btcta' in key:
            data = json.loads(data)
            if 'depth' in key:
                res = []
                for data_i in data:
                    dic = {}
                    dic['timestamp'] = data_i['timestamp']
                    for price in ['asks','bids']:
                        for i, price_i in enumerate(data_i[price]):
                            dic['{}_{}_p'.format(price[:3],i+1)] = price_i[0]
                            dic['{}_{}_v'.format(price[:3],i+1)] = price_i[1]
                    res.append(dic)
                data = pd.DataFrame(res)
            else:
                data = pd.DataFrame(data)
        elif '1token' in key and 'trades' in key:
            columns = ['exchange_time', 'contract', 'price', 'bs', 'amount', 'exchange_timestamp', 'time', 'timestamp']
            data = io.StringIO(data)
            data = pd.read_csv(data, names = columns)
        
        else:
            try:
                data = io.StringIO(data)
                data = pd.read_csv(data)
            except:
                data = None
        return data
        
    def data_compress(self, data):
        return gzip.compress(data)

    def make_key(self, source, exchange, method, ticker, date):
        key = '{}/{}/{}/{}/{}.gz'.format(source, exchange, method, ticker, date)
        return key

    def save_data(self, df, folder, ticker):
        if ticker[0] == 'I':
            column = self.TICK_COLUMNS_FUTURE
        else:
            column = self.TICK_COLUMNS_STOCK
        df['time'] = np.array(df.index.to_pydatetime(), dtype = 'datetime64[ms]')
        data_type = [(col_i,'f4') for col_i in column]
        data_type.append(('time','datetime64[ms]'))
        df = [tuple(x) for x in df.values]
        df = np.array(df,dtype = data_type) 
        np.savez_compressed(os.path.join(folder, '{}.npz'.format(ticker)), df)

    def load_data(self, folder, ticker):
        # may learn to cache data here!
        if ticker[0] == 'I':
            column = self.TICK_COLUMNS_FUTURE
        else:
            column = self.TICK_COLUMNS_STOCK
        
        if not self.has_data(folder, ticker):
            return None
        value = np.load(os.path.join(folder, '{}.npy'.format(ticker)),allow_pickle = True)
        columns_tmp = column
        columns_tmp.append('time')
        df = pd.DataFrame(data = value, columns = columns_tmp)
        df.index = df['time']
        df.drop('time',axis = 1, inplace = True)
        return df
        

    def has_data(self, folder, ticker):
        return os.path.isfile('{}/{}.npy'.format(folder, ticker))

    def load_meta_data(self, path):
        json_file = path + '/.meta_data.json'
        with open(json_file,'r') as load_f:
            load_dict = json.load(load_f)
        return load_dict

    def write_json(self, path, data, js_name):
        json_file = os.path.join(path, js_name)
        with open(json_file,'w') as fout:
            fout.write(json.dumps(data))

class DownloadBasic(Utility):
    
    RAW_BUCKET_NAME = 'll-raw-data'

    def __init__(self, start_date=None, end_date=None, ticker_list=None, msg=None):
        self.start_date = start_date
        self.end_date = end_date
        self.ticker_list = ticker_list
        self.msg = msg
        if (start_date and end_date):
            self.data_list = list(pd.date_range(self.start_date, self.end_date))
        Utility.__init__(self)
        
    def download_result_dict(self):
        data_result = {
            'exist'     : [],
            'fail'      : [],
            'success'   : [],
        }
        return data_result
        
 
        