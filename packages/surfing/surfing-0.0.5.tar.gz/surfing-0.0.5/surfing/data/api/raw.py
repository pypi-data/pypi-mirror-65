import pandas as pd
from ..wrapper.mysql import RawDatabaseConnector
from ..view.raw_models import *


class RawDataApi(object):
    def get_raw_cm_index_price_df(self, start_date, end_date):
        with RawDatabaseConnector().managed_session() as db_session:
            try:
                query = db_session.query(
                    CmIndexPrice
                ).filter(
                    CmIndexPrice.datetime >= start_date,
                    CmIndexPrice.datetime <= end_date
                )
                df = pd.read_sql(query.statement, query.session.bind)
                return df

            except Exception as e:
                print('Failed to get data <err_msg> {}'.format(e))

    def get_cxindex_index_price_df(self, start_date, end_date):
        with RawDatabaseConnector().managed_session() as db_session:
            try:
                query = db_session.query(
                    CxindexIndexPrice
                ).filter(
                    CxindexIndexPrice.datetime >= start_date,
                    CxindexIndexPrice.datetime <= end_date
                )
                df = pd.read_sql(query.statement, query.session.bind)
                return df

            except Exception as e:
                print('Failed to get data <err_msg> {}'.format(e))

    def get_yahoo_index_price_df(self, start_date, end_date):
        with RawDatabaseConnector().managed_session() as db_session:
            try:
                query = db_session.query(
                    YahooIndexPrice
                ).filter(
                    YahooIndexPrice.datetime >= start_date,
                    YahooIndexPrice.datetime <= end_date
                )
                df = pd.read_sql(query.statement, query.session.bind)
                return df

            except Exception as e:
                print('Failed to get data <err_msg> {}'.format(e))

    def get_rq_index_price_df(self, start_date, end_date):
        with RawDatabaseConnector().managed_session() as db_session:
            try:
                query = db_session.query(
                    RqIndexPrice
                ).filter(
                    RqIndexPrice.datetime >= start_date,
                    RqIndexPrice.datetime <= end_date
                )
                df = pd.read_sql(query.statement, query.session.bind)
                return df

            except Exception as e:
                print('Failed to get data <err_msg> {}'.format(e))

    def get_wind_fund_info(self):
        with RawDatabaseConnector().managed_session() as db_session:
            try:
                query = db_session.query(
                    WindFundInfo
                )
                df = pd.read_sql(query.statement, query.session.bind)
                return df

            except Exception as e:
                print('Failed to get data <err_msg> {}'.format(e))

    def get_fund_fee(self):
        with RawDatabaseConnector().managed_session() as db_session:
            try:
                query = db_session.query(
                    FundFee
                )
                df = pd.read_sql(query.statement, query.session.bind)
                return df

            except Exception as e:
                print('Failed to get data <err_msg> {}'.format(e))

    def get_fund_rating(self):
        with RawDatabaseConnector().managed_session() as db_session:
            try:
                query = db_session.query(
                    FundRating
                )
                df = pd.read_sql(query.statement, query.session.bind)
                return df

            except Exception as e:
                print('Failed to get data <err_msg> {}'.format(e))

    def get_stock_fin_fac(self, stock_id_list, start_date):
        with RawDatabaseConnector().managed_session() as db_session:
            try:
                query = db_session.query(
                    RqStockFinFac
                ).filter(
                    RqStockFinFac.stock_id.in_(stock_id_list),
                    RqStockFinFac.datetime >= start_date,
                )
                df = pd.read_sql(query.statement, query.session.bind)
                return df

            except Exception as e:
                print('Failed to get data <err_msg> {}'.format(e))

    def get_rq_stock_valuation(self, stock_id_list, start_date):
        with RawDatabaseConnector().managed_session() as db_session:
            try:
                query = db_session.query(
                    RqStockValuation.datetime,
                    RqStockValuation.stock_id,
                    RqStockValuation.pb_ratio_lf,
                    RqStockValuation.pe_ratio_ttm,
                    RqStockValuation.peg_ratio_ttm,
                    RqStockValuation.dividend_yield_ttm,
                ).filter(
                    RqStockValuation.stock_id.in_(stock_id_list),
                    RqStockValuation.datetime >= start_date,

                )
                df = pd.read_sql(query.statement, query.session.bind)
                return df

            except Exception as e:
                print('Failed to get data <err_msg> {}'.format(e))

    def get_rq_index_weight(self, index_id_list, start_date):
        with RawDatabaseConnector().managed_session() as quant_session:
            try:
                query = quant_session.query(
                        RqIndexWeight.index_id,
                        RqIndexWeight.datetime,
                        RqIndexWeight.stock_list,
                    ).filter(
                        RqIndexWeight.index_id.in_(index_id_list),
                        RqIndexWeight.datetime >= start_date,
                    )
                df = pd.read_sql(query.statement, query.session.bind)
                return df
            
            except Exception as e:
                print('Failed to get data <err_msg> {}'.format(e))

    def get_index_val_pct(self):
        with RawDatabaseConnector().managed_session() as quant_session:
            try:
                query = quant_session.query(
                        IndexValPct
                    )
                df = pd.read_sql(query.statement, query.session.bind)
                return df
            
            except Exception as e:
                print('Failed to get data <err_msg> {}'.format(e))

    def get_rq_fund_indicator(self, start_date, end_date):
        with RawDatabaseConnector().managed_session() as db_session:
            try:
                query = db_session.query(
                    RqFundIndicator
                ).filter(
                    RqFundIndicator.datetime >= start_date,
                    RqFundIndicator.datetime <= end_date
                )
                df = pd.read_sql(query.statement, query.session.bind)
                return df
            except Exception as e:
                print('Failed to get data <err_msg> {}'.format(e))
                return None

    def get_trading_day_list(self, start_date, end_date):
        with RawDatabaseConnector().managed_session() as db_session:
            try:
                query = db_session.query(
                    TradingDayList
                ).filter(
                    TradingDayList.datetime >= start_date,
                    TradingDayList.datetime <= end_date
                )
                df = pd.read_sql(query.statement, query.session.bind)
                return df
            except Exception as e:
                print('Failed to get data <err_msg> {}'.format(e))
                return None

    def get_stock_info(self):
        with RawDatabaseConnector().managed_session() as db_session:
            try:
                query = db_session.query(
                    StockInfo
                )
                df = pd.read_sql(query.statement, query.session.bind)
                return df
            except Exception as e:
                print('Failed to get data <err_msg> {}'.format(e))
                return None

    def get_fund_nav(self, start_date, end_date):
        with RawDatabaseConnector().managed_session() as db_session:
            try:
                query = db_session.query(
                    RqFundNav
                ).filter(
                    RqFundNav.datetime >= start_date,
                    RqFundNav.datetime <= end_date
                )
                df = pd.read_sql(query.statement, query.session.bind)
                return df
            except Exception as e:
                print('Failed to get data <err_msg> {}'.format(e))
                return None

    def get_fund_size(self):
        with RawDatabaseConnector().managed_session() as db_session:
            try:
                query = db_session.query(
                    RqFundSize
                )
                df = pd.read_sql(query.statement, query.session.bind)
                return df
            except Exception as e:
                print('Failed to get data <err_msg> {}'.format(e))
                return None

    def get_rq_stock_price(self, start_date, end_date):
        with RawDatabaseConnector().managed_session() as db_session:
            try:
                query = db_session.query(
                    RqStockPrice
                ).filter(
                    RqStockPrice.datetime >= start_date,
                    RqStockPrice.datetime <= end_date
                )
                df = pd.read_sql(query.statement, query.session.bind)
                return df
            except Exception as e:
                print('Failed to get data <err_msg> {}'.format(e))
                return None

    def get_rq_stock_post_price(self, start_date, end_date):
        with RawDatabaseConnector().managed_session() as db_session:
            try:
                query = db_session.query(
                    RqStockPostPrice
                ).filter(
                    RqStockPostPrice.datetime >= start_date,
                    RqStockPostPrice.datetime <= end_date
                )
                df = pd.read_sql(query.statement, query.session.bind)
                return df
            except Exception as e:
                print('Failed to get data <err_msg> {}'.format(e))
                return None

