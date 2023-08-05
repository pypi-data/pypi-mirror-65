#!/usr/bin/env python
# coding: utf-8
import numpy as np
import pandas as pd
import rqdatac as rq
from .EMQuantAPI_Python.python3.EmQuantAPI import *
import datetime
import json
import csv
from ..db.database import RawDatabaseConnector
from ..db.raw_models import *
from ..util.constant import STOCK_VALUATION_FACTORS, FUND_INDICATORS
from ..data_api.basic_new import BasicDataApi

class EmRawDataDownloader(object):

    def __init__(self):
        # ForceLogin
        # 取值0，当线上已存在该账户时，不强制登录
        # 取值1，当线上已存在该账户时，强制登录，将前一位在线用户踢下线
        options = "ForceLogin=1"
        loginResult = c.start(options, mainCallBack=self._main_callback)
        if(loginResult.ErrorCode != 0):
            print("EM login failed")
            exit()

        self._fund_ids = self._get_fund_ids()

    def _upload_raw(self, df, table_name, if_exists='append'):
        print(table_name)
        print(df)
        # df.to_sql(table_name, RawDatabaseConnector().get_engine(), index=False, if_exists=if_exists)

    def _get_fund_ids(self):
        fund_id_list = []
        with open('tag.csv') as csvfile:
            csvreader = csv.reader(csvfile)
            for row in csvreader:
                fund_id_list.append(f'{row[1][:-2]}.OF')
        print(fund_id_list)

        fund_id_str = ','.join(fund_id_list)
        return fund_id_str

    def _main_callback(self, quantdata):
        """
        mainCallback 是主回调函数，可捕捉连接错误
        该函数只有一个为c.EmQuantData类型的参数quantdata
        :param quantdata: c.EmQuantData
        """
        print (f"MainCallback: {quantdata}")

    def em_fund_nav(self, start_date, end_date):
        # TODO: compare date param with actual start_data, end_data of each fund, then get data
        df = c.csd(self._fund_ids, "ADJUSTEDNAV", start_date, end_date, "AdjustFlag=2,Ispandas=1")

        # self._upload_raw(df_all, EmFundNav.__table__.name)

    def em_index(self, start_date, end_date):
        # ----------------------
        # H11073.CSI,信用债
        # SPX.GI,标普500
        # GDAXI.GI,德国DAX
        # N225.GI,日经225
        # 000012.SH,利率债
        # 000300.SH,沪深300
        # 000905.SH,中证500
        # 399006.SZ,创业板
        # 801181.SWI,房地产开发申万
        # ----------------------
        # USDCNY.IB,美元兑人民币市询价,TODO: '''ErrorCode=10001012, ErrorMsg=insufficient user access, Data={}'''
        # JPYCNY.IB,日元兑人民币市询价,TODO: '''ErrorCode=10001012, ErrorMsg=insufficient user access, Data={}'''
        # EURCNY.IB,欧元兑人民币市询价,TODO: '''ErrorCode=10001012, ErrorMsg=insufficient user access, Data={}'''
        # ----------------------
        # AU0.SHF,沪金主力连续
        # BC.ICE,布伦特原油当月连续,TODO: always get None
        # ----------------------
        codes = ("H11073.CSI,SPX.GI,GDAXI.GI,N225.GI,000012.SH,000300.SH,000905.SH,399006.SZ,801181.SWI,"
            "USDCNY.IB,JPYCNY.IB,EURCNY.IB,"
            "AU0.SHF,BC.ICE")
        df = c.csd(codes, "CLOSE", start_date, end_date, "Ispandas=1")

        # self._upload_raw(df, EmIndexPrice.__table__.name)

    def download_all(self, start_date, end_date):
        self.em_fund_nav(start_date, end_date)
        # self.em_index(start_date, end_date)
