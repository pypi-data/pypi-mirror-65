import pandas as pd
import datetime
from ...db.database import BasicDatabaseConnector
from ...data_api.raw_new import RawDataApi
from ...data_api.basic_new import BasicDataApi
from ...db.basic_models import *

class BasicDataProcessor(object):

    def __init__(self):
        self._index_info_df = BasicDataApi().get_index_info()
        self._fund_info_df = BasicDataApi().get_fund_info()
        # Get the mapping between order_book_id and fund_id (which is defined in this system)
        self._fund_id_mapping = BasicDataApi().get_fund_id_mapping()

    def _upload_basic(self, df, table_name, if_exists='append'):
        print(table_name)
        # print(df)
        df.to_sql(table_name, BasicDatabaseConnector().get_engine(), index=False, if_exists=if_exists)

    def _get_fund_id_from_order_book_id(self, order_book_id, date):
        if order_book_id in self._fund_id_mapping:
            for fund_info in self._fund_id_mapping[order_book_id]:
                if (date >= fund_info['start_date'] and 
                        (fund_info['end_date'] == '00000000' or date <= fund_info['end_date'])):
                    return fund_info['fund_id']
        return None

    def _status_mapping(self, x):
        if x == 'Open':
            return 0
        elif x == 'Suspended':
            return 1
        elif x == 'Limited':
            return 2
        elif x == 'Close':
            return 3
        else:
            return None

    def _find_tag(self, symbol, wind_class_II):
        if '沪深300' in symbol and wind_class_II in ['普通股票型基金', '增强指数型基金', '被动指数型基金']:
            return 'A股大盘'
        elif '中证500' in symbol and wind_class_II in ['普通股票型基金', '增强指数型基金', '被动指数型基金']:
            return 'A股中盘'
        elif '标普500' in symbol:
            return '美股大盘'
        elif '创业板' in symbol and wind_class_II in ['普通股票型基金', '增强指数型基金', '被动指数型基金']:
            return '创业板'
        elif '德国' in symbol:
            return '德国大盘'
        elif '日本' in symbol or '日经' in symbol:
            return '日本大盘'
        elif (('国债' in symbol or '利率' in symbol or '金融债' in symbol)
              and wind_class_II in ['短期纯债型基金', '中长期纯债型基金', '被动指数型债券基金']):
            return '利率债'
        elif (('信用' in symbol or '企债' in symbol or '企业债' in symbol)
              and wind_class_II in ['短期纯债型基金', '中长期纯债型基金', '被动指数型债券基金']):
            return '信用债'
        elif '黄金' in symbol:
            return '黄金'
        elif '原油' in symbol or '石油' in symbol or '油气' in symbol:
            return '原油'
        elif ('地产' in symbol or '金融' in symbol) and ('美国'not in symbol):
            return '房地产'
        else:
            return 'null'

    def fund_info(self):
        # Update manually
        # Not verified
        track_index_df = pd.read_csv('./data/fund_track_index.csv',index_col=0 )
        wind_fund_info = RawDataApi().get_wind_fund_info()
        fund_fee = RawDataApi().get_fund_fee()
        wind_fund_info['order_book_id'] = [_.split('!')[0].split('.')[0] for _ in wind_fund_info['wind_id'] ]
        res = []
        for i in wind_fund_info['wind_id']:
            if not '!' in i:
                res.append(0)
            else:
                res_i = int(i.split('!')[1].split('.')[0])
                res.append(res_i)
        wind_fund_info['transition'] = res
        wind_fund_info['fund_id'] = [o + '!' + str(t) for o, t in zip(wind_fund_info['order_book_id'], wind_fund_info['transition'])]
        wind_fund_info = wind_fund_info.set_index('fund_id')
        fund_fee = fund_fee.drop(['id','desc_name'], axis = 1).set_index('fund_id')
        wind_fund_info = wind_fund_info.join(fund_fee)
        wind_fund_info['fund_id'] = wind_fund_info.index
        wind_fund_info['asset_type'] = [self._find_tag(symbol, wind_class_II) for symbol, wind_class_II in zip(wind_fund_info['desc_name'],wind_fund_info['wind_class_2'])]
        wind_fund_info['update_time'] = datetime.datetime.now()
        wind_fund_info = wind_fund_info.drop(['id'], axis = 1)
        wind_fund_info = wind_fund_info[[i.split('.')[1] == 'OF' for i in wind_fund_info['wind_id']]]
        wind_fund_info = wind_fund_info.set_index('wind_id')
        dic = {k:v for k,v in zip(self._index_info_df['desc_name'], self._index_info_df['index_id'])}
        wind_fund_info = wind_fund_info.join(track_index_df[['track_index']])
        wind_fund_info['wind_id'] = wind_fund_info.index
        wind_fund_info['track_index'] = wind_fund_info['track_index'].map(lambda x: dic.get(x,'none'))
        self._upload_basic(wind_fund_info, FundInfo.__table__.name)

    def index_info(self):
        # Update manually
        # Not verified
        df = pd.read_csv('./data/index_info.csv')
        self._upload_basic(df, IndexInfo.__table__.name)

    def fund_nav(self, start_date, end_date):
        df = RawDataApi().get_fund_nav(start_date, end_date)
        df['fund_id'] = df.apply(
            lambda x: self._get_fund_id_from_order_book_id(x['order_book_id'], x['datetime']), axis=1)
        df['subscribe_status'] = df['subscribe_status'].map(self._status_mapping)
        df['redeem_status'] = df['redeem_status'].map(self._status_mapping)
        df = df[df['fund_id'].notna()]
        self._upload_basic(df, FundNav.__table__.name)

    def index_price(self, start_date, end_date):
        cm_index_price = RawDataApi().get_raw_cm_index_price_df(start_date, end_date)
        cxindex_index_price = RawDataApi().get_cxindex_index_price_df(start_date, end_date)
        yahoo_index_price = RawDataApi().get_yahoo_index_price_df(start_date, end_date)
        rq_index_price = RawDataApi().get_rq_index_price_df(start_date, end_date)

        df_list = []
        index_list = ['sp500', 'dax30', 'n225']
        cm_index_list = ['sp500rmb', 'dax30rmb', 'n225rmb']
        for i, c in zip(index_list, cm_index_list):
            cm_index = yahoo_index_price.copy()
            df = cm_index[cm_index['index_id'] == i]
            df = cm_index_price.set_index('datetime').join(df.set_index('datetime'))
            df = df.fillna(method='ffill')
            df['close'] = df['close'] * df['usd_central_parity_rate']
            df = df[['close']]
            df['datetime'] = df.index
            df['ret'] = df['close'] / df['close'].shift(1) - 1
            df['open'] = float('Nan')
            df['high'] = float('Nan')
            df['low'] = float('Nan')
            df['volume'] = float('Nan')
            df['total_turnover'] = float('Nan')
            df['index_id'] = c
            df_list.append(df.copy())

        index_dic = {k: v for k, v in zip(
            self._index_info_df['order_book_id'], self._index_info_df['index_id']) if k != 'not_available'}
        rq_index_price['index_id'] = rq_index_price['order_book_id'].map(
            lambda x: index_dic[x])
        res = []
        for index_i in list(set(rq_index_price['order_book_id'].tolist())):
            dftmp = rq_index_price[rq_index_price['order_book_id'] == index_i].copy(
            )
            dftmp['ret'] = dftmp['close'] / dftmp['close'].shift(1) - 1
            res.append(dftmp)
        rq_index_price = pd.concat(res)
        df_list.append(yahoo_index_price)
        df_list.append(cxindex_index_price)
        df_list.append(rq_index_price)

        df = pd.concat(df_list).drop(['order_book_id'], axis=1)
        df['datetime'] = pd.to_datetime(df['datetime'])
        df = df.drop(['id'], axis=1)
        self._upload_basic(df, IndexPrice.__table__.name)

    def fund_rating_latest(self):
        fund_rating_df = RawDataApi().get_fund_rating()
        fund_info = self._fund_info_df[['fund_id', 'order_book_id', 'start_date', 'end_date']]
        score_name = ['zs', 'sh3', 'sh5', 'jajx']
        score_dic = {}
        for s in score_name:
            score_df = fund_rating_df[['order_book_id', 'datetime', s]]
            datelist = sorted(list(set(score_df.dropna().datetime.tolist())))
            score_dic[s] = datelist[-1]
        res = []
        for s, d in score_dic.items():
            df = fund_rating_df[['order_book_id', 'datetime', s]]
            df = df[df['datetime'] == d]
            con1 = fund_info['start_date'] <= d
            con2 = fund_info['end_date'] >= d
            fund_info_i = fund_info[con1 & con2]
            dic = {row['order_book_id']: row['fund_id']
                   for index, row in fund_info_i.iterrows()}
            df['fund_id'] = df['order_book_id'].map(lambda x: dic[x])
            df = df[['fund_id', s]].copy().set_index('fund_id')
            res.append(df)
        df = pd.concat(res, axis=1, sort=False)
        df['fund_id'] = df.index
        df['update_time'] = datetime.date.today()
        self._upload_basic(df, FundRatingLatest.__table__.name, 'replace')

    def stock_price(self, start_date, end_date):
        stock_price_df = RawDataApi().get_rq_stock_price(start_date, end_date)
        stock_post_price_df = RawDataApi().get_rq_stock_post_price(start_date, end_date)

        stock_post_price_df['adj_close'] = stock_post_price_df['close']
        stock_post_price_df = stock_post_price_df.filter(items=['adj_close', 'datetime', 'order_book_id'], 
            axis='columns')

        stock_price_merge_df = stock_price_df.merge(stock_post_price_df, how='left', on=['datetime', 'order_book_id'])
        stock_price_merge_df['post_adj_factor'] = stock_price_merge_df['adj_close'] / stock_price_merge_df['close']
        stock_price_merge_df['ret'] = stock_price_merge_df['adj_close'] / stock_price_merge_df['adj_close'].shift(1) - 1
        stock_price_merge_df = stock_price_merge_df.rename(columns={'order_book_id': 'stock_id'}).drop(
            columns=['id'])

        self._upload_basic(stock_price_merge_df, StockPrice.__table__.name)

    def fund_ret(self, start_date, end_date):
        column_rename_dict = {
            'sharp_ratio': 'sharpe_ratio',
            'last_week_return': 'w1_ret',
            'last_month_return': 'm1_ret',
            'last_three_month_return': 'm3_ret',
            'last_six_month_return': 'm6_ret',
            'last_twelve_month_return': 'y1_ret',
            'max_drop_down': 'mdd',
            'annualized_returns': 'annual_ret',
            'average_size': 'avg_size',
            'information_ratio': 'info_ratio',
            'to_date_return':'to_date_ret'
        }
        column_drop_list = ['id', 'order_book_id', 'year_to_date_return', 'annualized_risk']

        df = RawDataApi().get_rq_fund_indicator(start_date, end_date)
        df['fund_id'] = df.apply(
            lambda x: self._get_fund_id_from_order_book_id(x['order_book_id'], x['datetime']), axis=1)
        df = df.rename(columns=column_rename_dict).drop(columns=column_drop_list)

        self._upload_basic(df, FundRet.__table__.name)

    def stock_info(self):
        df = RawDataApi().get_stock_info()
        self._upload_basic(df, StockInfo.__table__.name, 'replace')

    def fund_size(self):
        df = RawDataApi().get_fund_size()
        df['fund_id'] = df.apply(
            lambda x: self._get_fund_id_from_order_book_id(x['order_book_id'], x['update_time']), axis=1)
        df = df.drop(['order_book_id'], axis = 1)
        df = df[df['fund_id'].notnull()]
        self._upload_basic(df, FundSize.__table__.name, 'replace')

    def trading_day_list(self, start_date, end_date):
        df = RawDataApi().get_trading_day_list(start_date, end_date)
        self._upload_basic(df, TradingDayList.__table__.name)
    
    def process_all(self, start_date, end_date):
        self.fund_nav(start_date, end_date)
        self.fund_ret(start_date, end_date)
        self.index_price(start_date, end_date)
        self.stock_price(start_date, end_date)
        self.trading_day_list(start_date, end_date)
        self.stock_info()
        self.fund_size()
        self.fund_rating_latest()
