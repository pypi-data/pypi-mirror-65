from . import DataManager
import pandas as pd
import dataclasses
import datetime
from fund.db.database import RawDatabaseConnector, BasicDatabaseConnector, DerivedDatabaseConnector
from ..struct import AssetWeight, AssetPrice, FundScoreParam, FundScoreHelper
from ..view.raw_models import *
from ..view.basic_models import *
from ..view.derived_models import *


@dataclasses.dataclass
class FundDataTables:
    # basic
    trading_days: pd.DataFrame = None
    index_info: pd.DataFrame = None
    index_price: pd.DataFrame = None
    index_pct: pd.DataFrame = None
    fund_info: pd.DataFrame = None
    fund_score: pd.DataFrame = None
    fund_list: set = None
    fund_nav: pd.DataFrame = None

    def __post_init__(self):
        self.fund_list = self.fund_list or set([])

    def __repr__(self):
        s = '<DTS'
        for k, v in self.__dict__.items():
            s += f' {k}:{v.shape if isinstance(v, pd.DataFrame) else (len(v) if isinstance(v, set) or isinstance(v, list) else None)}'
        s += '>'
        return s

class FundDataManager(DataManager):

    def __init__(self, start_time=None, end_time=None, fund_score_param: FundScoreParam=None):
        DataManager.__init__(self, 
            start_time or datetime.datetime(2005, 1, 1), 
            end_time or datetime.datetime.now()
        )
        self._fund_score_param = fund_score_param or FundScoreParam(tag_type=1, score_method=1, is_full=1)
        self.dts = FundDataTables()

    def init(self, index_list=None):
        index_list = index_list or list(AssetWeight.__dataclass_fields__.keys())
        # get derived data first
        with DerivedDatabaseConnector().managed_session() as derived_session:
            # fund_score
            tag_names = list(map(lambda x: FundScoreHelper.get(x), index_list))
            _fund_score_query = derived_session.query(
                    FundScore.fund_id,
                    FundScore.datetime,
                    FundScore.score, 
                    FundScore.tag_name, 
                    FundScore.score_method,
                    FundScore.is_full,
                    FundScore.tag_type
                ).filter(
                    FundScore.tag_name.in_(tag_names),
                    FundScore.score_method == self._fund_score_param.score_method,
                    FundScore.is_full == self._fund_score_param.is_full,
                    FundScore.tag_type == self._fund_score_param.tag_type
                )
            self.dts.fund_score = pd.read_sql(_fund_score_query.statement, _fund_score_query.session.bind)
            self.dts.fund_score['index_id'] = self.dts.fund_score.tag_name.apply(lambda x: FundScoreHelper.parse(x))
            # update fund_list with tag score
            self.dts.fund_list = set(self.dts.fund_score.fund_id)

        # info is necessary
        with BasicDatabaseConnector().managed_session() as quant_session:
            def fetch_table(view):
                query = quant_session.query(view)
                return pd.read_sql(query.statement, query.session.bind)
            self.dts.fund_info = fetch_table(FundInfo)
            self.dts.trading_days = fetch_table(TradingDayList)
            # index
            self.dts.index_info = fetch_table(IndexInfo)
            _index_query = quant_session.query(IndexPrice.index_id, IndexPrice.datetime, IndexPrice.close).filter(IndexPrice.index_id.in_(index_list))
            self.dts.index_price = pd.read_sql(_index_query.statement, _index_query.session.bind).pivot_table(index='datetime', columns='index_id', values='close').fillna(method= 'ffill')
            # fund nav
            _fund_nav_query = quant_session.query(
                    FundNav.fund_id,
                    FundNav.adjusted_net_value,
                    FundNav.subscribe_status, 
                    FundNav.redeem_status, 
                    FundNav.datetime
                ).filter(
                    FundNav.fund_id.in_(self.dts.fund_list),
                    FundNav.datetime >= self.start_date,
                    FundNav.datetime <= self.end_date,
                )
            self.dts.fund_nav = pd.read_sql(_fund_nav_query.statement, _fund_nav_query.session.bind)

        # raw index val pct, only used in tactic asset allocation
        with RawDatabaseConnector().managed_session() as quant_session:
            query = quant_session.query(IndexValPct)
            df = pd.read_sql(query.statement, query.session.bind).pivot_table(index='datetime', columns='index_id', values='pe_pct').fillna(method='ffill')
            self.dts.index_pct = df.rename(columns=FundScoreHelper.TACTIC_ASSET_CONVERT)
            '''
            self.index_pct = {}
            self.index_pct['hs300'] = index_valpct[index_valpct['index_id'] == '000300.XSHG'][['datetime', 'pe_pct']].set_index('datetime')
            self.index_pct['csi500'] = index_valpct[index_valpct['index_id'] == '000905.XSHG'][['datetime', 'pe_pct']].set_index('datetime')
            self.index_pct['hs300']  = self.index_data[['hs300']].join(self.index_pct['hs300']).fillna(method = 'ffill')[['pe_pct']]
            self.index_pct['csi500'] = self.index_data[['csi500']].join(self.index_pct['csi500']).fillna(method = 'ffill')[['pe_pct']]
            '''
        print(self.dts)

    def get_index_pcts(self, dt):
        # jch: only pct within 7 days take effect
        INDEX_PCT_EFFECTIVE_DELAY_DAY_NUM = 7
        res = {}
        for index_id in self.dts.index_pct.columns:
            df = self.dts.index_pct[index_id]
            _filtered = df[(df.index <= dt) & (df.index >= dt - datetime.timedelta(days=INDEX_PCT_EFFECTIVE_DELAY_DAY_NUM))]
            if len(_filtered) > 0:
                res[index_id] = _filtered.iloc[-1]
        return res

    def get_fund_score(self, dt, index_id) -> dict: 
        df = self.dts.fund_score
        # jch: only score within 14 days take effect
        SCORE_EFFECTIVE_DELAY_DAY_NUM = 14
        # 注意，对于dt天结束时的分析，可以选用当天的打分！
        # TODO: 打分这里，可以考虑根据时间最后打分时间到现在，进行分数的适当扣减？
        _filtered = df[(df.index_id==index_id) & (df.datetime <= dt) & (df.datetime >= dt - datetime.timedelta(days=SCORE_EFFECTIVE_DELAY_DAY_NUM))]
        return {fund_id: _filtered[_filtered.fund_id==fund_id].iloc[-1].score for fund_id in set(_filtered.fund_id)}

    def get_fund_info(self, fund_id=None):
        '''
        fund_id                                                   000001!0
        wind_id                                                  000001.OF
        transition                                                       0
        order_book_id                                               000001
        desc_name                                                     华夏成长
        start_date                                              2001-12-18
        end_date                                                2040-12-31
        wind_class_1                                                 混合型基金
        wind_class_2                                               偏股混合型基金
        manager_id       王亚伟(20011218-20050412)\r\n田擎(20040227-20051029...
        company_id                                                    华夏基金
        benchmark                                                        0
        full_name                                               华夏成长证券投资基金
        currency                                                       CNY
        base_fund_id                                                     0
        is_structured                                                    0
        is_open                                                          0
        asset_type                                                    null
        update_time                                             2020-03-24
        manage_fee                                                     1.5
        trustee_fee                                                   0.25
        purchase_fee                                                   NaN
        redeem_fee                                                     NaN
        note                                                          None
        track_index                                                   none
        '''
        if fund_id:
            df = self.dts.fund_info
            _filtered = df[df['fund_id']=='000001!0']
            return None if len(_filtered) == 0 else _filtered.iloc[0]
        else:
            return self.dts.fund_info.copy()

    def get_trading_days(self):
        return self.dts.trading_days.copy()

    def get_index_price(self, dt=None):
        if dt:
            return self.dts.index_price.loc[dt]
        else:
            return self.dts.index_price.copy()
    
    def get_index_price_data(self, dt):
        _index_price = self.get_index_price(dt)
        return AssetPrice(**_index_price.to_dict())

if __name__ == '__main__':
    m = FundDataManager('20100101', '20200101')
    m.init()
    print(m.get_fund_info(fund_id=None))
    print(m.get_fund_info(fund_id='000001!0'))
    print(m.get_trading_days())