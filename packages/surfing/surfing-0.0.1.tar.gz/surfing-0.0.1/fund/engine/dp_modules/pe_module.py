# 接受一个要更新的日期参数，从数据库拉取行业行业分类信息，每支股票最新的净利润，历史PE数据，计算每个行业的PE，合并到历史PE数据并计算百分位后，上传更新原来的数据库

import pandas as pd
import time
import math

from fund.data_engine.data_processor import DpModule
from fund.util.utility import Utility
from fund.data_engine.common import DataType
from fund.db.models import IndustryPE, StockLatestNetProfit

# 流程
# 1. 每个月初更新profit table

# 2. 读取industry list(股票的行业分类信息)
# 3. 读取profit table（最近年度净利润）
# 4. 读取当天股票市值（财报公布之后才对股本数据进行调节，而不对报告期（例如，半年报为06-30）至公布日期之间的数据进行覆盖更新）
# 5. PE计算,更新PEQ
# 6. 写入industry_pe 和 stock_latest_pe数据库

class PeDailyModule(DpModule):
    '''
    计算杠杆率、爆仓价格距离和风险敞口
    '''

    def __init__(self):
        DpModule.__init__(self)
        self._necessary_keys = [
            DataType.INDUSTRY_INFO,
            DataType.INDUSTRY_PE,
            DataType.STOCK_FINANCIAL_INDICATOR,
            DataType.STOCK_DAILY_VALUE,
            DataType.STOCK_ANNUAL_NET_PROFIT
        ]

    def get_latest_annual_net_profit(self, df_stock_financial_indicator, stock):
        latest_financial_df = df_stock_financial_indicator[(df_stock_financial_indicator['order_book_id'] == stock)][
                              -5:]
        eps_df = latest_financial_df['adjusted_net_profit'].values
        quarter = latest_financial_df['quarter'].values
        if eps_df.shape[0] == 0:
            return 0, quarter[-1]
        else:
            for i in range(eps_df.shape[0] - 1, 0, -1):
                if quarter[i][-1] == '4' or quarter[i][-1] == '3' or quarter[i][-1] == '2':
                    eps_df[i] -= eps_df[i - 1]
            if eps_df.shape[0] < 5:
                # print('[info] NewStock')
                return eps_df.sum() / (eps_df.shape[0]) * 4, quarter[-1]
            else:
                return eps_df[1:].sum(), quarter[-1]

    def _run(self, data_in):
        '''
        计算行业估值
        :param data_in: 输入数据字典，需包括如下几个 keys
         - INDUSTRY_INFO: 行业划分信息
         - INDUSTRY_PE: 行业历史市盈率
         - STOCK_FINANCIAL_INDICATOR: 股票财报
         - STOCK_DAILY_VALUE: 股票每日市值
         - STOCK_ANNUAL_NET_PROFIT: 股票年度净利润
        '''
        # Output dict
        output = {}
        output[DataType.UPDATE_INDUSTRY_PE] = []
        # Get multiple data
        if data_in[DataType.STOCK_DAILY_VALUE] == []:
            self._logger.warn(f'No daily stock valuation data get!')
            print('No daily get!')
            return output

        industry_stock_dict = {}
        ind_all_df = pd.DataFrame(data_in[DataType.INDUSTRY_INFO])
        for _, i in ind_all_df.iterrows():
            if i['industry_name'] not in industry_stock_dict:
                industry_stock_dict[i['industry_name']] = [i['order_book_id']]
            else:
                industry_stock_dict[i['industry_name']].append(i['order_book_id'])
        df_industry_pe = pd.DataFrame(data_in[DataType.INDUSTRY_PE])
        if data_in[DataType.STOCK_FINANCIAL_INDICATOR] != []:
            df_stock_financial_indicator = pd.DataFrame(data_in[DataType.STOCK_FINANCIAL_INDICATOR])
            update_eps = True
            output[DataType.UPDATE_STOCK_ANNUAL_NET_PROFIT] = []
        else:
            update_eps = False
            df_stock_annual_net_profit = pd.DataFrame(data_in[DataType.STOCK_ANNUAL_NET_PROFIT])
        df_stock_valuation_daily = pd.DataFrame(data_in[DataType.STOCK_DAILY_VALUE])

        date = df_stock_valuation_daily['date'].values[0]

        # 如果计算了当天的pe，则删除历史数据重新计算
        df_industry_pe.drop(df_industry_pe[(df_industry_pe['date'] == date)].index, inplace=True)

        # 新建股票最新年度净值表
        if update_eps:
            df_stock_annual_net_profit = pd.DataFrame(
                {'order_book_id': [], 'update_date': [], 'quarter': [], 'net_profit': []})
        df_stock_annual_net_profit.set_index('order_book_id', inplace=True)

        # define a bref table to search
        df_stock_valuation_daily['new_index'] = df_stock_valuation_daily.loc[:,
                                                'date'] + df_stock_valuation_daily.loc[:, 'order_book_id']
        # stock_daily_price_df_short.apply(lambda x: x.date + x.order_book_id,axis=1)
        df_stock_valuation_daily.set_index('new_index', inplace=True)

        # 遍历上证指数更新日期
        for industry in industry_stock_dict:
            # 1.跳过无意义的行业
            if industry == "未知":
                continue
            e_industry = 0
            p_industry = 0
            pe_industry = 0
            num_stock = 0
            for stock in industry_stock_dict[industry]:
                # 2. 判断行业股票财报是否完全,并在当天有更新
                try:
                    if update_eps:
                        net_profit, quarter = self.get_latest_annual_net_profit(df_stock_financial_indicator, stock)
                        output[DataType.UPDATE_STOCK_ANNUAL_NET_PROFIT].append(
                            StockLatestNetProfit(order_book_id=str(stock), update_date=str(date),
                                                 quarter=str(quarter), net_profit=float(net_profit)))
                    else:
                        net_profit = float(df_stock_annual_net_profit.loc[stock, :]['net_profit'])
                    stock_close = float(df_stock_valuation_daily.loc[date + stock, :]['market_cap_3'])
                except Exception as e:
                    # print('No_information', industry, date + stock)
                    pass
                else:
                    if not math.isnan(stock_close):
                        e_industry += float(net_profit)
                        p_industry += stock_close
                        num_stock += 1
            pe_industry = p_industry / e_industry if e_industry != 0 else float('inf')
            # 计算p/e百分位
            peq = (pd.to_numeric(
                df_industry_pe.loc[(df_industry_pe.industry_name == industry) & (df_industry_pe.P != 0), 'PE']).append(
                pd.Series(pe_industry), ignore_index=True).rank(
                pct=True) * 100).values[-1]
            output[DataType.UPDATE_INDUSTRY_PE].append(
                IndustryPE(industry_name=industry, num_stock=num_stock, date=date, P=float(p_industry),
                           E=float(e_industry), PE=float(pe_industry), PEQ=float(peq)))
        return output

if __name__=='__main__':
    from python.data_engine.data_loader import DataLoader
    dl = DataLoader()
    data_in = dl.load(date='20190201')
    pe_cal = PeDailyModule()
    result = pe_cal._run(data_in)
    print(result)
