import numpy as np
import pandas as pd
from .clean_base import CleanBase

class RQdataTicksClean(CleanBase):

    DATA_TYPE  = [
        ('ask_price_1',     'f4'),
        ('ask_volume_1',    'f4'),
        ('ask_price_2',     'f4'),
        ('ask_volume_2',    'f4'),
        ('ask_price_3',     'f4'),
        ('ask_volume_3',    'f4'),
        ('ask_price_4',     'f4'),
        ('ask_volume_4',    'f4'),
        ('ask_price_5',     'f4'),
        ('ask_volume_5',    'f4'),
        ('bid_price_1',     'f4'),
        ('bid_volume_1',    'f4'), 
        ('bid_price_2',     'f4'),
        ('bid_volume_2',    'f4'),
        ('bid_price_3',     'f4'),
        ('bid_volume_3',    'f4'),
        ('bid_price_4',     'f4'),
        ('bid_volume_4',    'f4'),
        ('bid_price_5',     'f4'),
        ('bid_volume_5',    'f4'),
        ('high_price',      'f4'),
        ('last_price',      'f4'),
        ('low_price',       'f4'),
        ('mkt_time',        'i8'),
        ('open_price',      'f4'),
        ('prev_close_price','f4'),
        ('turnover',        'f4'),
        ('volume',          'f4'),
    ]

    DROP_COLUMN = ['change_rate', 'limit_up', 'limit_down']

    MATCH_DICT = {
        'a1'            :   'ask_price_1',
        'a1_v'          :   'ask_volume_1',
        'a2'            :   'ask_price_2',
        'a2_v'          :   'ask_volume_2',
        'a3'            :   'ask_price_3',
        'a3_v'          :   'ask_volume_3',
        'a4'            :   'ask_price_4',
        'a4_v'          :   'ask_volume_4',
        'a5'            :   'ask_price_5',
        'a5_v'          :   'ask_volume_5',
        'b1'            :   'bid_price_1',
        'b1_v'          :   'bid_volume_1',
        'b2'            :   'bid_price_2',
        'b2_v'          :   'bid_volume_2',
        'b3'            :   'bid_price_3',
        'b3_v'          :   'bid_volume_3',
        'b4'            :   'bid_price_4',
        'b4_v'          :   'bid_volume_4',
        'b5'            :   'bid_price_5',
        'b5_v'          :   'bid_volume_5',
        'high'          :   'high_price',
        'last'          :   'last_price',
        'low'           :   'low_price',
        'open'          :   'open_price',
        'prev_close'    :   'prev_close_price',
        'time'          :   'mkt_time',
        'total_turnover':   'turnover',
        'volume'        :   'volume',
    }

    def change_time(self, df):
        df.loc[:,'mkt_time'] = (df['mkt_time'].copy(deep=True) - np.datetime64('1970-01-01T00:00:00Z')) / np.timedelta64(1, 's')*pow(10,9)
        return df

