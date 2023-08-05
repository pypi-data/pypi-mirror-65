import io
import json
import requests
from .download_base import DownloadBasic
import boto3

class Download1Token(DownloadBasic):
    
    ONE_TOKEN_URL = 'https://hist-quote.1tokentrade.cn'
    SOURCE = '1token'

    # test
    def __init__(self,start_date=None,end_date=None,ticker_list=None,msg=None):
        self.headers = {"ot-key": self.get_otkey()}
        DownloadBasic.__init__(self,start_date=start_date,end_date=end_date,ticker_list=ticker_list,msg=msg)

    def url_contract_list(self, date):
        return self.ONE_TOKEN_URL + '/ticks/contracts?date={}'.format(date)

    def url_method(self, method, date, ticker):
        if method == 'ticks':
            return self.ONE_TOKEN_URL + '/ticks/full?date={}&contract={}'.format(date, ticker)
        
        elif method == 'trades':
            return self.ONE_TOKEN_URL + '/trades/?date={}&contract={}'.format(date, ticker)

    def get_otkey(self):
        bucket_name = 'surfboard'
        key = 'data/oneToken.json'
        s3 = boto3.client('s3')
        retr = s3.get_object(Bucket = bucket_name, Key = key)
        bytestream = io.BytesIO(retr['Body'].read())
        data_json = json.load(bytestream)
        return data_json['key']

    def download_url(self, url, headers = None):
        response = requests.get(url, headers= headers)
        if response.status_code == 200:
            data = response.content
            if 'ot-quota-remaining' in list(response.headers.keys()):
                ot_quota_remain = response.headers['ot-quota-remaining']
            else:
                ot_quota_remain = 'not provided'
            return True, data, ot_quota_remain
        else:
            return False, [], ''

    def download_contract_list(self, date):
         # contract info dont need ot-key  free! 
         # limit:  10 request per second 
        date = self.date_modify(date)
        url = self.url_contract_list(date)
        data = self.download_url(url)[1]
        data = str(data, encoding = "utf-8")
        data = data[2:-2].split('", "')
        return data

    def check_method_ticker(self, method):
        content = '##########start download###########\nstart download with data type : {}'.format(method)
        self.msg.send(content=content,is_error=False,chat_con=True)
        if not method in ['ticks', 'trades']:
            self.msg.send(content='choose method in ticks or trades',is_error=True,chat_con=True)
            raise SystemExit
        contract_list = self.download_contract_list(self.start_date)
        for ticker in self.ticker_list:
            if not ticker in contract_list:
                content = 'contract downloaded: {} not exist, pls choose others'.format(ticker)
                self.msg.send(content=content,is_error=True,chat_con=True)
        ticker_list = [i for i in self.ticker_list if i in contract_list]
        return ticker_list

    def process_data(self, method):
        # pipeline for processing ticks and trades data
        ticker_list = self.check_method_ticker(method)
        bucket = self.s3_init(DownloadBasic.RAW_BUCKET_NAME)
        data_result = self.download_result_dict()
        for ticker in ticker_list:
            for date in self.data_list:
                date = date.strftime("%Y-%m-%d")
                exchange = ticker.split('/')[0]
                ticker_modi = ticker.split('/')[1]
                key = self.make_key(self.SOURCE, exchange, method, ticker_modi, date)
                result_i = date+' '+ticker
                if self.s3_obj_exist(bucket, key):
                    data_result['exist'].append(result_i)
                    continue
                url = self.url_method(method, date, ticker)
                status, data, ot_quota_remain = self.download_url(url, self.headers)
                if not status:
                    content = 'Download failed {} {}'.format(date, ticker)
                    self.msg.send(content=content,is_error=True,chat_con=True)
                    data_result['fail'].append(result_i)
                    continue
                
                self.put_object_s3(bucket, 'private', data, key)
                content = '{} {} success\n ot quota remain: {}'.format(date, ticker, ot_quota_remain)
                self.msg.send(content=content,is_error=False,chat_con=True)
                data_result['success'].append(result_i)
        
        content = 'finish \n {} \n#########finish download############'.format(data_result)
        self.msg.send(content=content,is_error=False,chat_con=True)
        