from sqlalchemy import CHAR, Column, Integer
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.dialects.mysql import DOUBLE

Base = declarative_base()

'''
文本用 Column(CHAR(...))
浮点用 Column(DOUBLE(asdecimal=False))
整数用 Column(Integer)
https://www.ricequant.com/doc/rqdata-institutional#research-API-instruments
'''

class FundFeeInfo(Base):
    '''基金费率表'''

    __tablename__ = 'fund_fee_info'
    id = Column(Integer, primary_key=True)

    wind_id = Column(CHAR(32)) # Wind代码
    symbol = Column(CHAR(32)) # 名称
    manage_fee = Column(DOUBLE(asdecimal=False)) # 管理费
    trustee_fee = Column(DOUBLE(asdecimal=False)) # 托管费
    purchase_fee = Column(DOUBLE(asdecimal=False)) # 申购费
    redeem_fee = Column(DOUBLE(asdecimal=False)) # 赎回费
    note = Column(CHAR(64)) # 附加信息
    fund_id = Column(CHAR(20)) # 基金名称


class Nav(Base):
    '''净值表'''

    __tablename__ = 'nav'
    id = Column(Integer, primary_key=True)

    fund_id = Column(CHAR(20)) # 基金ID
    acc_net_value = Column(DOUBLE(asdecimal=False)) # 累积单位净值
    adjusted_net_value = Column(DOUBLE(asdecimal=False)) # 复权净值
    change_rate = Column(DOUBLE(asdecimal=False)) # 涨跌幅
    daily_profit = Column(DOUBLE(asdecimal=False)) # 每万元收益（日结型货币基金专用）
    order_book_id = Column(CHAR(20)) # 合约代码
    redeem_status = Column(CHAR(10)) # 赎回状态，开放 - Open, 暂停 - Suspended, 限制大额申赎 - Limited, 封闭期 - Close
    subscribe_status = Column(CHAR(10)) # 订阅状态，开放 - Open, 暂停 - Suspended, 限制大额申赎 - Limited, 封闭期 - Close
    unit_net_value = Column(DOUBLE(asdecimal=False)) # 单位净值
    weekly_yield = Column(DOUBLE(asdecimal=False)) # 7日年化收益率（日结型货币基金专用）
    datetime = Column(CHAR(10)) # 日期


class ActiveAssetIndex(Base):
    '''大类资产指数表'''

    __tablename__ = 'active_asset_index'
    id = Column(Integer, primary_key=True)

    sp500 = Column(DOUBLE(asdecimal=False)) # 标普500
    n225 = Column(DOUBLE(asdecimal=False)) # 日经225
    dax30 = Column(DOUBLE(asdecimal=False)) # 德标30
    national_debt = Column(DOUBLE(asdecimal=False)) # 国债指数
    csi500 = Column(DOUBLE(asdecimal=False)) # 中证500
    real_state_index = Column(DOUBLE(asdecimal=False)) # 房地产指数
    gem = Column(DOUBLE(asdecimal=False)) # 创业板指
    csi300 = Column(DOUBLE(asdecimal=False)) # 沪深300
    gold = Column(DOUBLE(asdecimal=False)) # 黄金
    oil = Column(DOUBLE(asdecimal=False)) # 石油
    credit_debt = Column(DOUBLE(asdecimal=False)) # 中证信用
    sp500rmb = Column(DOUBLE(asdecimal=False)) # 标普500人民币
    n225rmb = Column(DOUBLE(asdecimal=False)) # 日经225人民币
    dax30rmb = Column(DOUBLE(asdecimal=False)) # 德标30人民币
    datetime = Column(CHAR(10)) # 日期


class FundListWind(Base):
    '''Wind 基金列表'''

    __tablename__ = 'fundlist_wind'
    id = Column(Integer, primary_key=True)

    fund_id = Column(CHAR(20)) # 基金ID
    wind_id = Column(CHAR(20)) # Wind基金ID
    transition = Column(Integer) # 基金变更次数
    order_book_id = Column(CHAR(20)) # RiceQuant基金ID
    symbol = Column(CHAR(64)) # 基金名称
    found_date = Column(CHAR(10)) # 成立日期
    end_date = Column(CHAR(10)) # 关闭日期
    wind_class_I = Column(CHAR(64)) # Wind基金类型
    wind_class_II = Column(CHAR(64)) # Wind基金二级类型
    fund_manager = Column(CHAR(255)) # 基金经理
    company_name = Column(CHAR(64)) # 基金公司
    benchmark = Column(CHAR(255)) # 业绩基准
    fund_full_name = Column(CHAR(255)) # 基金全名
    money = Column(CHAR(20)) # 币种
    structured_fund_base_fund_code = Column(CHAR(20)) # 分级基金基础基金代号
    if_structured_fund = Column(CHAR(10)) # 是否为分级基金
    if_regular_open_fund = Column(CHAR(10)) # 是否为开放式基金
    update_time = Column(CHAR(20)) # 更新时间