class OneTokenTicksClean(CleanBase):

    DATA_TYPE  = [
        ('ask_price_1',     'f4'),
        ('ask_volume_1',    'f4'),
        ('ask_price_2',     'f4'),
        ('ask_volume_2',    'f4'),
        ('ask_price_3',     'f4'),
        ('ask_volume_3',    'f4'),
        ('ask_price_4',     'f4'),
        ('ask_volume_4',    'f4'),
        ('ask_price_5',     'f4'),
        ('ask_volume_5',    'f4'),
        ('bid_price_1',     'f4'),
        ('bid_volume_1',    'f4'),
        ('bid_price_2',     'f4'),
        ('bid_volume_2',    'f4'),
        ('bid_price_3',     'f4'),
        ('bid_volume_3',    'f4'),
        ('bid_price_4',     'f4'),
        ('bid_volume_4',    'f4'),
        ('bid_price_5',     'f4'),
        ('bid_volume_5',    'f4'),
        ('last_price',      'f4'),
        ('mkt_time',        'i8'),
        ('volume',          'f4'),
    ]

    DROP_COLUMN = ['{}_{}_{}'.format(i, j, k) for i in ['ask', 'bid'] for j in range(5,10) for k in ['p', 'v']]+ ['time']

    MATCH_DICT = {
        'last'          :   'last_price',
        'timestamp'     :   'mkt_time',
        'volume'        :   'volume',
        'ask_0_p'       :   'ask_price_1',
        'ask_0_v'       :   'ask_volume_1',
        'ask_1_p'       :   'ask_price_2',
        'ask_1_v'       :   'ask_volume_2',
        'ask_2_p'       :   'ask_price_3',
        'ask_2_v'       :   'ask_volume_3',
        'ask_3_p'       :   'ask_price_4',
        'ask_3_v'       :   'ask_volume_4',
        'ask_4_p'       :   'ask_price_5',
        'ask_4_v'       :   'ask_volume_5',
        'bid_0_p'       :   'bid_price_1',
        'bid_0_v'       :   'bid_volume_1',
        'bid_1_p'       :   'bid_price_2',
        'bid_1_v'       :   'bid_volume_2',
        'bid_2_p'       :   'bid_price_3',
        'bid_2_v'       :   'bid_volume_3',
        'bid_3_p'       :   'bid_price_4',
        'bid_3_v'       :   'bid_volume_4',
        'bid_4_p'       :   'bid_price_5',
        'bid_4_v'       :   'bid_volume_5',    
    }
    
    def change_time(self, df):
        df.loc[:,'mkt_time'] = df['mkt_time'].copy(deep=True) *pow(10,6)
        return df


class OneTokenTradesClean(CleanBase):
    
    DATA_TYPE = [
        ('amount',          'f4'),
        ('direction',       'S1'),
        ('mkt_time',        'i8'),
        ('price',           'f4'),
        ('receive_time',    'i8'),
    ]
    
    DROP_COLUMN = ['contract', 'exchange_time', 'time']

    MATCH_DICT = {
        'amount'                :   'amount',
        'bs'                    :   'direction',
        'exchange_timestamp'    :   'mkt_time',
        'timestamp'             :   'receive_time',
        'price'                 :   'price',
    }
   
    def change_time(self, df):
        df.loc[:,'mkt_time'] = df['mkt_time'].copy(deep=True) *pow(10,9)
        df.loc[:,'receive_time'] = df['receive_time'].copy(deep=True) *pow(10,9)
        return df

class OkefTicksClean(CleanBase):
    
    DATA_TYPE  = [
        ('ask_price_1',     'f4'),
        ('ask_volume_1',    'f4'),
        ('ask_price_2',     'f4'),
        ('ask_volume_2',    'f4'),
        ('ask_price_3',     'f4'),
        ('ask_volume_3',    'f4'),
        ('ask_price_4',     'f4'),
        ('ask_volume_4',    'f4'),
        ('ask_price_5',     'f4'),
        ('ask_volume_5',    'f4'),
        ('bid_price_1',     'f4'),
        ('bid_volume_1',    'f4'),
        ('bid_price_2',     'f4'),
        ('bid_volume_2',    'f4'),
        ('bid_price_3',     'f4'),
        ('bid_volume_3',    'f4'),
        ('bid_price_4',     'f4'),
        ('bid_volume_4',    'f4'),
        ('bid_price_5',     'f4'),
        ('bid_volume_5',    'f4'),
        ('last_price',      'f4'),
        ('mkt_time',        'i8'),
        ('volume',          'f4'),
    ]

    DROP_COLUMN = ['{}_{}_{}'.format(i, j, k) for i in ['ask', 'bid'] for j in range(5,20) for k in ['p', 'v']]+ ['time']

    MATCH_DICT = {
        'ask_0_p'           :   'ask_price_1',
        'ask_0_v'           :   'ask_volume_1',
        'ask_1_p'           :   'ask_price_2',
        'ask_1_v'           :   'ask_volume_2',
        'ask_2_p'           :   'ask_price_3',
        'ask_2_v'           :   'ask_volume_3',
        'ask_3_p'           :   'ask_price_4',
        'ask_3_v'           :   'ask_volume_4',
        'ask_4_p'           :   'ask_price_5',
        'ask_4_v'           :   'ask_volume_5',
        'bid_0_p'           :   'bid_price_1',
        'bid_0_v'           :   'bid_volume_1',
        'bid_1_p'           :   'bid_price_2',
        'bid_1_v'           :   'bid_volume_2',
        'bid_2_p'           :   'bid_price_3',
        'bid_2_v'           :   'bid_volume_3',
        'bid_3_p'           :   'bid_price_4',
        'bid_3_v'           :   'bid_volume_4',
        'bid_4_p'           :   'bid_price_5',
        'bid_4_v'           :   'bid_volume_5',
        'last'              :   'last_price',
        'timestamp'         :   'mkt_time',
        'volume'            :   'volume',
    }

    def change_time(self, df):
        df.loc[:,'mkt_time'] = df['mkt_time'].copy(deep=True) *pow(10,6)
        return df


