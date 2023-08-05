import inspect

class ReadableEnum(object):
    _code_name_cache = None

    @classmethod
    def init_cache(cls):
        cls._code_name_cache = ({}, {})
        for name in dir(cls):
            attr = getattr(cls, name)
            if name.startswith('_') or inspect.ismethod(attr):
                continue
            # assert attr not in cls._code_name_cache[0], f'failed to register {name}, {attr} is a registed value'
            # assert name not in cls._code_name_cache[1], f'failed to register {attr}, {name} is a registed enum'
            cls._code_name_cache[0][attr] = name
            cls._code_name_cache[1][name] = attr

    @classmethod
    def read(cls, code):
        if cls._code_name_cache is None:
            cls.init_cache()
        return cls._code_name_cache[0].get(code, code)

    @classmethod
    def parse(cls, code):
        if cls._code_name_cache is None:
            cls.init_cache()
        return cls._code_name_cache[1].get(code, code)


class BarraFactorType(ReadableEnum):
    BETA = 0 # 风险指数
    LEVERAGE = 1 # 杠杆率
    LONG_MOMENTUN = 2 # 长期动量
    QUALITY = 3 # 盈利能力
    SHORT_MOMENTUM = 4 # 短期动量
    SIZE = 5 # 市值
    TURNOVER = 6 # 换手率
    VALUE = 7 # 估值
    VOLATILITY = 8 # 收益波动率

STOCK_VALUATION_FACTORS = [
    'pe_ratio_lyr',
    'pe_ratio_ttm',
    'ep_ratio_lyr',
    'ep_ratio_ttm',
    'pcf_ratio_total_lyr',
    'pcf_ratio_total_ttm',
    'pcf_ratio_lyr',
    'pcf_ratio_ttm',
    'cfp_ratio_lyr',
    'cfp_ratio_ttm',
    'pb_ratio_lyr',
    'pb_ratio_ttm',
    'pb_ratio_lf',
    'book_to_market_ratio_lyr',
    'book_to_market_ratio_ttm',
    'book_to_market_ratio_lf',
    'dividend_yield_ttm',
    'peg_ratio_lyr',
    'peg_ratio_ttm',
    'ps_ratio_lyr',
    'ps_ratio_ttm',
    'sp_ratio_lyr',
    'sp_ratio_ttm',
    'market_cap',
    'market_cap_2',
    'market_cap_3',
    'a_share_market_val',
    'a_share_market_val_in_circulation',
    'ev_lyr',
    'ev_ttm',
    'ev_lf',
    'ev_no_cash_lyr',
    'ev_no_cash_ttm',
    'ev_no_cash_lf',
    'ev_to_ebitda_lyr',
    'ev_to_ebitda_ttm',
    'ev_no_cash_to_ebit_lyr',
    'ev_no_cash_to_ebit_ttm'
]

FUND_INDICATORS = [
    'last_week_return',
    'last_month_return',
    'last_three_month_return',
    'last_six_month_return',
    'last_twelve_month_return',
    'year_to_date_return',
    'to_date_return',
    'average_size',
    'annualized_returns',
    'annualized_risk',
    'sharp_ratio',
    'max_drop_down',
    'information_ratio'
]
