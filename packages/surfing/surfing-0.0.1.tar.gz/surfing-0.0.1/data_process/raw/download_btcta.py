import io
import pandas as pd
from urllib.request import urlopen, Request
import json
import urllib.request
import urllib.error
from datetime import timedelta
from .download_base import Utility
import boto3 

class download_btcta(Utility):
    
    HEADERS = { 'User-Agent'   : "btcta agent",
                'Content-Type' : 'application/json; charset=utf-8' }
    TYPES = {'SpotCandle','SpotTicker','SpotTrade','SpotDepth','FuturesCandle','FuturesTicker','FuturesTrade','FuturesDepth'}
    TIME_SPAN = 10
    TIMEOUT= 60
    RAW_BUCKET_NAME = 'll-raw-data'
    SOURCE = 'btcta'
    EXCHANGE_MAP = {
        'OKEX'      :   'okex',
        'Binance'   :   'bina',
        'ZB.COM'    :   'zb',
        'Bibox'     :   'bibo',
        'Bithumb'   :   'bith',
        'Poloniex'  :   'polo',
        'Huobi'     :   'hbg',
        'BitMEX'    :   'bitm',
        'Hitbtc'    :   'hitb',
        'Bitfinex'  :   'bitf',
        'Gate.io'   :   'gate',
        'Deribit'   :   'deri',
    }

    def __init__(self,exchange=None,coin=None,begin_date=None,end_date=None,asset_type=None,data_type=None,msg=None):
        self.begin_date = begin_date
        self.end_date = end_date
        self.date_list = list(pd.date_range(self.begin_date, self.end_date))
        self.api_key = self.get_btcta_key()
        self.exchange = exchange
        self.coin = coin
        self.asset_type = asset_type
        self.data_type = data_type
        self.asset = asset_type.capitalize()+data_type.capitalize()
        self.url = 'http://117.175.169.121:8088/api/fetch/{}'.format(self.asset)
        self.msg = msg
        Utility.__init__(self)
        
    def get_btcta_key(self):
        bucket_name = 'surfboard'
        key = 'data/btcta.json'
        s3 = boto3.client('s3')
        retr = s3.get_object(Bucket = bucket_name, Key = key)
        bytestream = io.BytesIO(retr['Body'].read())
        surfboard_json = json.load(bytestream)
        return surfboard_json['key']

    def get_request(self, begin_date, end_date):
        dic = { 'apiKey'   :   self.api_key,
                'exchange' :   self.exchange,
                'coin'     :   self.coin,
                'beginDate':   begin_date,
                'endDate'  :   end_date}
        return  json.dumps(dic).encode('utf-8')

    def download_element(self, request_json_string):
        try:
            req = Request(self.url, request_json_string, self.HEADERS)
            response = urlopen(req, timeout=self.TIMEOUT)
            json_response_str = response.read().decode('utf-8')
            json_data =  json.loads(json_response_str)    
            return json_data

        except urllib.error.HTTPError as httpErr:
            self.msg.send(content = 'HTTPError. code:{0} {1})'.format(httpErr.code, httpErr.reason) ,is_error = True, chat_con=True)
        except ValueError as jsonErr:
            self.msg.send(content = 'jsonErr. {0})'.format(jsonErr), is_error = True, chat_con=True)
        except Exception as ex:
            self.msg.send(content = 'Exception. {0}'.format(ex), is_error = True, chat_con=True)
        return

    def get_split_dates(self, str_begin_date):
        dt_begin = str_begin_date
        dt_end   = dt_begin + timedelta(days=1)

        dt_current = dt_begin
        seconds_delta = timedelta(seconds=self.TIME_SPAN*60)
        time_diff = timedelta(milliseconds=0.001)
        result = []
        while True:
            dt_current += seconds_delta
            if dt_current < dt_end:
                result.append({ "start": dt_begin.strftime('%Y-%m-%d %H:%M:%S.%f'), 
                                "end":dt_current.strftime('%Y-%m-%d %H:%M:%S.%f')})
                dt_begin = dt_current
                dt_begin += time_diff
            else:
                result.append({ "start": dt_begin.strftime('%Y-%m-%d %H:%M:%S.%f'), 
                                "end":dt_end.strftime('%Y-%m-%d %H:%M:%S.%f')})
                break
        return result

    def test_network(self):
        self.msg.send(content = '######start download######', is_error = False, chat_con=True)
        request_data = {"apiKey":self.api_key,
                        "exchange": "okex",
                        "coin": "BTC-USDT",
                        "beginDate": "2019-05-16 12:20:00",
                        "endDate": "2019-05-16 12:30:59"
                    }
        request_json_string = json.dumps(request_data).encode('utf-8')
        url = "http://117.175.169.121:8088/api/fetch/SpotCandle"
        req = Request(url, request_json_string, self.HEADERS)
        try:
            response = urlopen(req, timeout=10)
        except Exception as e:
            content = 'Exception: {}\
                       \nbtcta network not good'.format(e)
            self.msg.send(content = content, is_error = True, chat_con=True)
            raise SystemExit

        json_response_str = response.read().decode('utf-8')
        json_data =  json.loads(json_response_str)
        df = pd.DataFrame(json_data['data'])
        if df.shape == (11,6):
            self.msg.send(content = 'btcta network good', is_error = False, chat_con=True)
        else:
            self.msg.send(content = 'btcta network not good ', is_error = True, chat_con=True)
            raise SystemExit

    def download(self):
        for date in self.date_list:
            list_date = self.get_split_dates(date)
            res = []
            for date_item in list_date:
                request_json_string = self.get_request(date_item['start'], date_item['end'])
                data = self.download_element(request_json_string)['data']
                if data:
                    res.extend(data)
            self.msg.send(content='download {}:{}'.format(self.coin, date), is_error = False, chat_con=True)
            key = '{}/{}/{}/{}/{}.gz'.format(self.SOURCE,self.exchange,self.METHOD_MAP[self.data_type],self.coin,date.strftime('%Y-%m-%d'))
            path = self.gz_json(res)
            self.upload_file(path,self.RAW_BUCKET_NAME,key)
            self.msg.send(content = 'key {} finish upload'.format(key), is_error = False, chat_con=True)
        self.msg.send(content = '######finish download######', is_error = False, chat_con=True)    