class CryptoBarsClean(CleanBase):

    DATA_TYPE  = [
        ('close_price',     'f4'),
        ('high_price',      'f4'),
        ('low_price',       'f4'),
        ('mkt_time',        'i8'),
        ('open_price',      'f4'),
        ('receive_time',    'i8'),
        ('volume',          'f4'),
    ]

    DROP_COLUMN = ['asset_type', 'exchange', 'frame_err_id', 'frame_msg_type', 'frame_req_id', 'frame_source', 'name', 'sec_interval', 'ticker', 'trading_day']

    MATCH_DICT = {
        'close'         :   'close_price',
        'high'          :   'high_price',
        'low'           :   'low_price',
        'open'          :   'open_price',
        'time'          :   'mkt_time',
        'volume'        :   'volume',
        'frame_dt'      :   'receive_time',
    }

    def change_time(self, df):
        return df
 
class CryptoTicksClean(CleanBase):

    DATA_TYPE  = [
        ('ask_price_1',     'f4'),
        ('ask_volume_1',    'f4'),
        ('ask_price_2',     'f4'),
        ('ask_volume_2',    'f4'),
        ('ask_price_3',     'f4'),
        ('ask_volume_3',    'f4'),
        ('ask_price_4',     'f4'),
        ('ask_volume_4',    'f4'),
        ('ask_price_5',     'f4'),
        ('ask_volume_5',    'f4'),
        ('bid_price_1',     'f4'),
        ('bid_volume_1',    'f4'),
        ('bid_price_2',     'f4'),
        ('bid_volume_2',    'f4'),
        ('bid_price_3',     'f4'),
        ('bid_volume_3',    'f4'),
        ('bid_price_4',     'f4'),
        ('bid_volume_4',    'f4'),
        ('bid_price_5',     'f4'),
        ('bid_volume_5',    'f4'),
        ('mkt_time',        'i8'),
        ('receive_time',    'i8'),
    ]

    DROP_COLUMN = ['asset_type', 'exchange', 'frame_err_id', 'frame_msg_type', 'frame_req_id', 'frame_source', 'name', 'ticker', 'trading_day']

    MATCH_DICT = {
        'ask_price1'            :   'ask_price_1',
        'ask_volume1'           :   'ask_volume_1',
        'ask_price2'            :   'ask_price_2',
        'ask_volume2'           :   'ask_volume_2',
        'ask_price3'            :   'ask_price_3',
        'ask_volume3'           :   'ask_volume_3',
        'ask_price4'            :   'ask_price_4',
        'ask_volume4'           :   'ask_volume_4',
        'ask_price5'            :   'ask_price_5',
        'ask_volume5'           :   'ask_volume_5',
        'bid_price1'            :   'bid_price_1',
        'bid_volume1'           :   'bid_volume_1',
        'bid_price2'            :   'bid_price_2',
        'bid_volume2'           :   'bid_volume_2',
        'bid_price3'            :   'bid_price_3',
        'bid_volume3'           :   'bid_volume_3',
        'bid_price4'            :   'bid_price_4',
        'bid_volume4'           :   'bid_volume_4',
        'bid_price5'            :   'bid_price_5',
        'bid_volume5'           :   'bid_volume_5',
        'time'                  :   'mkt_time',
        'frame_dt'              :   'receive_time',
    }

    def change_time(self, df):
        return df

