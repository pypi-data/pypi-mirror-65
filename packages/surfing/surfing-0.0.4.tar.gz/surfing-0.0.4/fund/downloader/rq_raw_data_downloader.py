#!/usr/bin/env python
# coding: utf-8
import numpy as np
import pandas as pd
import rqdatac as rq
import datetime
import json
from ..db.database import RawDatabaseConnector
from ..db.raw_models import *
from ..util.constant import STOCK_VALUATION_FACTORS, FUND_INDICATORS
from ..data_api.basic_new import BasicDataApi

class RqRawDataDownloader(object):
    def __init__(self, rq_license):
        # Initialize RiceQuant API
        rq.init('license', rq_license, ('rqdatad-pro.ricequant.com', 16011))

        # Get all fund order_book_ids 
        self._fund_order_book_id_list = list(set(rq.fund.all_instruments()['order_book_id'].tolist()))

        # Get stock order_book_ids
        self._stock_order_book_id_list = rq.all_instruments(type='CS', market='cn')['order_book_id'].tolist()

        # Get index list
        index_df = BasicDataApi().get_index_info()
        self._index_list = [order_book_id for order_book_id in index_df['order_book_id'].tolist() 
            if '.' in order_book_id and order_book_id != 'not_available']
        self._future_list = [order_book_id for order_book_id in index_df['order_book_id'].tolist() 
            if '.' not in order_book_id and order_book_id != 'not_available']
        self._order_book_id_2_index_id = {order_book_id : index_id for order_book_id, index_id in 
            zip(index_df['order_book_id'], index_df['index_id']) if order_book_id != 'not_available'}

    def _upload_raw(self, df, table_name, if_exists='append'):
        print(table_name)
        # print(df)
        df.to_sql(table_name, RawDatabaseConnector().get_engine(), index=False, if_exists=if_exists)

    def _get_date_list(self, start_date, end_date):
        start_datetime = datetime.datetime.strptime(start_date, '%Y%m%d')
        end_datetime = datetime.datetime.strptime(end_date, '%Y%m%d')
        date_list = []
        while start_datetime <= end_datetime:
            date_list.append(start_datetime.strftime('%Y%m%d'))
            start_datetime += datetime.timedelta(days=1)
        return date_list

    def rq_fund_indicator(self, start_date, end_date):
        df = rq.fund.get_indicators(self._fund_order_book_id_list, start_date, end_date, 
            fields=FUND_INDICATORS)

        if df is not None:
            df.reset_index(inplace=True)
            self._upload_raw(df, RqFundIndicator.__table__.name)

    def rq_fund_nav(self, start_date, end_date):
        df_list = []

        count = 0
        for order_book_id in self._fund_order_book_id_list:
            count += 1
            if count % 100 == 0:
                print(f'[{RqFundNav.__table__.name}] downloaded {count} out of '
                    f'{len(self._fund_order_book_id_list)} funds')
            df = rq.fund.get_nav(order_book_id, start_date, end_date, expect_df=True)
            if df is None:
                continue
            df.reset_index(inplace=True)
            df_list.append(df)

        if len(df_list) > 0:
            df_all = pd.concat(df_list)
            self._upload_raw(df_all, RqFundNav.__table__.name)
            
    def rq_fund_size(self):
        instruments = []
        for instrument in rq.fund.instruments(self._fund_order_book_id_list):
            instruments.append({
                'order_book_id' : instrument.order_book_id, 
                'latest_size' : instrument.latest_size
            })
        df = pd.DataFrame(instruments)
        if df is not None:
            df['update_time'] = datetime.date.today()
            self._upload_raw(df, RqFundSize.__table__.name, if_exists='replace')

    def rq_index_price(self, start_date, end_date):
        df = rq.get_price(self._index_list, start_date, end_date, expect_df=True)
        if df is not None:
            df = df.reset_index().drop(['num_trades'], axis = 1)
            df['datetime'] = df['date']
            df = df.drop(['date'], axis = 1)
            self._upload_raw(df, RqIndexPrice.__table__.name)

        df = rq.get_price(self._future_list, start_date, end_date, expect_df=True)
        if df is not None:
            df = df.reset_index().drop(['limit_down', 'prev_settlement', 'limit_up', 'open_interest', 'settlement', 
                'dominant_id'], axis = 1)
            df['datetime'] = df['date']
            df = df.drop(['date'], axis = 1)
            self._upload_raw(df, RqIndexPrice.__table__.name)

    def rq_index_weight(self, start_date, end_date):
        date_list = self._get_date_list(start_date, end_date)
        for i in self._index_list:
            res = []
            for d in date_list:
                try:
                    df = rq.index_weights(i, date=d)
                    if df is not None:
                        dic = df.to_dict()
                        stock_list = [k for k, v in dic.items()]
                        weight_list = [round(v, 6) for k, v in dic.items()]
                        res.append({
                            'index_id': self._order_book_id_2_index_id[i],
                            'datetime': d,
                            'weight_list': json.dumps(weight_list),
                            'stock_list': json.dumps(stock_list),  
                        })
                except:
                    pass
            if len(res) > 0:
                df = pd.DataFrame(res)
                self._upload_raw(df, RqIndexWeight.__table__.name)

    def rq_stock_fin_fac(self, start_date, end_date):
        factor = 'return_on_equity_ttm'
        df = rq.get_factor(self._stock_order_book_id_list, factor=factor, start_date=start_date, end_date=end_date)
        to_convert_series = type(df) is pd.core.series.Series
        if to_convert_series:
            df = df.to_frame()
        df = df.stack().reset_index()
        df.columns = ['stock_id', 'datetime', factor] if to_convert_series else ['datetime', 'stock_id', factor]
        self._upload_raw(df, RqStockFinFac.__table__.name)

    def rq_stock_post_price(self, start_date, end_date):
        df = rq.get_price(self._stock_order_book_id_list, start_date=start_date, end_date=end_date, 
            adjust_type='post', expect_df=True)
        if df is not None:
            df = df.reset_index().rename(columns={'date': 'datetime'})
            self._upload_raw(df, RqStockPostPrice.__table__.name)

    def rq_stock_price(self, start_date, end_date):
        df = rq.get_price(self._stock_order_book_id_list, start_date=start_date, end_date=end_date, 
            adjust_type='none', expect_df=True)
        if df is not None:
            df = df.reset_index().rename(columns={'date': 'datetime'})
            self._upload_raw(df, RqStockPrice.__table__.name)

    def rq_stock_valuation(self, start_date, end_date):
        df = rq.get_factor(self._stock_order_book_id_list, STOCK_VALUATION_FACTORS, start_date=start_date, 
            end_date=end_date, expect_df=True)
        if df is not None:
            df = df.reset_index().rename(columns={'order_book_id': 'stock_id', 'date':'datetime'}).replace(
                [np.inf, -np.inf], np.nan)
            self._upload_raw(df, RqStockValuation.__table__.name)

    def trading_day_list(self, start_date, end_date):
        df = pd.DataFrame(rq.get_trading_dates(start_date=start_date, end_date=end_date, market='cn'), 
            columns=['datetime'])
        if df is not None:
            self._upload_raw(df, TradingDayList.__table__.name)

    def stock_info(self):
        order_book_ids = []
        for stock_order_book_id in self._stock_order_book_id_list:
            order_book_ids.append({
                'rq_id' : stock_order_book_id, 
                'stock_id' : stock_order_book_id
            })
        df = pd.DataFrame(order_book_ids)
        if df is not None:
            self._upload_raw(df, StockInfo.__table__.name, if_exists='replace')

    def fund_rating(self, start_date, end_date):
        try:
            df = rq.fund.get_ratings(self._fund_order_book_id_list)
            if df is not None:
                df.reset_index(inplace=True)
                df = df[(df['datetime'] >= start_date) & (df['datetime'] <= end_date)]
                self._upload_raw(df, FundRating.__table__.name)
        except Exception as e:
            print(e)

    def download_all(self, start_date, end_date):
        self.rq_fund_indicator(start_date, end_date)
        self.rq_fund_nav(start_date, end_date)
        self.rq_index_price(start_date, end_date)
        self.rq_index_weight(start_date, end_date)
        self.rq_stock_fin_fac(start_date, end_date)
        self.rq_stock_post_price(start_date, end_date)
        self.rq_stock_price(start_date, end_date)
        self.rq_stock_valuation(start_date, end_date)
        self.trading_day_list(start_date, end_date)
        self.fund_rating(start_date, end_date)
        self.stock_info()
        self.rq_fund_size()