class StockValuation(Base):
    '''
    股票每日估值
    LF, Last File 时效性最好
    LYR, Last Year Ratio 上市公司年报有审计要求，数据可靠性最高
    TTM, Trailing Twelve Months 时效性较好，滚动4个报告期计算，可避免某一期财报数据的偶然性
    '''

    __tablename__ = 'stock_valuation'
    order_book_id = Column(CHAR(20), primary_key=True) # 基金ID
    datetime = Column(CHAR(10), primary_key=True) # 日期

    pe_ratio_lyr = Column(DOUBLE(asdecimal=False)) # 市盈率lyr
    pe_ratio_ttm = Column(DOUBLE(asdecimal=False)) # 市盈率ttm
    ep_ratio_lyr = Column(DOUBLE(asdecimal=False)) # 盈市率lyr
    ep_ratio_ttm = Column(DOUBLE(asdecimal=False)) # 盈市率ttm
    pcf_ratio_total_lyr = Column(DOUBLE(asdecimal=False)) # 市现率_总现金流lyr
    pcf_ratio_total_ttm = Column(DOUBLE(asdecimal=False)) # 市现率_总现金流ttm
    pcf_ratio_lyr = Column(DOUBLE(asdecimal=False)) # 市现率_经营lyr
    pcf_ratio_ttm = Column(DOUBLE(asdecimal=False)) # 市现率_经营 ttm
    cfp_ratio_lyr = Column(DOUBLE(asdecimal=False)) # 现金收益率lyr
    cfp_ratio_ttm = Column(DOUBLE(asdecimal=False)) # 现金收益率ttm
    pb_ratio_lyr = Column(DOUBLE(asdecimal=False)) # 市净率lyr
    pb_ratio_ttm = Column(DOUBLE(asdecimal=False)) # 市净率ttm
    pb_ratio_lf = Column(DOUBLE(asdecimal=False)) # 市净率lf
    book_to_market_ratio_lyr = Column(DOUBLE(asdecimal=False)) # 账面市值比lyr
    book_to_market_ratio_ttm = Column(DOUBLE(asdecimal=False)) # 账面市值比ttm
    book_to_market_ratio_lf = Column(DOUBLE(asdecimal=False)) # 账面市值比lf
    dividend_yield_ttm = Column(DOUBLE(asdecimal=False)) # 股息率ttm
    peg_ratio_lyr = Column(DOUBLE(asdecimal=False)) # PEG值lyr
    peg_ratio_ttm = Column(DOUBLE(asdecimal=False)) # PEG值ttm
    ps_ratio_lyr = Column(DOUBLE(asdecimal=False)) # 市销率lyr
    ps_ratio_ttm = Column(DOUBLE(asdecimal=False)) # 市销率ttm
    sp_ratio_lyr = Column(DOUBLE(asdecimal=False)) # 销售收益率lyr
    sp_ratio_ttm = Column(DOUBLE(asdecimal=False)) # 销售收益率ttm
    market_cap = Column(DOUBLE(asdecimal=False)) # 总市值1 
    market_cap_2 = Column(DOUBLE(asdecimal=False)) # 流通股总市值
    market_cap_3 = Column(DOUBLE(asdecimal=False)) # 总市值3
    a_share_market_val = Column(DOUBLE(asdecimal=False)) # A股市值
    a_share_market_val_in_circulation = Column(DOUBLE(asdecimal=False)) # 流通A股市值
    ev_lyr = Column(DOUBLE(asdecimal=False)) # 企业价值lyr
    ev_ttm = Column(DOUBLE(asdecimal=False)) # 企业价值ttm
    ev_lf = Column(DOUBLE(asdecimal=False)) # 企业价值lf 
    ev_no_cash_lyr = Column(DOUBLE(asdecimal=False)) #企业价值(不含货币资金)lyr
    ev_no_cash_ttm = Column(DOUBLE(asdecimal=False)) # 企业价值(不含货币资金)ttm
    ev_no_cash_lf = Column(DOUBLE(asdecimal=False)) # 企业价值(不含货币资金)lf
    ev_to_ebitda_lyr = Column(DOUBLE(asdecimal=False)) # 企业倍数lyr
    ev_to_ebitda_ttm = Column(DOUBLE(asdecimal=False)) # 企业倍数ttm
    ev_no_cash_to_ebit_lyr = Column(DOUBLE(asdecimal=False)) #企业倍数(不含货币资金)lyr
    ev_no_cash_to_ebit_ttm = Column(DOUBLE(asdecimal=False)) # 企业倍数(不含货币资金)ttm


class IndexPrice(Base):
    '''指数价格'''

    __tablename__ = 'index_price'
    order_book_id = Column(CHAR(20), primary_key=True) # 指数ID
    datetime = Column(CHAR(10), primary_key=True) # 日期

    volume = Column(DOUBLE(asdecimal=False)) # 交易量
    low = Column(DOUBLE(asdecimal=False)) # 最低价
    close = Column(DOUBLE(asdecimal=False)) # 收盘价
    high = Column(DOUBLE(asdecimal=False)) # 最高价
    open = Column(DOUBLE(asdecimal=False)) # 开盘价
    num_trades = Column(Integer) # 交易笔数
    total_turnover = Column(DOUBLE(asdecimal=False)) # 总成交量
    ret = Column(DOUBLE(asdecimal=False)) # 收益率

class StockDailyPrice(Base):
    '''股票价格'''

    __tablename__ = 'stock_daily_price'
    order_book_id = Column(CHAR(20), primary_key=True) # 指数ID
    datetime = Column(CHAR(10), primary_key=True) # 日期

    close = Column(DOUBLE(asdecimal=False))
    limit_down = Column(DOUBLE(asdecimal=False))
    limit_up = Column(DOUBLE(asdecimal=False))
    open = Column(DOUBLE(asdecimal=False))
    low = Column(DOUBLE(asdecimal=False))
    total_turnover = Column(DOUBLE(asdecimal=False))
    num_trades = Column(DOUBLE(asdecimal=False))
    high = Column(DOUBLE(asdecimal=False))
    volume = Column(DOUBLE(asdecimal=False))
    adj_close = Column(DOUBLE(asdecimal=False))
    adj_post = Column(DOUBLE(asdecimal=False))
    ret = Column(DOUBLE(asdecimal=False))

