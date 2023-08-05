
from load_and_update_data.get_fund_data import DataLoader



# two database
dl = DataLoader(username, password, database_name=database)
dl2 = DataLoader(username, password, database_name=derivedbase)

# display_result.py
dl.get_data('fundlist_wind', column_names=['symbol'], select_columns=['fund_id'], aim_values=[fund_id], operator=['=']).values.flatten()[0]
dl.get_data('index_info', column_names=['symbol'], select_columns=['order_book_id'], aim_values=[index_id], operator=['=']).values.flatten()[0]


# fund_backtest
dl.get_data('active_asset_index').set_index('date').drop(['标普500人民币','德标30人民币','日经225人民币'],axis=1).dropna().astype(float)
dl.get_data('fund_fee_info', column_names=['manage_fee','fund_id','trustee_fee']).set_index('fund_id')
dl.get_data('nav', column_names=['adjusted_net_value','subscribe_status','redeem_status','datetime','fund_id'],
                                   select_columns = ['datetime','datetime','fund_id'],
                                   aim_values=[self.switch_date[0], self.switch_date[-1], fund_i], 
                                   operator=['>=', '<=', '='])

#fund_class
dl.get_data('fund_tag')
dl.get_data('basic_fund_indicators')
dl.get_data('fundlist_wind')[['order_book_id','symbol']].drop_duplicates(['order_book_id'],keep='last')

# fund_holdings
dl.get_data('holdings', 
                        column_names=['order_book_id','share_order_book_id','type','weight','category','release_date'],
                        aim_values=[self.start_date, self.end_date], 
                        select_columns=['release_date', 'release_date'],
                        operator=['>=', '<=']) 

dl.get_data('stock_valuation', 
                        column_names=['market_cap_2', 'date', 'order_book_id'],
                        aim_values=[self.start_date, self.end_date], 
                        select_columns=['date', 'date'],
                        operator=['>=', '<=']) 


# fund_indicators

dl.get_data('index_price', column_names=['date'], 
                        select_columns=['date', 'date', 'order_book_id'], 
                        aim_values=[self.previous_date, end_date, self.market_index_id], 
                        operator=['>=', '<=', '=']).sort_values(by=['date'], ignore_index=True, ascending=True)

dl.get_data('nav', column_names=['change_rate', 'datetime', 'adjusted_net_value'], 
                        select_columns=['datetime', 'datetime', 'fund_id'], 
                        aim_values=[self.previous_date, end_date, fund_id], 
                        operator=['>=', '<=', '='])

dl.get_data('index_price', column_names=['ret', 'date', 'close'], 
                                    select_columns=['date', 'date', 'order_book_id'], 
                                    aim_values=[self.previous_date, end_date, self.market_index_id], 
                                    operator=['>=', '<=', '='])
                    
dl.get_data('fundlist_wind', column_names=['fund_id', 'found_date', 'end_date'], 
                       select_columns=['order_book_id'], 
                       aim_values=[miquant_id], 
                       operator=['='])
dl.get_data('nav', column_names=['change_rate', 'datetime'], 
                        select_columns=['datetime', 'datetime', 'fund_id'], 
                        aim_values=[start_date, end_date, fund_id], 
                        operator=['>=', '<=', '='])

dl.get_data('index_price', column_names=['ret', 'date'], 
                                select_columns=['date', 'date', 'order_book_id'], 
                                aim_values=[pre_date, start_date, self.market_index_id], 
                                operator=['>=', '<=', '='])

dl.get_data('nav', column_names=['change_rate', 'datetime'], 
                        select_columns=['datetime', 'datetime', 'fund_id'], 
                        aim_values=[pre_date, end_date, fund_id], 
                        operator=['>=', '<=', '='])

dl.get_data('nav', column_names=['change_rate', 'datetime'], 
                                select_columns=['datetime', 'datetime', 'fund_id'], 
                                aim_values=[start_date, end_date, fund_id], 
                                operator=['>=', '<=', '='])
dl.get_data('index_price', column_names=['ret', 'date'], 
                                        select_columns=['date', 'date', 'order_book_id'], 
                                        aim_values=[start_date, end_date, self.market_index_id], 
                                        operator=['>=', '<=', '='])

dl.get_data('nav', column_names=['adjusted_net_value', 'datetime'], 
                        select_columns=['datetime', 'datetime', 'fund_id'], 
                        aim_values=[start_date, end_date, fund_id], 
                        operator=['>=', '<=', '=']).sort_values(by=['datetime'], ignore_index=True, ascending=True)

dl.get_data('nav', column_names=['change_rate', 'datetime'], 
                        select_columns=['datetime', 'datetime', 'fund_id'], 
                        aim_values=[start_date, end_date, fund_id], 
                        operator=['>=', '<=', '=']).sort_values(by=['datetime'], ignore_index=True, ascending=True)

dl.get_data('nav', column_names=['adjusted_net_value', 'datetime'], 
                        select_columns=['datetime', 'datetime', 'fund_id'], 
                        aim_values=[start_date, end_date, fund_id], 
                        operator=['>=', '<=', '=']).sort_values(by=['datetime'], ignore_index=True, ascending=True)

dl.get_data('fund_fee_info', column_names=['manage_fee', 'trustee_fee'], 
                       select_columns=['fund_id'], 
                       aim_values=[fund_id], 
                       operator=['='])

#index_indicator
dl.get_data('index_price', column_names=['ret', 'date', 'close'], 
                            select_columns=['date', 'date', 'order_book_id'], 
                            aim_values=[self.previous_date, end_date, self.index_id], 
                            operator=['>=', '<=', '='])
