from ..util.constant import ReadableEnum

class DataType(ReadableEnum):
    #Industry Info data
    INDUSTRY_INFO = 200
    #Industry p/e
    INDUSTRY_PE = 201
    # stock latest financial indicator
    STOCK_FINANCIAL_INDICATOR = 202
    # stock daily value
    STOCK_DAILY_VALUE = 203
    # stock latest annual net profit
    STOCK_ANNUAL_NET_PROFIT = 204

    # industry pe ratio to update
    UPDATE_INDUSTRY_PE = 500
    # stock latest annual net profit to update
    UPDATE_STOCK_ANNUAL_NET_PROFIT = 501




