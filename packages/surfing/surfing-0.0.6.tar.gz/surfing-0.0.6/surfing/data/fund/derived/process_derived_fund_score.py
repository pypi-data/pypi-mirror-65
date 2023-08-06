import numpy as np
import pandas as pd
import datetime
from datetime import date
from pyfinance.ols import PandasRollingOLS
from fund.db.database import BasicDatabaseConnector,DerivedDatabaseConnector
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score
from fund.data_api.basic import get_index_info, get_trading_day_list, get_index_price, get_fund_ret,get_fund_info,get_fund_nav
from fund.data_api.derived import get_fund_nav_adjusted_nv, get_index_benchmark_data,get_fund_list,get_fund_fee,get_fund_asset,get_fund_indicator


class SWElm:

    def __init__(self,alpha=0,beta=0,fee_rate=0,track_err=0,tag_method=None):
        self.alpha = alpha
        self.beta = beta
        self.fee_rate = fee_rate
        self.track_err = track_err
        self.tag_method = tag_method

def get_score(r,m):
    if m == 1: # 如果当前该资产只有一只基金，选吧
        return 1
    else:
        alv = (r.alpha - avg.alpha) / std.alpha
        bev = (r.beta   -avg.beta) / std.beta
        trv = (r.track_err - avg.track_err) /std.track_err
        frv = (r.fee_rate  - avg.fee_rate) / std.fee_rate
        m = score_dict[r.asset_type]
        result = m.alpha * alv + m.beta * abs(1-bev) + m.track_err * trv + m.fee_rate * frv
    return result        
        
def check_fund_number(fund_indicator):
    d_l= len(list(set(fund_indicator['datetime'].tolist())))
    tag_list  = list(set(fund_indicator['asset_type'].tolist()))
    for t in tag_list:
        l = fund_indicator[fund_indicator['asset_type'] == t].shape[0]
        print(t, l, l/d_l)    

score_dict = {}
tag_method = 'm0'

score_dict['A股大盘'] = SWElm(alpha=0.6, beta=-0.2, fee_rate = -0.2,tag_method=tag_method)
score_dict['A股中盘'] = SWElm(alpha=0.6, beta=-0.2, fee_rate = -0.2,tag_method=tag_method)
score_dict['创业板'] = SWElm(alpha=0.6, beta=-0.2, fee_rate = -0.2,tag_method=tag_method)
score_dict['美股大盘'] = SWElm(fee_rate = -0.2,track_err=-0.8,tag_method=tag_method)
score_dict['德国大盘'] = SWElm(fee_rate = -0.2,track_err=-0.8,tag_method=tag_method)
score_dict['日本大盘'] = SWElm(fee_rate = -0.2,track_err=-0.8,tag_method=tag_method)
score_dict['利率债'] = SWElm(alpha=0.2, fee_rate = -0.2,track_err=-0.6,tag_method=tag_method)
score_dict['信用债'] = SWElm(alpha=0.2, fee_rate = -0.2,track_err=-0.8,tag_method=tag_method)
score_dict['黄金'] = SWElm(alpha=0.2, fee_rate = -0.2,track_err=-0.8,tag_method=tag_method)
score_dict['原油'] = SWElm(alpha=0.2, fee_rate = -0.2,track_err=-0.8,tag_method=tag_method)
score_dict['房地产'] = SWElm(alpha=0.2, fee_rate = -0.2,track_err=-0.8,tag_method=tag_method)


fund_info = get_fund_info()
fund_info = fund_info[fund_info['asset_type'] != 'null']
asset_type = {i['fund_id'] : i['asset_type'] for i in fund_info.to_dict('records')}
fund_list = fund_info['fund_id'].to_list()
fund_indicator = get_fund_indicator(fund_list)
fund_indicator['asset_type'] = fund_indicator['fund_id'].map(lambda x : asset_type[x] )
fund_indicator['fee_rate'] = fund_indicator['fee_rate']

tag_list = list(score_dict.keys())
date_list = sorted(list(set(fund_indicator['datetime'].tolist())))
result = []
# 各资产日均基金数 
# 信用债 A股中盘 创业板 利率债 美股大盘 原油 德国大盘 A股大盘 房地产 黄金
#  35   19       8     12    3      6     1     40     23    11  
# 对于个数少的类别，筛选条件不严格

for d in date_list: 
    fid = fund_indicator[fund_indicator['datetime'] ==  d].copy()
    for t in tag_list:
        fitd = fid[fid['asset_type'] == t].copy()
        if fitd.shape[0] == 0:
            continue
        if t in ['创业板', '利率债', '美股大盘', '原油', '德国大盘', '黄金']:
            pass 
        elif t in ['信用债','A股中盘', 'A股大盘','房地产']:
            avg = fitd.mean()
            std = fitd.std()
            con1 = fitd.beta > (avg - std).beta
            con2 = fitd.beta < (avg + std).beta
            con3 = fitd.track_err > (avg - std).track_err
            fitd = fitd[con1 & con2 & con3].copy()
            if fitd.shape[0] < 5:
                continue
        avg = fitd.mean()
        std = fitd.std()
        result_i = []
        num = fitd.shape[0] 
        for i,r in fitd.iterrows():
            res  = get_score(r, num)
            r = r.to_dict()
            r['score'] = res
            result_i.append(r)
        df_i = pd.DataFrame(result_i)
        # TODO if df.shape[0] == 1: if df.shape[0] df.std = nan, np.std(df) = 0 
        # 
        avg = df_i['score'].mean()  
        std = df_i['score'].std()  
        con = (avg - std) < df_i['score']
        df_i = df_i[con]        
        df_i['score']  = (df_i['score']  - df_i['score'].min() )/ (df_i['score'].max() - df_i['score'].min())
        result.append(df_i.copy())

score_df = pd.concat(result)

fd_dic = {r.fund_id : {'start': r.start_date, 'end': r.end_date} for i, r in fund_info.iterrows()}
is_full = [r.datetime < fd_dic[r.fund_id]['end'] and r.datetime > fd_dic[r.fund_id]['start'] for i, r in score_df.iterrows()] 
score_df['is_full'] =  [int(_) for _ in is_full]
score_df = score_df.drop(['alpha','beta','fee_rate','track_err'] ,axis = 1)
name_dict = {
    'asset_type':'tag_name',
    'datetime':'datetime',
    'fund_id':'fund_id',
    'score':'score',
    'is_full':'is_full',
}
score_df = score_df.rename(columns=name_dict)
score_df.loc[:,'tag_type'] = 1 # 1 '大类资产评分'
score_df.loc[:,'tag_method'] = tag_method
score_df.loc[:,'score_method'] = 1 #'去一倍std beta 去一倍上界track_err 去一倍score score 0，1化 不同资产根据基金数决定筛选条件'
score_df.loc[:,'update_time'] = datetime.datetime.now()
score_df = score_df.replace(np.inf, np.nan)
score_df = score_df.replace(-np.inf, np.nan)
score_df = score_df.dropna()        
name_dict = {r.fund_id : r.desc_name for i,r in fund_info.iterrows()}      
score_df['desc_name'] = score_df['fund_id'].map(lambda x : name_dict[x])
score_df.to_sql('fund_score', DerivedDatabaseConnector().get_engine(), index=False, if_exists='append') 