from fund.db.models import (IndexPrice,StockInfo,StockValuation,StockFinancialIndicator,StockLatestNetProfit,IndustryPE)
from fund.util.timer import Timer
from fund.util.logger import SurfingLogger
from fund.util.utility import Utility
from .database import QuantDatabaseConnector,DerivedDatabaseConnector
from .common import DataType

import json
import pandas as pd
import datetime
from sqlalchemy.sql import func
from collections import defaultdict

class DataLoader(object):
    '''
    DataLoader is used to load data from database to memory.
    (DB) -> DataLoader -> (Memory)
    '''

    DEFAULT_COMMISSION_CONF_FILE = '/shared/fof/config/sub_account.json'

    def __init__(self):
        '''
        Initialization
        '''
        self._logger = SurfingLogger.get_logger(type(self).__name__)
    def load(self, start_time=None, end_time=None, date=None, internal_data=None):
        '''
        Main function of DataLoader, to be called by DataEngine.
        :param start_time: start time for data loading
        :param end_time: end time for data loading
        :param date: date for daily update
        :return output: dict, {DataType -> data}
        '''
        output = {}
        output[DataType.INDUSTRY_INFO] = []
        output[DataType.INDUSTRY_PE] = []
        output[DataType.STOCK_FINANCIAL_INDICATOR] = []
        output[DataType.STOCK_DAILY_VALUE] = []
        output[DataType.STOCK_ANNUAL_NET_PROFIT] = []

        # Load industry division information
        industry_division = self._load_industry_info_data()
        if industry_division is not None:
            output[DataType.INDUSTRY_INFO] = industry_division
        self._logger.debug('Loaded industry division info')

        # Load stock pe ratio
        industry_pe = self._load_industry_pe()
        if industry_pe is not None:
            output[DataType.INDUSTRY_PE] = industry_pe
        self._logger.debug('Loaded industry pe ratio')


        if date is None:
            date = Timer.datetime()

        if date[-2:] == '01':
            # Load stock financial data
            stock_financial_data = self._load_stock_financial_indicator(date)
            if stock_financial_data is not None:
                output[DataType.STOCK_FINANCIAL_INDICATOR] = stock_financial_data
            self._logger.debug('Loaded stock financial data')

        else:
            # Load stock annual net profit
            stock_annual_net_profit = self._load_stock_latest_net_profit()
            if stock_annual_net_profit is not None:
                output[DataType.STOCK_ANNUAL_NET_PROFIT] = stock_annual_net_profit
            self._logger.debug('Loaded stock annual net profit')

        # Load stock daily value
        stock_daily_value = self._load_stock_valuation(date)
        if stock_daily_value is not None:
            output[DataType.STOCK_DAILY_VALUE] = stock_daily_value
        self._logger.debug('Loaded stock daily value')


        return output

    def _load_index_price_data_to_fund_indicators(self,start, end, order_book_id):
        '''
        获取某个指数一段时间内的价格
        :return: 某个指数一段时间内的价格, 若不存在为 None
        '''
        with QuantDatabaseConnector().managed_session() as derived_session:
            try:
                latest_record = derived_session.query(IndexPrice.ret,IndexPrice.date,IndexPrice.close).filter(
                    IndexPrice.date>= start, IndexPrice.date<=end, IndexPrice.order_book_id==order_book_id
                ).all()
                return latest_record
            except Exception as e:
                self._logger.error('获取某个指数一段时间内的价格失败 <err_msg>{}'.format(e))
        return None


    def _load_stock_valuation(self, date):
        '''
        获取某个时间点所有股票的市值
        :return: 某天所有股票的市值, 若不存在为 None
        '''
        with QuantDatabaseConnector().managed_session() as quant_session:
            try:
                latest_record = quant_session.query(StockValuation.order_book_id, StockValuation.date, StockValuation.market_cap_3).filter(
                    StockValuation.date == date
                ).all()
                return latest_record
            except Exception as e:
                self._logger.error('获取某个时间点所有股票的市值 <err_msg>{}'.format(e))
        return None


    def _load_industry_info_data(self):
        '''
        获取股票的行业分类
        :return: 全部股票的行业分类, 若不存在为 None
        '''
        with QuantDatabaseConnector().managed_session() as derived_session:
            try:
                latest_record = derived_session.query(StockInfo.industry_name,StockInfo.order_book_id).all()
                return latest_record
            except Exception as e:
                self._logger.error('获取获取股票的行业分类失败 <err_msg>{}'.format(e))
        return None

    def _load_industry_pe(self):
        '''
        获取行业的市盈率
        :return: 全部行业的名称和2015年来的历史市盈率, 若不存在为 None
        '''
        with DerivedDatabaseConnector().managed_session() as derived_session:
            try:
                latest_record = derived_session.query(IndustryPE.industry_name,IndustryPE.PE,IndustryPE.date,IndustryPE.P).all()
                #print(latest_record)
                return latest_record
            except Exception as e:
                self._logger.error('获取行业的市盈率 <err_msg>{}'.format(e))
        return None

    def _load_stock_latest_net_profit(self):
        '''
        获取股票最近年度净利润
        :return: 全部股票最近年度净利润, 若不存在为 None
        '''
        with DerivedDatabaseConnector().managed_session() as derived_session:
            try:
                latest_record = derived_session.query(StockLatestNetProfit.order_book_id, StockLatestNetProfit.update_date,StockLatestNetProfit.quarter, StockLatestNetProfit.net_profit).all()
                return latest_record
            except Exception as e:
                self._logger.error('获取股票最近年度净利润 <err_msg>{}'.format(e))
        return None

    def _load_stock_financial_indicator(self,date):
        '''
        获取股票最近财报
        :return: 全部股票最近财报, 若不存在为 None
        '''

        query_year = date[:4]
        pre_query_year = str(int(query_year)-2)
        with QuantDatabaseConnector().managed_session() as quant_session:
            try:
                latest_record = quant_session.query(StockFinancialIndicator.quarter, StockFinancialIndicator.order_book_id, StockFinancialIndicator.adjusted_net_profit,StockFinancialIndicator.announce_date).filter(
                    StockFinancialIndicator.quarter <= query_year, StockFinancialIndicator.quarter >=pre_query_year
                ).all()
                return latest_record
            except Exception as e:
                self._logger.error('获取股票最近财报 <err_msg>{}'.format(e))
        return None



if  __name__=='__main__':
    a = DataLoader()
    b = a.load(date='20190123')




