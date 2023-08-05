import pandas as pd
import numpy as np
from load_and_update_data.get_fund_data import DataLoader
import datetime
from sqlalchemy import create_engine

def tagging(x, default_name='symbol'):
    symbol = str(x[default_name])
    wind_class_II = str(x['wind_class_II'])
    struct = str(x['if_structured_fund'])
    if struct == '是':
        return
    
    if '沪深300' in symbol and wind_class_II in ['普通股票型基金', '增强指数型基金', '被动指数型']:
        return 'A股大盘'
    elif '中证500' in symbol and wind_class_II in ['普通股票型基金', '增强指数型基金', '被动指数型']:
        return 'A股中盘'
    elif '标普500' in symbol:
        return '美股大盘'
    elif '创业板' in symbol and wind_class_II in ['普通股票型基金', '增强指数型基金', '被动指数型']:
        return '创业板'
    elif '德国' in symbol:
        return '德国大盘'
    elif '日本' in symbol or '日经' in symbol:
        return '日本大盘'
    elif ('国债' in symbol or '利率' in symbol or '金融债' in symbol) and wind_class_II in ['短期纯债型基金', '中长期纯债型基金', '被动指数型债券基金']:
        return '利率债'
    elif ('信用' in symbol or '企债' in symbol or '企业债' in symbol) and wind_class_II in ['短期纯债型基金', '中长期纯债型基金', '被动指数型债券基金']:
        return '信用债'
    elif '黄金' in symbol:
        return '黄金'
    elif '原油' in symbol or '石油' in symbol or '油气' in symbol:
        return '原油'
    elif ('地产' in symbol or '金融' in symbol) and ('美国' not in symbol):
        return '房地产'

dl = DataLoader('huyunfan', 'Huyunfan123456')
fund_tb = dl.get_data('fundlist_wind', column_names=['fund_id', 'symbol', 'wind_class_II', 'if_structured_fund', 'benchmark'])
fund_tb['asset_type'] = fund_tb.apply(tagging, axis=1)
fund_tb = fund_tb.drop(columns=['symbol', 'wind_class_II', 'benchmark', 'if_structured_fund'])

sql = "select * from quant_data.fund_tag where `datetime` = '20200225'"
tag_data = dl.get_data_from_sql(sql)
tag_data.drop(columns=['asset_type'], inplace=True)
new_tags = tag_data.merge(fund_tb, how='left', on='fund_id')

new_tags['datetime'] = datetime.datetime.now().strftime('%Y%m%d')
# new_tags['datetime'] = '20200301'
engine = create_engine('mysql+pymysql://huangkejia:Huangkejia123456@fundinfo.cq1tbd5lkqzo.rds.cn-northwest-1.amazonaws.com.cn:3306/quant_data', pool_recycle=1)
new_tags.to_sql('fund_tag', engine, index=False, if_exists='append')