class FundIndicator(Base):
    """基金收益信息"""

    __tablename__ = 'fund_indicators'
    # id = Column(Integer, primary_key=True)

    annualized_returns = Column(DOUBLE(asdecimal=False))  # 成立以来年化收益率
    annualized_risk = Column(DOUBLE(asdecimal=False))  #  成立以来年化风险
    average_size = Column(DOUBLE(asdecimal=False))  # 平均规模
    information_ratio = Column(DOUBLE(asdecimal=False))  # 成立以来信息比率
    last_month_return = Column(DOUBLE(asdecimal=False))  # 近一月收益率
    last_six_month_return = Column(DOUBLE(asdecimal=False))
    last_three_month_return = Column(DOUBLE(asdecimal=False))  # 近一季度收益率
    last_twelve_month_return = Column(DOUBLE(asdecimal=False))  # 近一年收益率
    last_two_year_return_a = Column(DOUBLE(asdecimal=False))
    last_week_return = Column(DOUBLE(asdecimal=False))  # 近一周收益率
    last_year_return_a = Column(DOUBLE(asdecimal=False))
    m1_alpha = Column(DOUBLE(asdecimal=False))
    m1_beta = Column(DOUBLE(asdecimal=False))
    m1_calmar_a = Column(DOUBLE(asdecimal=False))
    m1_excess_a = Column(DOUBLE(asdecimal=False))
    m1_inf_a = Column(DOUBLE(asdecimal=False))
    m1_return = Column(DOUBLE(asdecimal=False))
    m1_return_a = Column(DOUBLE(asdecimal=False))
    m1_sharp_a = Column(DOUBLE(asdecimal=False))
    m1_sor_a = Column(DOUBLE(asdecimal=False))
    m1_stdev = Column(DOUBLE(asdecimal=False))
    m1_stdev_a = Column(DOUBLE(asdecimal=False))
    m3_alpha = Column(DOUBLE(asdecimal=False))
    m3_beta = Column(DOUBLE(asdecimal=False))
    m3_calmar_a = Column(DOUBLE(asdecimal=False))
    m3_excess_a = Column(DOUBLE(asdecimal=False))
    m3_inf_a = Column(DOUBLE(asdecimal=False))
    m3_return = Column(DOUBLE(asdecimal=False))
    m3_return_a = Column(DOUBLE(asdecimal=False))
    m3_sharp_a = Column(DOUBLE(asdecimal=False))
    m3_sor_a = Column(DOUBLE(asdecimal=False))
    m3_stdev = Column(DOUBLE(asdecimal=False))
    m3_stdev_a = Column(DOUBLE(asdecimal=False))
    m6_alpha = Column(DOUBLE(asdecimal=False))
    m6_beta = Column(DOUBLE(asdecimal=False))
    m6_calmar_a = Column(DOUBLE(asdecimal=False))
    m6_excess_a = Column(DOUBLE(asdecimal=False))
    m6_inf_a = Column(DOUBLE(asdecimal=False))
    m6_return = Column(DOUBLE(asdecimal=False))
    m6_return_a = Column(DOUBLE(asdecimal=False))
    m6_sharp_a = Column(DOUBLE(asdecimal=False))
    m6_sor_a = Column(DOUBLE(asdecimal=False))
    m6_stdev = Column(DOUBLE(asdecimal=False))
    m6_stdev_a = Column(DOUBLE(asdecimal=False))
    max_drop_down = Column(DOUBLE(asdecimal=False))   # 成立以来最大回撤
    month_return = Column(DOUBLE(asdecimal=False))
    quarter_alpha = Column(DOUBLE(asdecimal=False))
    quarter_beta = Column(DOUBLE(asdecimal=False))
    quarter_calmar_a = Column(DOUBLE(asdecimal=False))
    quarter_excess_a = Column(DOUBLE(asdecimal=False))
    quarter_inf_a = Column(DOUBLE(asdecimal=False))
    quarter_return = Column(DOUBLE(asdecimal=False))
    quarter_return_a = Column(DOUBLE(asdecimal=False))
    quarter_sharp_a = Column(DOUBLE(asdecimal=False))
    quarter_sor_a = Column(DOUBLE(asdecimal=False))
    quarter_stdev = Column(DOUBLE(asdecimal=False))
    quarter_stdev_a = Column(DOUBLE(asdecimal=False))
    sharp_ratio = Column(DOUBLE(asdecimal=False))   # 成立以来夏普比率
    to_date_return = Column(DOUBLE(asdecimal=False))  # 成立至今收益率
    total_alpha = Column(DOUBLE(asdecimal=False))
    total_beta = Column(DOUBLE(asdecimal=False))
    total_calmar_a = Column(DOUBLE(asdecimal=False))
    total_excess_a = Column(DOUBLE(asdecimal=False))
    total_inf_a = Column(DOUBLE(asdecimal=False))
    total_return = Column(DOUBLE(asdecimal=False))
    total_return_a = Column(DOUBLE(asdecimal=False))
    total_sharp_a = Column(DOUBLE(asdecimal=False))
    total_sor_a = Column(DOUBLE(asdecimal=False))
    total_stdev = Column(DOUBLE(asdecimal=False))
    total_stdev_a = Column(DOUBLE(asdecimal=False))
    week_return = Column(DOUBLE(asdecimal=False))
    y1_alpha = Column(DOUBLE(asdecimal=False))
    y1_beta = Column(DOUBLE(asdecimal=False))
    y1_calmar_a = Column(DOUBLE(asdecimal=False))
    y1_excess_a = Column(DOUBLE(asdecimal=False))
    y1_inf_a = Column(DOUBLE(asdecimal=False))
    y1_return = Column(DOUBLE(asdecimal=False))
    y1_return_a = Column(DOUBLE(asdecimal=False))
    y1_sharp_a = Column(DOUBLE(asdecimal=False))
    y1_sor_a = Column(DOUBLE(asdecimal=False))
    y1_stdev = Column(DOUBLE(asdecimal=False))
    y1_stdev_a = Column(DOUBLE(asdecimal=False))
    y2_alpha = Column(DOUBLE(asdecimal=False))
    y2_beta = Column(DOUBLE(asdecimal=False))
    y2_calmar_a = Column(DOUBLE(asdecimal=False))
    y2_excess_a = Column(DOUBLE(asdecimal=False))
    y2_inf_a = Column(DOUBLE(asdecimal=False))
    y2_return = Column(DOUBLE(asdecimal=False))
    y2_return_a = Column(DOUBLE(asdecimal=False))
    y2_sharp_a = Column(DOUBLE(asdecimal=False))
    y2_sor_a = Column(DOUBLE(asdecimal=False))
    y2_stdev = Column(DOUBLE(asdecimal=False))
    y2_stdev_a = Column(DOUBLE(asdecimal=False))
    y3_alpha = Column(DOUBLE(asdecimal=False))
    y3_beta = Column(DOUBLE(asdecimal=False))
    y3_calmar_a = Column(DOUBLE(asdecimal=False))
    y3_excess_a = Column(DOUBLE(asdecimal=False))
    y3_inf_a = Column(DOUBLE(asdecimal=False))
    y3_return = Column(DOUBLE(asdecimal=False))
    y3_return_a = Column(DOUBLE(asdecimal=False))
    y3_sharp_a = Column(DOUBLE(asdecimal=False))
    y3_sor_a = Column(DOUBLE(asdecimal=False))
    y3_stdev = Column(DOUBLE(asdecimal=False))
    y3_stdev_a = Column(DOUBLE(asdecimal=False))
    y5_alpha = Column(DOUBLE(asdecimal=False))
    y5_beta = Column(DOUBLE(asdecimal=False))
    y5_calmar_a = Column(DOUBLE(asdecimal=False))
    y5_excess_a = Column(DOUBLE(asdecimal=False))
    y5_inf_a = Column(DOUBLE(asdecimal=False))
    y5_return = Column(DOUBLE(asdecimal=False))
    y5_return_a = Column(DOUBLE(asdecimal=False))
    y5_sharp_a = Column(DOUBLE(asdecimal=False))
    y5_sor_a = Column(DOUBLE(asdecimal=False))
    y5_stdev = Column(DOUBLE(asdecimal=False))
    y5_stdev_a = Column(DOUBLE(asdecimal=False))
    year_alpha = Column(DOUBLE(asdecimal=False))
    year_beta = Column(DOUBLE(asdecimal=False))
    year_calmar_a = Column(DOUBLE(asdecimal=False))
    year_excess_a = Column(DOUBLE(asdecimal=False))
    year_inf_a = Column(DOUBLE(asdecimal=False))
    year_return = Column(DOUBLE(asdecimal=False))
    year_return_a = Column(DOUBLE(asdecimal=False))
    year_sharp_a = Column(DOUBLE(asdecimal=False))
    year_sor_a = Column(DOUBLE(asdecimal=False))
    year_stdev = Column(DOUBLE(asdecimal=False))
    year_stdev_a = Column(DOUBLE(asdecimal=False))
    year_to_date_return = Column(DOUBLE(asdecimal=False))  # 今年以来收益率
    order_book_id = Column(CHAR(20), primary_key=True)  # 订阅id
    datetime = Column(CHAR(20))  # 时间


