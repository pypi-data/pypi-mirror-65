from .index_valuation_processor import IndexValuationProcessor
from .derived_fund_indicator_processor import FundIndicatorProcessor

class DerivedDataProcessor(object):
    def __init__(self, rq_license):
        self.index_valuation_processor = IndexValuationProcessor()
        self.derived_fund_indicator_processor = FundIndicatorProcessor()

    def process(self, start_date, end_date):
        self.index_valuation_processor.index_valuation()
        self.derived_fund_indicator_processor.process()
