import os
import json
import datetime
import numpy as np
import rqdatac as rq
from .download_base import DownloadBasic


class DownloadRqdataDaily(DownloadBasic):

    STOCK_POOL = {
        '000001.XSHG'   :   '上证指数',
        '000002.XSHG'   :   'A股指数',
        '000016.XSHG'   :   '上证50',
        '000300.XSHG'   :   '沪深300',
        '000905.XSHG'   :   '中证500',
        '399001.XSHE'   :   '深证成指',
        '399005.XSHE'   :   '中小板指',
        '399006.XSHE'   :   '创业板',
    }

    def __init__(self,start_date=None,end_date=None,msg=None):
        rq.init()
        #self.fold_path = self.init_folder_data('rqdata')
        DownloadBasic.__init__(self,start_date=start_date,end_date=end_date,msg=msg)
        self.fold_path_data = self.init_folder('rqdata_daily')
        self.fold_path_factor = self.init_folder('rqdata_factor')
        self.stocks = sorted(self.get_stocks())       
        self.source = 'rqdata'
        self.s3_prefix_price = 'rqdata/daily'
        self.s3_prefix_factor = 'rqdata/daily/factor_example'
        
    def get_trading_dates(self):
        return rq.get_trading_dates(self.start_date, self.end_date)
    
    def get_stocks(self):
        return rq.all_instruments(type = 'CS', market = 'cn', date = self.end_date).order_book_id.values    

    def init_path_folder(self, default_path, data_name):
        path = os.path.join(default_path, data_name)
        if not os.path.exists(path):
            os.makedirs(path)
        return path

    def df_columns_sorted(self, df):
        df_columns = sorted(list(df.columns.values))
        df = df[df_columns].copy()
        return df

    def meta_data_update(self, dates, tickers, column_path):
        json_file = os.path.join(column_path, '.meta_data.json')
        data = {
            'update_time'   :   str(datetime.datetime.now().strftime('%Y%m%d-%H:%M:%S')),
            'dates'         :   [date.strftime('%Y-%m-%d') for date in dates],
            'tickers'       :   list(tickers),
        }
        with open(json_file, 'w') as fout:
            fout.write(json.dumps(data))    

    def process_df(self, df, column_i, column_path):
        stocks_columns = sorted(list(df.columns.values))
        df = df[stocks_columns].copy()
        data_type = [(i, 'f4') for i in df.columns]
        df['time'] = np.array(df.index.to_pydatetime(), dtype = 'datetime64[ms]')
        dates = df.index.to_pydatetime()
        data_type.append(('time','datetime64[ms]'))
        df = [tuple(x) for x in df.values]
        df = np.array(df,dtype = data_type)
        if not os.path.exists(column_path): 
            os.makedirs(column_path)
        npy_file = os.path.join(column_path, '{}.npz'.format(column_i))
        np.savez_compressed(npy_file, df)
        self.meta_data_update(dates, stocks_columns, column_path)
        print(f'    update {column_i} finish')

    def update_stock_pool(self):
        print('update stock pool')
        index_list = list(self.STOCK_POOL.keys())
        for index_i in index_list:
            try:
                index_i_folder = self.init_path_folder(self.fold_path_data, 'stock_pool')
                data = rq.index_components( order_book_id = index_i, 
                                            start_date = self.start_date, 
                                            end_date = self.end_date)
                
                dic = {}
                for key in data.keys():
                    dic[key.strftime('%Y-%m-%d')] = data[key]
                    self.write_json(index_i_folder, dic, '{}.json'.format(index_i))
                print('    update', index_i,' success')
            except:
                print('    update', index_i, 'failed')

    def update_limit_up_limit_down(self):
        print('update limit up limit down')
        df_change = rq.get_price_change_rate(   order_book_ids = self.stocks, start_date = self.start_date, 
                                                end_date = self.end_date, expect_df = True )
        
        folder_path = self.init_path_folder(self.fold_path_data, 'limit')
        dic = {}
        for idx, row in df_change.iterrows():
            dic[idx.strftime('%Y-%m-%d')] = row.index[row.apply(lambda x:x <= -0.099 or x >= 0.099)].tolist()
        self.write_json(folder_path, dic, 'limit.json') 

    def update_suspended(self):
        print('update suspended')
        df_suspended = rq.is_suspended(order_book_ids = self.stocks, start_date= self.start_date, end_date= self.end_date)
        folder_path = self.init_path_folder(self.fold_path_data, 'suspended')  
        dic = {}
        for idx, row in df_suspended.iterrows():
            dic[idx.strftime('%Y-%m-%d')] = row.index[row.values].tolist()
        self.write_json(folder_path, dic, 'suspended.json')

    def update_st(self):
        print('update st')
        df_st = rq.is_st_stock(order_book_ids = self.stocks, start_date= self.start_date, end_date= self.end_date)    
        folder_path = self.init_path_folder(self.fold_path_data, 'st')
        dic = {}
        for idx, row in df_st.iterrows():
            dic[idx.strftime('%Y-%m-%d')] = row.index[row.values].tolist()
        self.write_json(folder_path, dic, 'st.json')

    def update_stock_info(self):
        print('update stock info')
        res_list = rq.instruments(self.stocks)
        folder_path = self.init_path_folder(self.fold_path_data, 'stock_info')
        info_dic = {}
        for info_i in res_list:
            info_dic[info_i.order_book_id] = {
                    'chn_name'              :   info_i.symbol,
                    'industry_code'         :   info_i.industry_code,         #国民经济行业分类代码
                    'sector_code_name'      :   info_i.sector_code_name,      #板块缩写代码,全球通用标准定义
                    'industry_name'         :   info_i.industry_name,         #国民经济行业分类名称
                    'shenwan_industry_code' :   info_i.shenwan_industry_code,
                    'shenwan_industry_name' :   info_i.shenwan_industry_name,
                }
        self.write_json(folder_path, info_dic, 'stock_info.json')

    def update_index_data(self):
        index_pool = list(self.STOCK_POOL.keys())
        start_date = datetime.datetime.strftime(datetime.datetime.strptime(self.start_date, '%Y-%m-%d') - datetime.timedelta(10), '%Y-%m-%d')
        index_close = rq.get_price(order_book_ids=index_pool, start_date=start_date, end_date=self.end_date, frequency='1d')['close']
        column_i = 'index_close'
        column_path = os.path.join(self.fold_path_data, column_i)
        self.process_df(index_close, column_i, column_path)

    def update_data(self):
        start_date = datetime.datetime.strftime(datetime.datetime.strptime(self.start_date, '%Y-%m-%d') - datetime.timedelta(10), '%Y-%m-%d')
        post_price_data = rq.get_price(     order_book_ids  = self.stocks,
                                            start_date      = start_date,
                                            end_date        = self.end_date,
                                            frequency       = '1d',
                                            adjust_type     = 'post'    
                                        )
        
        none_price_data = rq.get_price(     order_book_ids  = self.stocks,
                                            start_date      = start_date,
                                            end_date        = self.end_date,
                                            frequency       = '1d',
                                            adjust_type     = 'none'    
                                        )
        
        # update post data
        print('update post and none data')
        for column_i in sorted(post_price_data):
            df = post_price_data[column_i]
            column_i = 'post_close' if column_i == 'close' else column_i
            column_i = 'post_volume' if column_i == 'volume' else column_i
            column_i = 'post_high' if column_i == 'high' else column_i
            column_i = 'post_low' if column_i == 'low' else column_i
            column_i = 'post_open' if column_i == 'open' else column_i
            
            column_path = os.path.join(self.fold_path_data, column_i)
            self.process_df(df, column_i, column_path)

        # update close volume
        for column_i in ['close', 'volume']:
            df = none_price_data[column_i]
            column_path = os.path.join(self.fold_path_data, column_i)
            self.process_df(df, column_i, column_path)

        # update vwap and post_vwap
        vwap = (none_price_data['total_turnover'] / none_price_data['volume']).fillna(method='ffill')
        cumu_factor = post_price_data['close']/none_price_data['close'] 
        post_vwap = vwap * cumu_factor
        column_i = 'post_vwap'
        column_path = os.path.join(self.fold_path_data, column_i)
        self.process_df(post_vwap, column_i, column_path)
        column_i = 'vwap'
        column_path = os.path.join(self.fold_path_data, column_i)
        self.process_df(vwap, column_i, column_path)

        # update post_preclose
        df = post_price_data['close']
        df_index = df.index[1:]
        post_preclose = df[:-1].copy()         
        post_preclose.index = df_index
        column_i = 'post_preclose'
        column_path = os.path.join(self.fold_path_data, column_i)
        self.process_df(post_preclose, column_i, column_path)

        # update preclose
        df = none_price_data['close']
        df_index = df.index[1:]
        df = df[:-1].copy()         
        df.index = df_index
        column_i = 'preclose'
        column_path = os.path.join(self.fold_path_data, column_i)
        self.process_df(df, column_i, column_path)

        # update post_vwap preclose diff
        post_vwap_preclose_diff = (100 * post_vwap[1:] / post_preclose -100 ).round(2)
        column_i = 'post_vwap_preclose_diff'
        column_path = os.path.join(self.fold_path_data, column_i)
        self.process_df(post_vwap_preclose_diff, column_i, column_path)

        # update example factor oversold_5
        fct_name = 'oversold_5'
        df = post_price_data['close'].rolling(window = 5, min_periods = 0).mean()
        df = 100 * (post_price_data['close'] / df  - 1) * (-1)
        column_path = os.path.join(self.fold_path_factor, fct_name)
        self.process_df(df, fct_name, column_path)

    def data_deploy(self):
        self.s3_deploy(self.fold_path_data, self.RAW_BUCKET_NAME, self.s3_prefix_price )
        self.s3_deploy(self.fold_path_factor, self.RAW_BUCKET_NAME,self.s3_prefix_factor)

    def update(self):
        # update main function
        self.update_index_data()
        self.update_stock_info()
        self.update_stock_pool()
        self.update_limit_up_limit_down()
        self.update_suspended()
        self.update_st()
        self.update_data()
        self.data_deploy()

 