# class StockFinancialIndicator(Base):
#     '''股票财报'''

#     __tablename__ = 'stock_financial_indicator'
#     id = Column(Integer, primary_key=True)

#     order_book_id = Column(CHAR(20)) # 股票ID
#     quarter = Column(CHAR(10)) # 季度
#     fcfe = Column(DOUBLE(asdecimal=False)) # 股权自由现金流量
#     adjusted_return_on_equity_weighted_average = Column(DOUBLE(asdecimal=False)) # 资产净收益
#     inc_revenue = Column(DOUBLE(asdecimal=False)) # 营业收入同比增长
#     net_debt = Column(DOUBLE(asdecimal=False)) # 净债务
#     quick_ratio = Column(DOUBLE(asdecimal=False)) # 速动比率
#     ev_to_ebitda = Column(DOUBLE(asdecimal=False)) # 企业倍数
#     retained_earnings_per_share = Column(DOUBLE(asdecimal=False)) # 每股留存收益
#     equity_to_debt_ratio = Column(DOUBLE(asdecimal=False)) # 权益负债比率
#     ebitda = Column(DOUBLE(asdecimal=False)) # 息税折旧摊销前利润l
#     inc_cash_from_operations  = Column(DOUBLE(asdecimal=False)) # 经营活动有关现金
#     total_asset_turnover = Column(DOUBLE(asdecimal=False)) # 总资产周转率
#     debt_to_asset_ratio = Column(DOUBLE(asdecimal=False)) # 资产负债率
#     net_working_capital = Column(DOUBLE(asdecimal=False)) # 净营运资本
#     free_cash_flow_equity_per_share = Column(DOUBLE(asdecimal=False)) # 每股股东自由现金流
#     return_on_asset = Column(DOUBLE(asdecimal=False)) # 总资产净利率
#     current_asset_to_total_asset = Column(DOUBLE(asdecimal=False)) # 流动资产比率
#     return_on_equity_weighted_average = Column(DOUBLE(asdecimal=False)) # 净资产收益率
#     non_current_debt_to_total_debt = Column(DOUBLE(asdecimal=False)) # 非流动负债率
#     ebit_to_debt = Column(DOUBLE(asdecimal=False)) # 税前利润负债比率
#     annual_return_on_equity = Column(DOUBLE(asdecimal=False)) # 权益年化收益
#     adjusted_profit_to_total_profit = Column(DOUBLE(asdecimal=False)) # 扣除非经常损益后的净利润与净利润之比
#     long_term_debt_to_working_capital = Column(DOUBLE(asdecimal=False)) # 长期负债营运资本比率
#     current_debt_to_total_debt = Column(DOUBLE(asdecimal=False)) # 流动负债比率
#     inc_diluted_earnings_per_share = Column(DOUBLE(asdecimal=False)) # 稀释每股收益同比增长率
#     annual_return_on_asset_net_profit = Column(DOUBLE(asdecimal=False)) # 总资产年化收益率
#     ocf_to_interest_bearing_debt = Column(DOUBLE(asdecimal=False)) # 经营活动产生的现金流量净额/带息债务
#     book_value_per_share = Column(DOUBLE(asdecimal=False)) # 每股净资产
#     gross_profit_margin = Column(DOUBLE(asdecimal=False)) # 销售毛利率
#     expense_to_revenue = Column(DOUBLE(asdecimal=False)) # 经营成本率
#     ebit_to_revenue = Column(DOUBLE(asdecimal=False)) # 税前收益率
#     non_interest_bearing_current_debt = Column(DOUBLE(asdecimal=False)) # 无息流动负债
#     non_current_asset_to_total_asset = Column(DOUBLE(asdecimal=False)) # 非流动资产比率
#     equity_to_interest_bearing_debt = Column(DOUBLE(asdecimal=False)) # 权益带息负债比率
#     interest_bearing_debt = Column(DOUBLE(asdecimal=False)) # 带息债务
#     debt_to_equity_ratio = Column(DOUBLE(asdecimal=False)) # 产权比率
#     inc_book_per_share = Column(DOUBLE(asdecimal=False)) # 每股净资产同比增长率
#     invested_capital = Column(DOUBLE(asdecimal=False)) # 全部投入资本
#     retained_earnings = Column(DOUBLE(asdecimal=False)) # 留存收益
#     fixed_asset_turnover = Column(DOUBLE(asdecimal=False)) # 固定资产周转率
#     fcff = Column(DOUBLE(asdecimal=False)) # 企业自由现金流量
#     tangible_asset_to_interest_bearing_debt = Column(DOUBLE(asdecimal=False)) # 有形资产带息负债比率
#     capital_reserve_per_share = Column(DOUBLE(asdecimal=False)) # 每股资本公积金
#     non_operating_profit_to_profit_before_tax = Column(DOUBLE(asdecimal=False)) # 非经营收益税前收益比率
#     return_on_equity = Column(DOUBLE(asdecimal=False)) # 净资产收益率
#     earnings_per_share = Column(DOUBLE(asdecimal=False)) # 每股收益
#     cash_flow_from_operations_per_share = Column(DOUBLE(asdecimal=False)) # 每股经营活动现金流
#     current_ratio = Column(DOUBLE(asdecimal=False)) # 流动比率
#     du_equity_multiplier = Column(DOUBLE(asdecimal=False)) # 权益乘数(杜邦分析)
#     ocf_to_net_debt = Column(DOUBLE(asdecimal=False)) # 经营活动产生的现金流量净额/净债务
#     income_tax_to_profit_before_tax = Column(DOUBLE(asdecimal=False)) # 所得税与利润总额之比
#     inc_return_on_equity = Column(DOUBLE(asdecimal=False)) # 净资产收益率(摊薄）同比增长率
#     dividend_per_share = Column(DOUBLE(asdecimal=False)) # 每股分红
#     return_on_equity_diluted = Column(DOUBLE(asdecimal=False)) # 摊薄净资产收益率
#     du_profit_margin = Column(DOUBLE(asdecimal=False)) # 净利率(杜邦分析）
#     operating_revenue_per_share = Column(DOUBLE(asdecimal=False)) # 每股营业收入
#     ev_2 = Column(DOUBLE(asdecimal=False)) # 企业价值
#     net_profit_to_revenue = Column(DOUBLE(asdecimal=False)) # 经营净利率
#     inc_operating_revenue = Column(DOUBLE(asdecimal=False)) # 营业收入同比增长率
#     cost_to_sales = Column(DOUBLE(asdecimal=False)) # 销售成本率
#     interest_bearing_debt_to_capital = Column(DOUBLE(asdecimal=False)) # 带息债务占企业全部投入成本的比重
#     free_cash_flow_company_per_share = Column(DOUBLE(asdecimal=False)) # 每股企业自由现金流
#     account_payable_turnover_days = Column(DOUBLE(asdecimal=False)) # 应付账款周转天数
#     return_on_asset_net_profit = Column(DOUBLE(asdecimal=False)) # 总资产净利率
#     du_return_on_equity = Column(DOUBLE(asdecimal=False)) # 净资产收益率ROE(杜邦分析)
#     ebit_per_share = Column(DOUBLE(asdecimal=False)) # 每股息税前利润
#     account_receivable_turnover_days = Column(DOUBLE(asdecimal=False)) # 应收账款周转天数
#     diluted_earnings_per_share = Column(DOUBLE(asdecimal=False)) # 稀释每股收益
#     tangible_asset_to_debt = Column(DOUBLE(asdecimal=False)) #  有形资产负债比率
#     inc_net_profit = Column(DOUBLE(asdecimal=False)) # 净收益同比增长率
#     adjusted_fully_diluted_earnings_per_share = Column(DOUBLE(asdecimal=False)) # 稀释每股收益_扣除
#     tangible_assets = Column(DOUBLE(asdecimal=False)) # 有形资产
#     adjusted_earnings_per_share = Column(DOUBLE(asdecimal=False)) # 基本每股收益_扣除
#     account_receivable_turnover_rate = Column(DOUBLE(asdecimal=False)) # 应收账款周转率
#     net_profit_margin = Column(DOUBLE(asdecimal=False)) # 销售净利率
#     operating_profit_to_profit_before_tax = Column(DOUBLE(asdecimal=False)) # 经营活动净收益与利润总额之比
#     fully_diluted_earnings_per_share = Column(DOUBLE(asdecimal=False)) # 稀释每股收益
#     operating_cash_flow_per_share = Column(DOUBLE(asdecimal=False)) # 每股经营现金流
#     operating_total_revenue_per_share = Column(DOUBLE(asdecimal=False)) # 每股营业总收入
#     return_on_invested_capital = Column(DOUBLE(asdecimal=False)) # 投入资本回报率
#     du_return_on_sales = Column(DOUBLE(asdecimal=False)) # 息税前利润/营业总收入
#     non_recurring_profit_and_loss = Column(DOUBLE(asdecimal=False)) # 非经常性损益
#     invesment_profit_to_profit_before_tax = Column(DOUBLE(asdecimal=False)) # 投资收益税前收益比率
#     ocf_to_current_ratio = Column(DOUBLE(asdecimal=False)) # 经营活动产生的现金流量净额/流动负债
#     earned_reserve_per_share = Column(DOUBLE(asdecimal=False)) # 每股盈余公积金
#     profit_from_operation_to_revenue = Column(DOUBLE(asdecimal=False)) # 营业利润率
#     inc_adjusted_net_profit = Column(DOUBLE(asdecimal=False)) # 净资产收益率同比增长率
#     annual_return_on_asset = Column(DOUBLE(asdecimal=False)) # 年化总资产报酬率
#     equity_multiplier = Column(DOUBLE(asdecimal=False)) # 权益乘数
#     ev = Column(DOUBLE(asdecimal=False)) # 企业价值
#     super_quick_ratio = Column(DOUBLE(asdecimal=False)) # 超速动比率
#     du_asset_turnover_ratio = Column(DOUBLE(asdecimal=False)) # 资产周转率
#     inc_gross_profit = Column(DOUBLE(asdecimal=False)) # 毛利率同比增长率
#     undistributed_profit_per_share = Column(DOUBLE(asdecimal=False)) # 每股未分配利润
#     inc_earnings_per_share = Column(DOUBLE(asdecimal=False)) # 每股收益同比增长率
#     adjusted_return_on_equity_average = Column(DOUBLE(asdecimal=False)) # 平均净资产收益率_扣除
#     time_interest_earned_ratio = Column(DOUBLE(asdecimal=False)) # 利息保障倍数
#     non_interest_bearing_non_current_debt = Column(DOUBLE(asdecimal=False)) # 无息非流动负债
#     current_asset_turnover = Column(DOUBLE(asdecimal=False)) # 流动资产周转率
#     adjusted_net_profit = Column(DOUBLE(asdecimal=False))# # 收益_扣除
#     inc_total_asset = Column(DOUBLE(asdecimal=False)) # 总资产同比增长率
#     depreciation_and_amortization = Column(DOUBLE(asdecimal=False)) # 当期计提折旧与摊销
#     account_payable_turnover_rate = Column(DOUBLE(asdecimal=False)) # 应付账款周转率
#     inc_profit_before_tax = Column(DOUBLE(asdecimal=False)) # 利润总额同比增长率
#     inventory_turnover = Column(DOUBLE(asdecimal=False)) # 存货周转率
#     ebit = Column(DOUBLE(asdecimal=False)) # 息税前利润
#     adjusted_return_on_equity_diluted = Column(DOUBLE(asdecimal=False)) # 摊薄净资产收益率_扣除
#     ocf_to_debt  = Column(DOUBLE(asdecimal=False)) # 经营活动产生的现金流量净额/负债合计
#     working_capital = Column(DOUBLE(asdecimal=False)) # 营运资本
#     announce_date = Column(CHAR(20)) # 发布日期


