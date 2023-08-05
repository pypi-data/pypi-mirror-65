import pandas as pd
import numpy as np
from datetime import datetime
from datetime import date
import json
from fund.db.database import BasicDatabaseConnector,DerivedDatabaseConnector,RawDatabaseConnector
from fund.data_api.raw import get_raw_cm_index_price_df, get_cxindex_index_price_df, get_yahoo_index_price_df, get_rq_index_price_df,get_rq_index_weight,get_rq_stock_valuation,get_stock_fin_fac
from fund.data_api.basic import get_index_info, get_trading_day_list, get_index_price, get_fund_ret,get_fund_info,get_fund_nav
import rqdatac as rq
rq.init()

'''
当前只算来 hs300 csi500 pe 百分位
其他算法可以参考米筐公式 下面所有数可以通过rq.get_factor获得

pb_ratio_lf = market_cap_3 / equity_parent_company_mrq_0
pe_ratio_ttm = market_cap_3 / net_profit_parent_company_ttm_0
peg_ratio_ttm = pe_ratio_ttm / ((net_profit_ttm_0 - net_profit_ttm_1) / net_profit_ttm_1)
dividend_yield_ttm = dividend_per_share / close_price
return_on_equity_ttm = net_profit_parent_company_ttm_0 * 2 / (ma_0 + equity_parent_company_ttm_1)
第一遍算错，用了未来函数，第二次在第一次基础上更改
'''


index_df = get_index_info()
index_df = index_df[index_df['index_id'].isin(['hs300','csi500'])]
trade_list = rq.get_trading_dates(date(2005,1,1), date(2020,3,30))
trade_list = [ _ for _ in trade_list if _ > date(2005,4,15)]
result = {}
for index_o in index_df.order_book_id.tolist():
    result[index_o] = {}
    for d in trade_list:
        res_i = rq.index_weights(index_o, d)
        result[index_o][d] = res_i
stock_list = []
for index_i in result:
    print(index_i)
    for d in result[index_i]:
        stock_list.extend(result[index_i][d].index.tolist())
stock_list = list(set(stock_list))  
stock_cap = rq.get_factor(stock_list, 'market_cap_3',trade_list[0],trade_list[-1])
stock_profit = rq.get_factor(stock_list, 'net_profit_parent_company_ttm_0',trade_list[0],trade_list[-1])

res = []
for index_i in result:
    for d in result[index_i]:
        stock_list_i = result[index_i][d].index.tolist()
        p = stock_cap.loc[d,stock_list_i].sum() 
        e = stock_profit.loc[d,stock_list_i].sum() 
        res.append({
            'index_id' : index_i,
            'datetime' : d,
            'pe_ratio_ttm'    : p / e ,
        })    
index_val = pd.DataFrame(res)
res = []
for index_i in index_df['order_book_id'].to_list():
    index_val_i  = index_val[index_val['index_id'] == index_i]
    index_val_i.loc[:,'pe_pct'] = index_val_i['pe_ratio_ttm'].rank(pct=True).copy()
    res.append(index_val_i)
index_df = pd.concat(res)  

index_list = ['000905.XSHG','000300.XSHG']
pctrank = lambda x: pd.Series(x).rank(pct=True).iloc[-1]
res = []
for index_i in index_list:
    df_index = index_df[index_df['index_id'] == index_i]
    df_index.loc[:,'pe_pct'] = df_index.set_index('datetime')[['pe_ratio_ttm']].rolling(242*5).apply(pctrank, raw=True).values
    res.append(df_index)

df = pd.concat(res).drop(['id'], axis = 1)

df.to_sql('index_valpct', RawDatabaseConnector().get_engine(), index=False, if_exists='append')