class CryptoTradesClean(CleanBase):
    
    DATA_TYPE = [
        ('mkt_time',        'i8'),
        ('price',           'f4'),
        ('receive_time',    'i8'),
        ('volume',          'f4'),
    ]
    
    DROP_COLUMN = ['asset_type', 'buy_order_index', 'exchange', 'frame_err_id', 'frame_msg_type', 'frame_req_id', 'frame_source', 'group_id', 'index', 'name', 'order_type', 'sell_order_index','ticker', 'trading_day']

    MATCH_DICT = {
        'volume'                :   'volume',
        'time'                  :   'mkt_time',
        'frame_dt'              :   'receive_time',
        'price'                 :   'price',
    }
   
    def change_time(self, df):
        return df

class BtctaSpotBarClean(CleanBase):
    
    DATA_TYPE = [
        ('close_price',     'f4'),
        ('high_price',      'f4'),
        ('low_price',       'f4'),
        ('mkt_time',        'i8'),
        ('open_price',      'f4'),
        ('volume',          'f4'),
    ]
    
    DROP_COLUMN = []

    MATCH_DICT = {
        'close'                 :   'close_price',
        'high'                  :   'high_price',
        'low'                   :   'low_price',
        'open'                  :   'open_price',
        'timestamp'             :   'mkt_time',
        'volume'                :   'volume',
    }

    def change_time(self, df):
        df.loc[:,'mkt_time'] = (pd.to_datetime(df['mkt_time'].copy(deep=True)) - np.datetime64('1970-01-01T00:00:00Z')) / np.timedelta64(1, 's')*pow(10,9)
        return df


class BtctaSpotTickClean(CleanBase):
    
    DATA_TYPE = [
        
        ('ask_price_1',     'f4'),
        ('bid_price_1',     'f4'),
        ('high_price',      'f4'),
        ('last_price',      'f4'),
        ('low_price',       'f4'),
        ('mkt_time',        'i8'),
        ('open_price',      'f4'),
        ('volume',          'f4'),
        ('turnover',        'f4'),
    ]
    
    DROP_COLUMN = []

    MATCH_DICT = {
        'amount'                 :   'turnover',
        'best_ask'               :   'ask_price_1',
        'best_bid'               :   'bid_price_1',
        'high'                   :   'high_price',
        'last'                   :   'last_time',
        'low'                    :   'low_time',
        'open'                   :   'open_price',
        'timestamp'              :   'mkt_time',
        'volume'                 :   'volume',
    }

    def change_time(self, df):
        df.loc[:,'mkt_time'] = (pd.to_datetime(df['mkt_time'].copy(deep=True)) - np.datetime64('1970-01-01T00:00:00Z')) / np.timedelta64(1, 's')*pow(10,9)
        return df

class BtctaSpotTradeClean(CleanBase):
    
    DATA_TYPE = [
        ('direction',       'S1'),
        ('mkt_time',        'i8'),
        ('price',           'f4'),
        ('trade_id',        'i8'),
        ('volume',          'f4'),
    ]
    
    DROP_COLUMN = []

    MATCH_DICT = {
        'price'                 :   'price',
        'side'                  :   'direction',
        'size'                  :   'volume',
        'timestamp'             :   'mkt_time',
        'trade_id'              :   'trade_id',
    }

    def change_time(self, df):
        df.loc[:,'mkt_time'] = (pd.to_datetime(df['mkt_time'].copy(deep=True)) - np.datetime64('1970-01-01T00:00:00Z')) / np.timedelta64(1, 's')*pow(10,9)
        df.loc[:,'direction'] = [i[0].lower() for i in df['direction'].copy(deep=True).values]
        return df