# class StockBalanceSheet(Base):
#     __tablename__ = 'stock_balance_sheet'
#     id = Column(Integer, primary_key=True)

#     order_book_id = Column(CHAR(20))
#     quarter = Column(CHAR(10))
#     liability_prefer_stock = Column(DOUBLE(asdecimal=False))
#     long_term_liabilities_due_one_year = Column(DOUBLE(asdecimal=False))
#     real_estate_investment = Column(DOUBLE(asdecimal=False))
#     accts_payable = Column(DOUBLE(asdecimal=False))
#     dividend_receivable = Column(DOUBLE(asdecimal=False))
#     interest_receivable = Column(DOUBLE(asdecimal=False))
#     cash = Column(DOUBLE(asdecimal=False))
#     current_assets = Column(DOUBLE(asdecimal=False))
#     deferred_income = Column(DOUBLE(asdecimal=False))
#     construction_in_progress = Column(DOUBLE(asdecimal=False))
#     paid_in_capital = Column(DOUBLE(asdecimal=False))
#     equity_preferred_stock = Column(DOUBLE(asdecimal=False))
#     bill_receivable = Column(DOUBLE(asdecimal=False))
#     deferred_expense = Column(DOUBLE(asdecimal=False))
#     long_term_deferred_expenses = Column(DOUBLE(asdecimal=False))
#     depreciation_reserve = Column(DOUBLE(asdecimal=False))
#     estimated_liabilities = Column(DOUBLE(asdecimal=False))
#     prepaid_tax = Column(DOUBLE(asdecimal=False))
#     short_term_debt = Column(DOUBLE(asdecimal=False))
#     tax_payable = Column(DOUBLE(asdecimal=False))
#     deferred_income_tax_assets = Column(DOUBLE(asdecimal=False))
#     surplus_reserve = Column(DOUBLE(asdecimal=False))
#     long_term_payable = Column(DOUBLE(asdecimal=False))
#     goodwill = Column(DOUBLE(asdecimal=False))
#     prepayment = Column(DOUBLE(asdecimal=False))
#     accumulated_depreciation = Column(DOUBLE(asdecimal=False))
#     notes_payable = Column(DOUBLE(asdecimal=False))
#     minority_interest = Column(DOUBLE(asdecimal=False))
#     non_current_liability_due_one_year = Column(DOUBLE(asdecimal=False))
#     long_term_equity_investment = Column(DOUBLE(asdecimal=False))
#     intangible_assets = Column(DOUBLE(asdecimal=False))
#     other_current_liabilities = Column(DOUBLE(asdecimal=False))
#     financial_asset_held_for_trading = Column(DOUBLE(asdecimal=False))
#     cash_equivalent = Column(DOUBLE(asdecimal=False))
#     provision = Column(DOUBLE(asdecimal=False))
#     deferred_revenue = Column(DOUBLE(asdecimal=False))
#     impairment_intangible_assets = Column(DOUBLE(asdecimal=False))
#     total_assets = Column(DOUBLE(asdecimal=False))
#     long_term_receivables = Column(DOUBLE(asdecimal=False))
#     net_fixed_assets = Column(DOUBLE(asdecimal=False))
#     current_liabilities = Column(DOUBLE(asdecimal=False))
#     total_equity = Column(DOUBLE(asdecimal=False))
#     inventory = Column(DOUBLE(asdecimal=False))
#     non_current_asset_due_one_year = Column(DOUBLE(asdecimal=False))
#     non_current_liabilities = Column(DOUBLE(asdecimal=False))
#     bond_payable = Column(DOUBLE(asdecimal=False))
#     interest_payable = Column(DOUBLE(asdecimal=False))
#     net_accts_receivable = Column(DOUBLE(asdecimal=False))
#     grants_received = Column(DOUBLE(asdecimal=False))
#     total_liabilities = Column(DOUBLE(asdecimal=False))
#     other_payable = Column(DOUBLE(asdecimal=False))
#     financial_liabilities = Column(DOUBLE(asdecimal=False))
#     capital_reserve = Column(DOUBLE(asdecimal=False))
#     financial_asset_hold_to_maturity = Column(DOUBLE(asdecimal=False))
#     oil_and_gas_assets = Column(DOUBLE(asdecimal=False))
#     equity_parent_company = Column(DOUBLE(asdecimal=False))
#     other_fees_payable = Column(DOUBLE(asdecimal=False))
#     housing_revolving_funds = Column(DOUBLE(asdecimal=False))
#     engineer_material = Column(DOUBLE(asdecimal=False))
#     undistributed_profit = Column(DOUBLE(asdecimal=False))
#     net_long_term_equity_investment = Column(DOUBLE(asdecimal=False))
#     financial_asset_available_for_sale = Column(DOUBLE(asdecimal=False))
#     fixed_asset_to_be_disposed = Column(DOUBLE(asdecimal=False))
#     short_term_loans = Column(DOUBLE(asdecimal=False))
#     contract_work = Column(DOUBLE(asdecimal=False))
#     payroll_payable = Column(DOUBLE(asdecimal=False))
#     accrued_expense = Column(DOUBLE(asdecimal=False))
#     long_term_deferred_income = Column(DOUBLE(asdecimal=False))
#     deferred_income_tax_liabilities = Column(DOUBLE(asdecimal=False))
#     other_non_current_liabilities = Column(DOUBLE(asdecimal=False))
#     invesment_refund = Column(DOUBLE(asdecimal=False))
#     non_current_assets = Column(DOUBLE(asdecimal=False))
#     other_non_current_assets = Column(DOUBLE(asdecimal=False))
#     capitalized_biological_assets = Column(DOUBLE(asdecimal=False))
#     other_current_assets = Column(DOUBLE(asdecimal=False))
#     bad_debt_reserve = Column(DOUBLE(asdecimal=False))
#     advance_from_customers = Column(DOUBLE(asdecimal=False))
#     long_term_loans = Column(DOUBLE(asdecimal=False))
#     dividend_payable = Column(DOUBLE(asdecimal=False))
#     total_equity_and_liabilities = Column(DOUBLE(asdecimal=False))
#     long_term_investment = Column(DOUBLE(asdecimal=False))
#     announce_date = Column(CHAR(20))


