import pandas as pd
from python.fund.db.database import DerivedDatabaseConnector, BasicDatabaseConnector
from python.fund.db.view_models import IndexDailyCollection
from python.fund.db.basic_models import IndexInfo, IndexPrice
from python.fund.db.derived_models import IndexValuation, IndexReturn, IndexVolatility
from sqlalchemy import create_engine


def get_index_volatility():
    with DerivedDatabaseConnector().managed_session() as mn_session:
        try:
            latest_time = mn_session.query(IndexVolatility).order_by(IndexVolatility.datetime.desc()).limit(1).one_or_none()
            latest_time = latest_time.datetime
            print(latest_time)
            query = mn_session.query(
                IndexVolatility.index_id,
                IndexVolatility.datetime,
                IndexVolatility.w1_vol,
                IndexVolatility.m1_vol,
                IndexVolatility.m3_vol,
                IndexVolatility.m6_vol,
                IndexVolatility.y1_vol,
                IndexVolatility.y3_vol,
                IndexVolatility.y5_vol,
                IndexVolatility.y10_vol,
                IndexVolatility.this_y_vol,
                IndexVolatility.cumulative_vol,
            ).filter(IndexVolatility.datetime==latest_time)
            df = pd.read_sql(query.statement, query.session.bind)
            df = df.rename(columns={'datetime': 'vol_datetime'})
            df = df.set_index('index_id')
            return df
        except Exception as e:
            print('Failed get_index_volatility <err_msg> {}'.format(e))

def get_index_valuation():
    with DerivedDatabaseConnector().managed_session() as mn_session:
        try:
            latest_time = mn_session.query(IndexValuation).order_by(IndexValuation.datetime.desc()).limit(1).one_or_none()
            latest_time = latest_time.datetime
            print(latest_time)
            query = mn_session.query(
                IndexValuation.index_id,
                IndexValuation.pb_mrq,
                IndexValuation.pe_ttm,
                IndexValuation.peg_ttm,
                IndexValuation.roe_ttm,
                IndexValuation.dy_ttm,
                IndexValuation.pe_pct,
                IndexValuation.pb_pct,
                IndexValuation.val_score,
                IndexValuation.datetime,
            ).filter(IndexValuation.datetime==latest_time)
            df = pd.read_sql(query.statement, query.session.bind)
            df = df.set_index('index_id')
            return df

        except Exception as e:
            print('Failed get_index_valuation <err_msg> {}'.format(e))

def get_index_return():
    with DerivedDatabaseConnector().managed_session() as mn_session:
        try:
            latest_time = mn_session.query(IndexReturn).order_by(IndexReturn.datetime.desc()).limit(1).one_or_none()
            latest_time = latest_time.datetime
            print(latest_time)
            query = mn_session.query(
                IndexReturn.index_id,
                IndexReturn.datetime,
                IndexReturn.w1_ret,
                IndexReturn.m1_ret,
                IndexReturn.m3_ret,
                IndexReturn.m6_ret,
                IndexReturn.y1_ret,
                IndexReturn.y3_ret,
                IndexReturn.y5_ret,
                IndexReturn.y10_ret,
                IndexReturn.this_y_ret,
                IndexReturn.cumulative_ret,
            ).filter(IndexReturn.datetime==latest_time)
            df = pd.read_sql(query.statement, query.session.bind)
            df = df.rename(columns={'datetime': 'ret_datetime'})
            df = df.set_index('index_id')
            return df

        except Exception as e:
            print('Failed get_index_return<err_msg> {}'.format(e))

def get_index_info():
    with BasicDatabaseConnector().managed_session() as mn_session:
        try:
            query = mn_session.query(
                IndexInfo.index_id,
                IndexInfo.order_book_id,
                IndexInfo.industry_tag,
                IndexInfo.tag_method,
                IndexInfo.desc_name,
            )
            df = pd.read_sql(query.statement, query.session.bind)
            df = df.set_index('index_id')
            return df

        except Exception as e:
            print('Failed get_index_return<err_msg> {}'.format(e))

def get_index_price():
    with BasicDatabaseConnector().managed_session() as mn_session:
        try:
            latest_time = mn_session.query(IndexPrice).order_by(IndexPrice.datetime.desc()).limit(1).one_or_none()
            latest_time = latest_time.datetime
            print(latest_time)
            query = mn_session.query(
                IndexPrice.index_id,
                IndexPrice.datetime,
                IndexPrice.volume,
                IndexPrice.low,
                IndexPrice.close,
                IndexPrice.high,
                IndexPrice.open,
                IndexPrice.total_turnover,
                IndexPrice.ret,
            ).filter(IndexPrice.datetime==latest_time)
            df = pd.read_sql(query.statement, query.session.bind)
            df = df.rename(columns={'datetime': 'price_datetime'})
            df = df.set_index('index_id')
            return df

        except Exception as e:
            print('Failed get_index_return<err_msg> {}'.format(e))

def append_data(table_name, data_append_directly_data_df):
    engine = create_engine(
            'mysql+pymysql://wangjun:Wangjun123456@fundinfo.cq1tbd5lkqzo.rds.cn-northwest-1.amazonaws.com.cn:3306/view')

    if not data_append_directly_data_df.empty:
        data_append_directly_data_df.to_sql(table_name, engine, index = False, if_exists = 'append')
        print('新数据已插入')
    else:
        print('没有需要插入的新数据')

def collection_daily_index():

    print('1、 load data...')
    info = get_index_info()
    vol = get_index_volatility()
    ret = get_index_return()
    val = get_index_valuation()
    price = get_index_price()

    print('2、 concat data...')
    df = pd.concat([info, vol, ret, val, price], axis=1, sort=False)
    df.index.name = 'index_id'
    df = df.reset_index()

    print('3、 special option...')

    df['order_book_id'] = df['order_book_id'].apply(lambda x: x.split('.')[0] if x != 'not_available' else None)
    df['industry_tag'] = df['industry_tag'].apply(lambda x: x if x != 'not_available' else None)

    append_data(IndexDailyCollection.__tablename__, df)

    print(df)


if __name__ == '__main__':
    collection_daily_index()
