from load_and_update_data.get_fund_data import DataLoader
import pandas as pd
import numpy as np
from sqlalchemy import create_engine

username = 'huangkejia'
password = 'Huangkejia123456'
database = 'quant_data'
dl = DataLoader(username, password, database_name=database)
engine = create_engine('mysql+pymysql://huangkejia:Huangkejia123456@fundinfo.cq1tbd5lkqzo.rds.cn-northwest-1.amazonaws.com.cn:3306/derived_data')

index_data = dl.get_data('active_asset_index').set_index('date').dropna().astype(float)
res = index_data.corr(method='pearson')
res['index'] = res.index
res.to_sql('index_corr', engine, index=False)