# class StockInfo(Base):
#     '''行业分类信息'''
#   TODO sql table data type not corret
#     __tablename__ = 'stock_info'
#     abbrev_symbol = Column(CHAR(10)) #证券名称缩写
#     board_type = Column(CHAR(10)) #板块类别
#     de_listed_date = Column(CHAR(10)) #退市日期
#     exchange = Column(CHAR(5)) #交易所
#     industry_code = Column(CHAR(5)) #国民经济行业代码
#     industry_name = Column(Text) #行业名称
#     listed_date = Column(CHAR(10)) #证券上市日期
#     market_tplus = Column(BigInteger) #交易制度
#     order_book_id = Column(Column(CHAR(10)), primary_key=True) #股票id
#     round_lot = Column(DOUBLE(asdecimal=False)) #最小下单手数
#     sector_code = Column(Text) #板块英文代码
#     sector_code_name = Column(Text) #板块中文
#     special_type = Column(CHAR(8)) #特别处理状态
#     status = Column(Text) #合约状态
#     symbol = Column(CHAR(10))# 简称
#     trading_hours = Column(Text) #合约交易时间
#     type = Column(CHAR(10)) #合约类型


# class BasicFundIndicators(Base):
#     __tablename__ = 'basic_fund_indicators'
#     order_book_id = Column(CHAR(20), primary_key=True)
#     datetime = Column(CHAR(10), primary_key=True)
#     Beta = Column(DOUBLE(asdecimal=False))
#     Alpha = Column(DOUBLE(asdecimal=False))
#     Treynor_Ratio = Column(DOUBLE(asdecimal=False))
#     Max_DD = Column(DOUBLE(asdecimal=False))
#     Downside_Risk = Column(DOUBLE(asdecimal=False))
#     Return_Over_Period = Column(DOUBLE(asdecimal=False))
#     Annualized_Average_Daily_Return = Column(DOUBLE(asdecimal=False))
#     Volatility = Column(DOUBLE(asdecimal=False))
#     M_square = Column(DOUBLE(asdecimal=False))
#     Time_Return = Column(DOUBLE(asdecimal=False))
#     Value_at_Risk = Column(DOUBLE(asdecimal=False))
#     R_square = Column(DOUBLE(asdecimal=False))
#     Sharp_Ratio = Column(DOUBLE(asdecimal=False))
#     Treynor_Mazuy_Coefficient = Column(DOUBLE(asdecimal=False))
#     Fee_Rate = Column(DOUBLE(asdecimal=False))


