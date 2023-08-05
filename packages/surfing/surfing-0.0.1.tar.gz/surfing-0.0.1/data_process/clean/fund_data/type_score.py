from load_and_update_data.get_fund_data import DataLoader
from sqlalchemy import create_engine
import numpy as np
import pandas as pd
import datetime

tb_v = 6

def get_date_str(year, quarter):
        
        if quarter == 1:
            q_str = '0331'
        elif quarter == 2:
            q_str = '0630'
        elif quarter == 3:
            q_str = '0930'
        elif quarter == 4:
            q_str = '1231'
        else:
            return None
        
        if year is not None:
            return str(year) + q_str
        return q_str

def quarter_upload(start_year, start_quarter, end_year, end_quarter, interval, version, dl=None, engine=None):
        cur_year = start_year
        cur_quarter = start_quarter
        if engine is None:
            engine = create_engine('mysql+pymysql://zhangyunfan:Zhangyunfan123456@fundinfo.cq1tbd5lkqzo.rds.cn-northwest-1.amazonaws.com.cn:3306/derived_data', pool_recycle=1)
        if dl is None:
            dl = DataLoader('huyunfan', 'Huyunfan123456')
        
        while cur_year <= end_year and cur_quarter <= end_quarter:
            
            print('calcalate:' + str(cur_year) + 'q' + str(cur_quarter))
            date_str = get_date_str(cur_year, cur_quarter)
            pre_date_str = get_date_str(cur_year - interval, cur_quarter)
            score_df = type_score(pre_date_str, date_str, dl, interval, version)
            print('upload')
            score_df.to_sql('fund_tag_score', engine, index=False, if_exists='append')
            cur_quarter += 1
            if cur_quarter > 4:
                cur_year += 1
                cur_quarter = 1

def type_score(pre_date, tag_date, dl, interval, version):
    sql = "SELECT * FROM quant_data.fund_tag where `datetime` = '20200301' and `asset_type` is not null;"
    id_df = dl.get_data_from_sql(sql).drop(columns=['transition', 'type_level_1', 'type_level_2', 'datetime', 'order_book_id'])
    # print(id_df['asset_type'].value_counts())

    sql_indicators = "SELECT * FROM derived_data.fund_indicator where `datetime`='{}' and timespan={};".format(tag_date, interval)
    indicators_df = dl.get_data_from_sql(sql_indicators)

    merge_1 = id_df.merge(indicators_df, how='inner', on='fund_id')
    merge_1['track_error'] = merge_1['track_error'].astype(float)

    merge_2 = merge_1
    merge_2['beta'] = merge_2['beta'].astype(float)
    merge_2['alpha'] = merge_2['alpha'].astype(float)
    merge_2['fee_rate'] = merge_2['fee_rate'].astype(float)
    merge_2['track_error'] =merge_2['track_error'].astype(float)

    group_tag = merge_1.groupby('asset_type')[['beta', 'alpha', 'fee_rate', 'track_error']]
    group_mean = group_tag.mean()
    group_std = group_tag.std()
    
    rule_tb = pd.read_csv('weight.csv')
    
    def score_rules(x):
        cur_type = str(x['asset_type'])
        cur_rule = rule_tb[(rule_tb['Type'] == cur_type) & (rule_tb['Version'] == version)]

        try:
            alpha = cur_rule['Alpha'].values[0]
            beta = cur_rule['Beta'].values[0]
            tr = cur_rule['Track_error'].values[0]
            fr = cur_rule['Fee_rate'].values[0]
        except:
            return np.nan
        

        try:
            alv = float(x['alpha'])
            bev = float(x['beta'])
            trv = float(x['track_error'])
            frv = float(x['fee_rate'])
        except:
            return np.nan
        
        alv = (alv - group_mean.loc[cur_type, 'alpha']) / alv - group_std.loc[cur_type, 'alpha']
        bev = (bev - group_mean.loc[cur_type, 'beta']) / bev - group_std.loc[cur_type, 'beta']
        trv = (trv - group_mean.loc[cur_type, 'track_error']) / trv - group_std.loc[cur_type, 'track_error']
        frv = (frv - group_mean.loc[cur_type, 'fee_rate']) / frv - group_std.loc[cur_type, 'fee_rate']

        if beta != -11:
            result = alpha * alv + beta * bev + tr * trv + fr * frv
        elif beta == -11:
            result = alpha * alv + abs(1 - bev) * -0.2 + tr * trv + fr * frv

        return result
    
    def check_date(x):
        found_date = str(x['found_date'])
        end_date = str(x['end_date'])

        if found_date <= pre_date:
            if end_date >= tag_date or end_date == '00000000':
                return 1
        
        return 0

    merge_2['score'] = merge_2.apply(score_rules, axis=1)
    merge_2['is_full'] = merge_2.apply(check_date, axis=1)
    merge_2['score_name'] = '大类资产评级v1'
    # merge_2['version'] = tb_v
    merge_2['timespan'] = interval
    merge_2.rename(columns={'asset_type':'tag_name'}, inplace=True)
    final = merge_2.filter(items=['fund_id', 'score_name', 'tag_name', 'score', 'datetime', 'beta', 
    'timespan', 'symbol', 'found_date', 'end_date', 'is_full'])
    final.drop_duplicates(['fund_id', 'datetime'], inplace=True)
    final_full = final[~final['score'].isnull()]

    return final_full

if __name__ == '__main__':
    quarter_upload(2013, 1, 2019, 4, 3, 4)

