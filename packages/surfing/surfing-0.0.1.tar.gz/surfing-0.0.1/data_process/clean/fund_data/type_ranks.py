from load_and_update_data.get_fund_data import DataLoader
import numpy as np
import pandas as pd

def get_nearest_season(check_date):
        year = check_date[:4]
        mon = check_date[4:]
        
        if mon < '0331': 
            return str(int(year) - 1) + '1231'
        elif mon < '0630':
            return year + '0331'        
        elif mon < '0930':
            return year + '0630'
        elif mon < '1231':
            return year + '0930'
        else:
            return year + '1231'

def type_ranks(score_name, typelist, check_date, dl=None):
    if dl is None:
        dl = DataLoader('huyunfan', 'Huyunfan123456', database_name='derived_data')
    
    strlist = []
    for fund_type in typelist:
        strlist.append("'" + fund_type + "'")
    sql_list = ','.join(strlist)
    sql_date = get_nearest_season(check_date)
    sql = "SELECT * FROM derived_data.fund_tag_score_backup where `datetime` = '{}' and score_name = '{}' and `tag_name` in ({}) and score is not null;".format(sql_date, score_name, sql_list)
    score_df = dl.get_data_from_sql(sql).sort_values(by=['tag_name', 'score'], ascending=False)

    return score_df

# def type_ranks(typelist, check_date, dl=None):
#     if dl is None:
#         dl = DataLoader('huyunfan', 'Huyunfan123456')
    
#     strlist = []
#     for fund_type in typelist:
#         strlist.append("'" + fund_type + "'")
#     sql_list = ','.join(strlist)
#     sql = "SELECT * FROM quant_data.fund_tag where `datetime` = '20200219' and `asset_type` in ({});".format(sql_list)
#     sql_date = get_nearest_season(check_date)
#     sql_score = "SELECT * FROM derived_data.fund_score where `datetime`='{}';".format(sql_date)

#     id_df = dl.get_data_from_sql(sql).drop(columns=['transition', 'symbol', 'found_date', 'end_date', 'type_level_1', 'type_level_2', 'datetime'])
#     score_df = dl.get_data_from_sql(sql_score)

#     final_tb = id_df.merge(score_df, how='left', on='order_book_id')
#     final_tb_full = final_tb[~(pd.isnull(final_tb['Alpha']))]
#     final_tb_full
#     sorted_tb = final_tb_full.sort_values(by=['asset_type', 'Score'], ascending=False, ignore_index=True)
#     return sorted_tb, id_df
       