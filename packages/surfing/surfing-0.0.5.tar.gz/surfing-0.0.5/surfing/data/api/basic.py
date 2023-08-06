import math
import pandas as pd
import pickle as pkl
from ..wrapper.mysql import BasicDatabaseConnector
from ..view.basic_models import *

class BasicDataApi(object):
    def get_trading_day_list(self):
        with BasicDatabaseConnector().managed_session() as db_session:
            try:
                query = db_session.query(
                        TradingDayList
                    )
                tag_df = pd.read_sql(query.statement, query.session.bind)
                return tag_df
            
            except Exception as e:
                print('Failed fill get data <err_msg> {}'.format(e))

    def get_fund_info(self):
        with BasicDatabaseConnector().managed_session() as db_session:
            try:
                query = db_session.query(
                        FundInfo
                    )
                tag_df = pd.read_sql(query.statement, query.session.bind)
                return tag_df
            
            except Exception as e:
                print('Failed fill get data <err_msg> {}'.format(e))


    def get_index_info(self):
        with BasicDatabaseConnector().managed_session() as db_session:
            try:
                query = db_session.query(
                        IndexInfo
                    )
                tag_df = pd.read_sql(query.statement, query.session.bind)
                return tag_df
            
            except Exception as e:
                print('Failed fill get data <err_msg> {}'.format(e))            

    def get_stock_info(self):
        with BasicDatabaseConnector().managed_session() as db_session:
            try:
                query = db_session.query(
                        StockInfo
                    )
                tag_df = pd.read_sql(query.statement, query.session.bind)
                return tag_df
            
            except Exception as e:
                print('Failed fill get data <err_msg> {}'.format(e))            

    def get_fund_nav(self, fund_list):
        with BasicDatabaseConnector().managed_session() as db_session:
            try:
                query = db_session.query(
                        FundNav
                ).filter(
                        # We could query all fund_ids at one time
                        FundNav.fund_id.in_(fund_list),
                    )
                    
                tag_df = pd.read_sql(query.statement, query.session.bind)
                return tag_df
            
            except Exception as e:
                print('Failed fill get data <err_msg> {}'.format(e))            

    def get_stock_price(self, stock_list):
        with BasicDatabaseConnector().managed_session() as db_session:
            try:
                query = db_session.query(
                        StockPrice
                ).filter(
                        # We could query all fund_ids at one time
                        StockPrice.stock_id.in_(stock_list),
                    )
                    
                tag_df = pd.read_sql(query.statement, query.session.bind)
                return tag_df
            
            except Exception as e:
                print('Failed fill get data <err_msg> {}'.format(e))            


    def get_fund_ret(self, fund_list):
        with BasicDatabaseConnector().managed_session() as db_session:
            try:
                query = db_session.query(
                        FundRet
                ).filter(
                        # We could query all fund_ids at one time
                        FundRet.fund_id.in_(fund_list),
                    )
                    
                tag_df = pd.read_sql(query.statement, query.session.bind)
                return tag_df
            
            except Exception as e:
                print('Failed fill get data <err_msg> {}'.format(e))            


    def get_index_price(self, index_list):
        with BasicDatabaseConnector().managed_session() as db_session:
            try:
                query = db_session.query(
                        IndexPrice
                ).filter(
                        # We could query all fund_ids at one time
                        IndexPrice.index_id.in_(index_list),
                    )
                    
                tag_df = pd.read_sql(query.statement, query.session.bind)
                return tag_df
            
            except Exception as e:
                print('Failed fill get data <err_msg> {}'.format(e))            


    def get_fund_nav_adjusted_nv(self, fund_list, start_date, end_date):
        with BasicDatabaseConnector().managed_session() as db_session:
            try:
                query = db_session.query(
                        FundNav.adjusted_net_value,
                        FundNav.fund_id,
                        FundNav.datetime,
                ).filter(
                        FundNav.fund_id.in_(fund_list),
                        FundNav.datetime >= start_date,
                        FundNav.datetime <= end_date,
                    )
                    
                tag_df = pd.read_sql(query.statement, query.session.bind)
                return tag_df
            
            except Exception as e:
                print('Failed fill get data <err_msg> {}'.format(e))   


    def get_index_benchmark_data(self, index_list, start_date,end_date):
        with BasicDatabaseConnector().managed_session() as db_session:
            try:
                query = db_session.query(
                        IndexPrice.ret,
                        IndexPrice.index_id,
                        IndexPrice.datetime,
                        IndexPrice.close,
                ).filter(
                        IndexPrice.index_id.in_(index_list),
                        IndexPrice.datetime >= start_date,
                        IndexPrice.datetime <= end_date,
                    )
                    
                tag_df = pd.read_sql(query.statement, query.session.bind)
                return tag_df
            
            except Exception as e:
                print('Failed fill get data <err_msg> {}'.format(e))   


    def get_fund_list(self):
        with BasicDatabaseConnector().managed_session() as db_session:
            try:
                query = db_session.query(
                        FundInfo.fund_id
                    )
                tag_df = pd.read_sql(query.statement, query.session.bind)
                return tag_df
            
            except Exception as e:
                print('Failed fill get data <err_msg> {}'.format(e))

    def get_fund_fee(self):
        with BasicDatabaseConnector().managed_session() as db_session:
            try:
                query = db_session.query(
                        FundInfo.fund_id,
                        FundInfo.manage_fee,
                        FundInfo.trustee_fee,
                    )
                tag_df = pd.read_sql(query.statement, query.session.bind)
                return tag_df
            
            except Exception as e:
                print('Failed fill get data <err_msg> {}'.format(e))

    def get_fund_asset(self):
        with BasicDatabaseConnector().managed_session() as db_session:
            try:
                query = db_session.query(
                        FundInfo.fund_id,
                        FundInfo.asset_type,
                    )
                tag_df = pd.read_sql(query.statement, query.session.bind)
                return tag_df
            
            except Exception as e:
                print('Failed fill get data <err_msg> {}'.format(e))

    def get_fund_id_mapping(self):
        fund_id_mapping = {}
        with BasicDatabaseConnector().managed_session() as db_session:
            try:
                query_results = db_session.query(
                        FundInfo.fund_id,
                        FundInfo.order_book_id,
                        FundInfo.start_date, 
                        FundInfo.end_date
                    ).all()

                for fund_id, order_book_id, start_date, end_date in query_results:
                    if order_book_id not in fund_id_mapping:
                        fund_id_mapping[order_book_id] = []
                    fund_id_mapping[order_book_id].append(
                        {'fund_id': fund_id, 'start_date':start_date, 'end_date': end_date})

            except Exception as e:
                print('Failed fill get fund id mapping <err_msg> {}'.format(e))
                return None
                
        return fund_id_mapping