from .compute_fund_daily_collection import FundDailyCollectionProcessor
from .compute_index_daily_collection import IndexDailyCollectionProcessor

class ViewDataProcessor(object):
    def __init__(self, rq_license):
        self.fund_daily_collection_processor = FundDailyCollectionProcessor()
        self.index_daily_collection_processor = IndexDailyCollectionProcessor()

    def process(self, start_date, end_date):
        self.fund_daily_collection_processor.compute_daily_collection()
        self.index_daily_collection_processor.collection_daily_index()
