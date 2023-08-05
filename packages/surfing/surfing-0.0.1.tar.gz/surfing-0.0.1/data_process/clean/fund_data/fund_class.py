from load_and_update_data.get_fund_data import DataLoader
from pprint import pprint
import pandas as pd
import numpy as np
from fund_indicators import fund_indicators
import pymysql
import sqlalchemy
from sqlalchemy import create_engine
pd.options.mode.chained_assignment = 'raise'

ACTIVE_RETURN = 0.1
TRACKING_ERROR = 0.1
FEE = 0.001

def find_indicator(type_name='',
                   active_ret=ACTIVE_RETURN,
                   alpha=0,
                   treynor=0,
                   mdd=0,
                   down_risk=0,
                   tracking_err=TRACKING_ERROR,
                   fee=0):
    if type_name == '普通股票型':
        return active_ret*0.25+alpha*0.25+treynor*0.25+mdd*0.15+down_risk*0.1
    elif type_name == '封闭式':
        return active_ret*0.20+alpha*0.30+treynor*0.25+mdd*0.15+down_risk*0.1
    elif type_name == '偏股混合型':
        return active_ret*0.25+alpha*0.20+treynor*0.3+mdd*0.15+down_risk*0.1
    elif type_name == '平衡混合型':
        return active_ret*0.25+alpha*0.20+treynor*0.3+mdd*0.15+down_risk*0.1
    elif type_name == '含股债券型':
        return active_ret*0.3+alpha*0.25+treynor*0.2+mdd*0.15+down_risk*0.1
    elif type_name == '被动指数型':
        return tracking_err*0.85 + fee*0.15
 
fund_tag = {
    '普通股票型基金'    : '普通股票型',
    '偏股混合型基金'    : '偏股混合型',
    '平衡混合型基金'    : '平衡混合型',
    '偏债混合型基金'    : '含股债券型',
    '被动指数型债券基金' : '被动指数型',
    '被动指数型基金'    : '被动指数型',
}

fund_keys = list(fund_tag.keys())
fund_class = {
  '普通股票型': [],
  '偏股混合型': [],
  '平衡混合型': [],
  '含股债券型': [], 
  '被动指数型': [],
}

fee_dic = {
    '150008' : 0.0122,
    '150009' : 0.0122,
}
  
username = 'huangkejia'
password = 'Huangkejia123456'
database = 'quant_data'
derivedbase = 'derived_data'
dl = DataLoader(username, password, database_name=database)
dl2 = DataLoader(username, password, database_name=derivedbase)
fund_tag_df = dl.get_data('fund_tag')
fund_indi = dl2.get_data('basic_fund_indicators')
fundlist = dl.get_data('fundlist_wind')[['order_book_id','symbol']].drop_duplicates(['order_book_id'],keep='last')
id_symbol_dic = fundlist.set_index('order_book_id').to_dict()['symbol']
id_base = list(id_symbol_dic.keys())
fund_indi['symbol'] = [id_symbol_dic[_] if _ in id_base else '*' for _ in fund_indi.order_book_id.tolist() ]
fund_indi.loc[fund_indi['order_book_id'].isin(['150008','150009']),'Fee_Rate'] = 0.0122

fund_tag_result = []
begin_date = '20170101'
end_date = '20191201'
for i in fund_tag_df.to_dict('records'):
    if i['end_date'] != '00000000' and  i['found_date'] < '20170101':
        continue
    if i['type_level_2'] in fund_keys:
        fund_tag_result.append([i['order_book_id'] , fund_tag[i['type_level_2']]])
date_list = sorted(list(set(fund_indi['datetime'])))


res = []
data_unvaild = []
for d in date_list:
    indi_d = fund_indi[fund_indi['datetime'] == d]
    for f in fund_tag_result:
        fund_id = f[0]
        type_name = f[1]
        
        # really bad fund
        if fund_id == '180002' and d == '20191231':
            continue
    
        data_d_f = indi_d[indi_d['order_book_id'] == fund_id]
        if data_d_f.empty:
            continue
        data_d_f = data_d_f.to_dict('records')[0]
        
        score_i = find_indicator(type_name=type_name,
                   alpha=data_d_f['Alpha'],
                   treynor=data_d_f['Treynor_Ratio'],
                   mdd=data_d_f['Max_DD'],
                   down_risk=data_d_f['Downside_Risk'],
                   fee=data_d_f['Fee_Rate'])
        
        data_d_f['Score'] = score_i  
        res.append(data_d_f)
        
result = pd.DataFrame(res)[['datetime','order_book_id','symbol','Alpha','Treynor_Ratio','Max_DD','Downside_Risk','Fee_Rate','Score']]
result['Score_100'] = 100*(result['Score']-result['Score'].min())/(result['Score'].max() - result['Score'].min())
engine = create_engine('mysql+pymysql://huangkejia:Huangkejia123456@fundinfo.cq1tbd5lkqzo.rds.cn-northwest-1.amazonaws.com.cn:3306/derived_data')
table_name = 'fund_score'
result.to_sql(table_name, engine, index=False)