class BtctaSpotDepthClean(CleanBase):

    DATA_TYPE  = [
        ('ask_price_1',     'f4'),
        ('ask_volume_1',    'f4'),
        ('ask_price_2',     'f4'),
        ('ask_volume_2',    'f4'),
        ('ask_price_3',     'f4'),
        ('ask_volume_3',    'f4'),
        ('ask_price_4',     'f4'),
        ('ask_volume_4',    'f4'),
        ('ask_price_5',     'f4'),
        ('ask_volume_5',    'f4'),
        ('bid_price_1',     'f4'),
        ('bid_volume_1',    'f4'),
        ('bid_price_2',     'f4'),
        ('bid_volume_2',    'f4'),
        ('bid_price_3',     'f4'),
        ('bid_volume_3',    'f4'),
        ('bid_price_4',     'f4'),
        ('bid_volume_4',    'f4'),
        ('bid_price_5',     'f4'),
        ('bid_volume_5',    'f4'),
        ('mkt_time',        'i8'),
    ]

    DROP_COLUMN = []

    MATCH_DICT = {
        'ask_1_p'                :   'ask_price_1',
        'ask_1_v'                :   'ask_volume_1',
        'ask_2_p'                :   'ask_price_2',
        'ask_2_v'                :   'ask_volume_2',
        'ask_3_p'                :   'ask_price_3',
        'ask_3_v'                :   'ask_volume_3',
        'ask_4_p'                :   'ask_price_4',
        'ask_4_v'                :   'ask_volume_4',
        'ask_5_p'                :   'ask_price_5',
        'ask_5_v'                :   'ask_volume_5',
        'bid_1_p'                :   'bid_price_1',
        'bid_1_v'                :   'bid_volume_1',
        'bid_2_p'                :   'bid_price_2',
        'bid_2_v'                :   'bid_volume_2',
        'bid_3_p'                :   'bid_price_3',
        'bid_3_v'                :   'bid_volume_3',
        'bid_4_p'                :   'bid_price_4',
        'bid_4_v'                :   'bid_volume_4',
        'bid_5_p'                :   'bid_price_5',
        'bid_5_v'                :   'bid_volume_5',
        'timestamp'              :   'mkt_time',
    }

    def change_time(self, df):
        df.loc[:,'mkt_time'] = (pd.to_datetime(df['mkt_time'].copy(deep=True)) - np.datetime64('1970-01-01T00:00:00Z')) / np.timedelta64(1, 's')*pow(10,9)
        return df


class BtctaFutureBarClean(CleanBase):

    DATA_TYPE  = [
        ('close_price',         'f4'),
        ('foreign_notional',    'f4'),
        ('high_price',          'f4'),
        ('home_notional',       'f4'),
        ('low_price',           'f4'),
        ('mkt_time',            'i8'),
        ('num_trades',          'i4'),
        ('open_price',          'f4'),
        ('turnover',            'f4'),
        ('volume',              'f4')
    ]

    DROP_COLUMN = ['lastSize','vwap']

    MATCH_DICT = {
        'close'                :   'close_price',
        'foreignNotional'      :   'foreign_notional',
        'high'                 :   'high_price',
        'homeNotional'         :   'home_notional',
        'low'                  :   'low_price',
        'open'                 :   'open_price',
        'trades'               :   'num_trades',
        'turnover'             :   'turnover',
        'volume'               :   'volume',
        'timestamp'            :   'mkt_time',
    }

    def change_time(self, df):
        df.loc[:,'mkt_time'] = (pd.to_datetime(df['mkt_time'].copy(deep=True)) - np.datetime64('1970-01-01T00:00:00Z')) / np.timedelta64(1, 's')*pow(10,9)
        return df

class BtctaFutureTickClean(CleanBase):

    DATA_TYPE  = [
        ('last_price',          'f4'),
        ('mkt_time',            'i8'),
        ('open_price',          'f4'),
        ('turnover',            'f4'),
        ('volume',              'f4')
    ]

    DROP_COLUMN = []

    MATCH_DICT = {
        'amount'                :   'turnover',
        'last'                  :   'last_price',
        'open'                  :   'open_price',
        'timestamp'             :   'mkt_time',
        'volume'                :   'volume',
    }

    def change_time(self, df):
        df.loc[:,'mkt_time'] = (pd.to_datetime(df['mkt_time'].copy(deep=True)) - np.datetime64('1970-01-01T00:00:00Z')) / np.timedelta64(1, 's')*pow(10,9)
        return df