# class FundTag(Base):
#     __tablename__ = 'fund_tag'
#     transition = Column(Integer)
#     order_book_id = Column(CHAR(20))
#     symbol = Column(Text)
#     found_date = Column(Text)
#     end_date = Column(Text)
#     asset_type = Column(Text)
#     type_level_1 = Column(Text)
#     type_level_2 = Column(Text)
#     datetime = Column(CHAR(10), primary_key=True)
#     fund_id = Column(CHAR(20), primary_key=True)


# class Holdings(Base):
#    #  Manque prime key
#     __tablename__ = 'holdings'
#     ID = Column(Integer, primary_key=True)
#     order_book_id = Column(Text)
#     share_order_book_id = Column(Text)
#     type = Column(Text)
#     weight = Column(DOUBLE(asdecimal=False))
#     shares = Column(DOUBLE(asdecimal=False))
#     market_value = Column(DOUBLE(asdecimal=False))
#     symbol = Column(Text)
#     category = Column(Text)
#     region = Column(Text)
#     release_date = Column(Text)


# class FundFeeInfo(Base):
#     __tablename__ = 'fund_fee_info'
#     ID = Column(Integer, primary_key=True)
#     wind_id = Column(Text)
#     symbol = Column(Text)
#     manage_fee = Column(DOUBLE(asdecimal=False))
#     trustee_fee = Column(DOUBLE(asdecimal=False))
#     note = Column(Text)
#     fund_id = Column(Text)


