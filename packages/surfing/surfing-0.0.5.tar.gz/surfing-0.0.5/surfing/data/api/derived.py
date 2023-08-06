import math
import pandas as pd
import pickle as pkl
from ..wrapper.mysql import DerivedDatabaseConnector
from ..view.derived_models import *


def get_fund_indicator(fund_list):
    with DerivedDatabaseConnector().managed_session() as quant_session:
        try:
            query = quant_session.query(
                    FundIndicator.fund_id,
                    FundIndicator.datetime,
                    FundIndicator.alpha,
                    FundIndicator.beta,
                    FundIndicator.fee_rate,
                    FundIndicator.track_err,
                ).filter(
                    FundIndicator.fund_id.in_(fund_list),
                )
            tag_df = pd.read_sql(query.statement, query.session.bind)
            return tag_df
        
        except Exception as e:
            print('Failed to get data <err_msg> {}'.format(e))
    
def get_fund_score():
    with DerivedDatabaseConnector().managed_session() as quant_session:
        try:
            query = quant_session.query(
                    FundScore,   
                )
            tag_df = pd.read_sql(query.statement, query.session.bind)
            return tag_df
        
        except Exception as e:
            print('Failed to get data <err_msg> {}'.format(e))

def get_index_valuation(index_id, start_date):
    with DerivedDatabaseConnector().managed_session() as mn_session:
        try:
            query = mn_session.query(
                IndexValuation
            ).filter(
                IndexValuation.index_id == index_id,
                IndexValuation.datetime >= start_date,
            ).order_by(IndexValuation.datetime.asc())
            df = pd.read_sql(query.statement, query.session.bind)
            return df
        except Exception as e:
            print(e)
            return pd.DataFrame([])