class BtctaFutureTradeClean(CleanBase):

    DATA_TYPE  = [
        ('amount',              'f8'),
        ('direction',           'S1'),
        ('foreign_notional',    'f8'),
        ('home_notional',       'f8'),
        ('mkt_time',            'i8'),
        ('price',               'f4'),
        ('volume',              'f4')
    ]

    DROP_COLUMN = []

    MATCH_DICT = {
        'foreignNotional'       :   'foreign_notional',
        'grossValue'            :   'amount',
        'homeNotional'          :   'home_notional',
        'price'                 :   'price',
        'side'                  :   'direction',
        'size'                  :   'volume',
        'timestamp'             :   'mkt_time',   
    }

    def change_time(self, df):
        df.loc[:,'mkt_time'] = (pd.to_datetime(df['mkt_time'].copy(deep=True)) - np.datetime64('1970-01-01T00:00:00Z')) / np.timedelta64(1, 's')*pow(10,9)
        df.loc[:,'direction'] = [i[0].lower() for i in df['direction'].copy(deep=True).values]
        return df


class BtctaFutureDepthClean(CleanBase):

    DATA_TYPE  = [
        ('ask_price_1',     'f4'),
        ('ask_volume_1',    'f4'),
        ('ask_price_2',     'f4'),
        ('ask_volume_2',    'f4'),
        ('ask_price_3',     'f4'),
        ('ask_volume_3',    'f4'),
        ('ask_price_4',     'f4'),
        ('ask_volume_4',    'f4'),
        ('ask_price_5',     'f4'),
        ('ask_volume_5',    'f4'),
        ('bid_price_1',     'f4'),
        ('bid_volume_1',    'f4'),
        ('bid_price_2',     'f4'),
        ('bid_volume_2',    'f4'),
        ('bid_price_3',     'f4'),
        ('bid_volume_3',    'f4'),
        ('bid_price_4',     'f4'),
        ('bid_volume_4',    'f4'),
        ('bid_price_5',     'f4'),
        ('bid_volume_5',    'f4'),
        ('mkt_time',        'i8'),
    ]

    DROP_COLUMN = [ 'ask_6_p','ask_6_v','bid_6_p','bid_6_v',
                    'ask_7_p','ask_7_v','bid_7_p','bid_7_v',
                    'ask_8_p','ask_8_v','bid_8_p','bid_8_v',
                    'ask_9_p','ask_9_v','bid_9_p','bid_9_v',
                    'ask_10_p','ask_10_v','bid_10_p','bid_10_v']

    MATCH_DICT = {
        'ask_1_p'                :   'ask_price_1',
        'ask_1_v'                :   'ask_volume_1',
        'ask_2_p'                :   'ask_price_2',
        'ask_2_v'                :   'ask_volume_2',
        'ask_3_p'                :   'ask_price_3',
        'ask_3_v'                :   'ask_volume_3',
        'ask_4_p'                :   'ask_price_4',
        'ask_4_v'                :   'ask_volume_4',
        'ask_5_p'                :   'ask_price_5',
        'ask_5_v'                :   'ask_volume_5',
        'bid_1_p'                :   'bid_price_1',
        'bid_1_v'                :   'bid_volume_1',
        'bid_2_p'                :   'bid_price_2',
        'bid_2_v'                :   'bid_volume_2',
        'bid_3_p'                :   'bid_price_3',
        'bid_3_v'                :   'bid_volume_3',
        'bid_4_p'                :   'bid_price_4',
        'bid_4_v'                :   'bid_volume_4',
        'bid_5_p'                :   'bid_price_5',
        'bid_5_v'                :   'bid_volume_5',
        'timestamp'              :   'mkt_time',
    }

    def change_time(self, df):
        df.loc[:,'mkt_time'] = (pd.to_datetime(df['mkt_time'].copy(deep=True)) - np.datetime64('1970-01-01T00:00:00Z')) / np.timedelta64(1, 's')*pow(10,9)
        return df