# class StockTurnover(Base):
#     __tablename__ = 'stock_turnover'
#     order_book_id = Column(CHAR(20), primary_key=True)
#     today = Column(DOUBLE(asdecimal=False))
#     week = Column(DOUBLE(asdecimal=False))
#     month = Column(DOUBLE(asdecimal=False))
#     year = Column(DOUBLE(asdecimal=False))
#     current_year = Column(DOUBLE(asdecimal=False))
#     date = Column(CHAR(10), primary_key=True)


# class FundTagScore(Base):
#     __tablename__ = 'fund_tag_score'
#     fund_id = Column(CHAR(20), primary_key=True)
#     datetime = Column(CHAR(20), primary_key=True)
#     score = Column(DOUBLE(asdecimal=False))
#     tag_name = Column(VARCHAR(45))
#     score_name = Column(VARCHAR(45))
#     version = Column(Integer, primary_key=True)
#     Beta = Column(DOUBLE(asdecimal=False))
#     interval = Column(Integer, primary_key=True)
#     found_date = Column(CHAR(10))
#     end_date = Column(CHAR(10))
#     symbol = Column(VARCHAR(45))
#     is_full = Column(Integer)


# class IndexInfo(Base):
#     __tablename__ = 'index_info'
#     order_book_id = Column(CHAR(20), primary_key=True)
#     trading_hours = Column(Text)
#     symbol = Column(Text)
#     exchange = Column(Text)
#     abbrev_symbol = Column(Text)
#     round_lot = Column(DOUBLE(asdecimal=False))
#     de_listed_date = Column(Text)
#     listed_date = Column(Text)


# class IndexWeight(Base):
#     __tablename__ = 'index_weight'
#     components = Column(Text)
#     date = Column(CHAR(10), primary_key=True)
#     order_book_id = Column(CHAR(20), primary_key=True)
#     weights = Column(Text)