dl.get_data('index_price', column_names=['close', 'date'], 
                                        select_columns=['date', 'date', 'order_book_id'], 
                                        aim_values=[start_date, end_date, self.index_id], 
                                        operator=['>=', '<=', '=']).sort_values(by=['date'], ignore_index=True, ascending=True)
dl.get_data('index_price', column_names=['ret', 'date'], 
                                        select_columns=['date', 'date', 'order_book_id'], 
                                        aim_values=[start_date, end_date, self.index_id], 
                                        operator=['>=', '<=', '=']).sort_values(by=['date'], ignore_index=True, ascending=True)

#indicators_uploader
dl.get_data('nav', column_names=['change_rate', 'datetime', 'adjusted_net_value', 'fund_id'], 
                            select_columns=['datetime', 'datetime'], 
                            aim_values=[data_date_s, data_date_e], 
                            operator=['>=', '<=']).sort_values(by=['datetime'], ignore_index=True, ascending=True)

dl.get_data('index_price', column_names=['ret', 'date', 'close'], 
                                    select_columns=['date', 'date', 'order_book_id'], 
                                    aim_values=[data_date_s, data_date_e, self.market_index_id], 
                                    operator=['>=', '<=', '=']).sort_values(by=['date'], ignore_index=True, ascending=True)
                            
# stock_factor_barra
self.data_size = self.dl.get_data('stock_valuation', 
                                column_names=['market_cap_2', 'date', 'order_book_id'],
                                aim_values=[self.start_date, self.end_date], 
                                select_columns=['date', 'date'],
                                operator=['>=', '<=']) 
self.data_value = self.dl.get_data('stock_valuation', 
                                column_names=['ep_ratio_ttm', 'date', 'order_book_id'],
                                aim_values=[self.start_date, self.end_date], 
                                select_columns=['date', 'date'],
                                operator=['>=', '<=']) 
self.data_turnover = self.dl.get_data('stock_turnover', 
                                column_names=['year', 'date', 'order_book_id'],
                                aim_values=[self.start_date, self.end_date], 
                                select_columns=['date', 'date'],
                                operator=['>=', '<='])
self.data_quality = self.dl.get_data('stock_financial_indicator',
                                column_names=['order_book_id','quarter','return_on_equity'],
                                aim_values=[self.start_date_q, self.end_date_q], 
                                select_columns=['quarter', 'quarter'],
                                operator=['>=', '<='])

self.data_hs300_ret = self.dl.get_data('index_price', column_names=['ret', 'date', 'close'], 
                        select_columns=['date', 'date', 'order_book_id'], 
                        aim_values=[self.start_date, end_date, self.market_index_id], 
                        operator=['>=', '<=', '='])

self.data_quality = self.dl.get_data('stock_financial_indicator',
                                column_names=['order_book_id','quarter','return_on_equity'],
                                aim_values=[self.start_date_q, self.end_date_q], 
                                select_columns=['quarter', 'quarter'],
                                operator=['>=', '<='])
self.data_leverage = self.dl.get_data('stock_balance_sheet',
                                        column_names = ['order_book_id','quarter','total_assets','total_equity'],
                                        aim_values=[self.start_date_q, self.end_date_q], 
                                        select_columns=['quarter', 'quarter'],
                                        operator=['>=', '<='])
self.data_ret = self.dl.get_data('stock_daily_price',
                                                column_names=['order_book_id','date','ret'],
                                                aim_values=[self.start_date, self.end_date], 
                                                select_columns=['date', 'date'],
                                                operator=['>=', '<='])

# tagging_type
dl.get_data('fundlist_wind', column_names=['fund_id', 'symbol', 'wind_class_II', 'if_structured_fund', 'benchmark'])

sql = "select * from quant_data.fund_tag where `datetime` = '20200225'"
tag_data = dl.get_data_from_sql(sql)

# track error
sql = 'select fund_id, asset_type from quant_data.fund_tag where asset_type is not null'
            self.fund_df = self.dl.get_data_from_sql(sql)

sql = "select fund_id, asset_type from quant_data.fund_tag \
            where fund_id in ({}) and asset_type is not null".format(strlist)
            self.fund_df = self.dl.get_data_from_sql(sql)

sql_price = "select change_rate, `datetime`, fund_id from quant_data.nav \
        where fund_id in ({}) and `datetime`>={} and `datetime`<={}".format(str_fund, data_date_s, data_date_e)
        self.fund_price = self.dl.get_data_from_sql(sql_price)

sql_index = "select * from quant_data.index_ret where `date`>={} and `date`<={}".format(data_date_s, data_date_e)
        self.index_df = self.dl.get_data_from_sql(sql_index)


#type_ranks
sql = "SELECT * FROM derived_data.fund_tag_score where `datetime` = '{}' and score_name = '{}' and `tag_name` in ({}) and score is not null;".format(sql_date, score_name, sql_list)
    score_df = dl.get_data_from_sql(sql).sort_values(by=['tag_name', 'score'], ascending=False)


#type_score
sql = "SELECT * FROM quant_data.fund_tag where `datetime` = '20200301' and `asset_type` is not null;"
    id_df = dl.get_data_from_sql(sql).drop(columns=['transition', 'type_level_1', 'type_level_2', 'datetime', 'order_book_id'])

sql_indicators = "SELECT * FROM derived_data.{} where `datetime`='{}';".format(fi_name, tag_date)
    indicators_df = dl.get_data_from_sql(sql_indicators)

sql_tr = "select * from derived_data.track_error where `interval`={} and `datetime`='{}'".format(interval, tag_date)
    tr = dl.get_data_from_sql(sql_tr)

# asset allocation

 dl.get_data('active_asset_index').set_index('date').drop(['标普500','德标30','日经225'],axis = 1).fillna(method= 'ffill')