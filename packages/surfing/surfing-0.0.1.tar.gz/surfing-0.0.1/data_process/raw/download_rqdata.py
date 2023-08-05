import os
import shutil
import json
import datetime
import rqdatac as rq
from .download_base import DownloadBasic


class DownloadRqdata(DownloadBasic):
    
    def __init__(self,months=None,msg=None):
        rq.init()
        self.months = months
        self.fold_path = self.init_folder_data('rqdata')
        self.finish_percent = 0
        self.source = 'rqdata'
        DownloadBasic.__init__(self,msg=msg)

    def prep_dir(self, path):
        if not os.path.exists(path):
            os.makedirs(path) 

    def meta_data_update(self, stocks,futures,path):
        json_file = path + '/.meta_data.json'
        data = {
            'update_time'   :   str(datetime.datetime.now().strftime('%Y%m%d-%H:%M:%S')),
            'stocks_info'   :   list(stocks.order_book_id.values),
            'futures_info'  :   list(futures.order_book_id.values),
        }        
        with open(json_file, 'w') as fout:
            fout.write(json.dumps(data))

    def last_day_of_month(self, any_day):
        if isinstance(any_day, str):
            if len(any_day) == 6:
                any_day = datetime.datetime.strptime(any_day, '%Y%m')
            elif len(any_day) == 8:
                any_day = datetime.datetime.strptime(any_day, '%Y%m%d')
            else:
                return NotImplementedError
        next_month = any_day.replace(day=28) + datetime.timedelta(days=4)  # this will never fail
        final = next_month - datetime.timedelta(days=next_month.day)
        return final.strftime('%Y%m%d')

    def download_element(self, month_i):
        content = '=== {} ==='.format(month_i)
        self.msg.send(content=content,is_error=False,chat_con=True)
        start_date = month_i + '01'
        end_date = self.last_day_of_month(month_i)
        cur_folder = self.fold_path + '/' + month_i
        self.prep_dir(cur_folder)

        insts = rq.all_instruments(date=end_date)
        stocks = insts[insts.type=='CS']

        futures = insts[insts.apply(lambda x:x.order_book_id[:2] in ['IC', 'IF'], axis=1)]   
        self.meta_data_update(stocks,futures,cur_folder)
        parse_insts = stocks.append(futures)
        parse_insts = parse_insts.reset_index(drop=True)
        content = ' download {} instruments...'.format(len(parse_insts))
        self.msg.send(content=content,is_error=False,chat_con=True)
        df_shape_0 = len(parse_insts) / 100
        for idx, row in parse_insts.iterrows():
            ticker = row.order_book_id
            if self.has_data(cur_folder, ticker):
                content = '  skip by existed {} {} '.format(ticker, month_i)
                self.msg.send(content=content,is_error=False,chat_con=False)
            else:
                ticks = rq.get_price(ticker, 
                                    start_date=start_date, 
                                    end_date=end_date, 
                                    frequency='tick',
                                    adjust_type='pre')
                if ticks is None:
                    content = ' skip by None --- {} on {}'.format(ticker, month_i)
                    self.msg.send(content=content,is_error=False,chat_con=False)
                else:
                    df = ticks.drop('trading_date', axis=1)
                    self.save_data(df, cur_folder, ticker)
            if int((idx+1) / df_shape_0) > (self.finish_percent+10):
                self.finish_percent += 10
                content = f"finish percent {self.finish_percent} % "
                self.msg.send(content=content,is_error=False,chat_con=True)
        content = f' finish download : {month_i}'
        self.msg.send(content=content,is_error=False,chat_con=True)
        zip_file_name = self.zip(cur_folder)
        year = month_i[:4]
        key = f'{self.source}/ticks/{year}/{month_i}.zip'
        self.upload_file(   path        = zip_file_name,
                            bucket_name = self.RAW_BUCKET_NAME,
                            key         = key)
        content = f'upload file with key : {key}'
        self.msg.send(content=content,is_error=False,chat_con=True)
        os.remove(zip_file_name)
        shutil.rmtree(cur_folder)
        content = f'remove local data : {month_i}'
        self.msg.send(content=content,is_error=False,chat_con=True)

    def download_months(self):
        content = f"download list: {self.months}"
        self.msg.send(content=content,is_error=False,chat_con=True)
        for month_i in self.months:
            if len(month_i) == 4:
                for i in range(12):
                    month_j = month_i+str(i+1).zfill(2)
                    self.download_element(month_j)
            else:
                self.download_element(month_i)