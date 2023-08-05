from sqlalchemy import CHAR, Column, Integer, TEXT
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.dialects.mysql import DOUBLE, DATE, TINYINT

Base = declarative_base()



class WindFundInfo(Base):
    '''万徳基金信息表'''

    __tablename__ = 'wind_fund_info'
    id = Column(Integer, primary_key=True)

    wind_id = Column(CHAR(20)) # 基金代码
    desc_name = Column(CHAR(64)) # 基金名称
    full_name = Column(CHAR(255)) #基金全称
    start_date = Column(DATE) # 成立日期
    end_date = Column(DATE) # 结束日期
    benchmark = Column(CHAR(255)) # 业绩比较基准
    wind_class_1 = Column(CHAR(64)) # wind投资分类一级
    wind_class_2 = Column(CHAR(64)) # wind投资分类二级
    currency = Column(CHAR(20)) # 交易币种
    base_fund_id = Column(CHAR(20)) # 分级基金母基金代码
    is_structured = Column(TINYINT(1)) # 是否分级基金
    is_open = Column(TINYINT(1)) # 是否定期开放基金
    manager_id = Column(CHAR(255)) # 基金经理(历任)
    company_id = Column(CHAR(64)) # 基金公司


class RqStockPrice(Base):
    '''米筐股票不复权数据表'''

    __tablename__ = 'rq_stock_price'
    id = Column(Integer, primary_key=True)

    open = Column(DOUBLE(asdecimal=False)) # 开盘价
    close = Column(DOUBLE(asdecimal=False)) # 收盘价
    high = Column(DOUBLE(asdecimal=False)) # 最高价
    low = Column(DOUBLE(asdecimal=False)) # 最低价
    limit_up = Column(DOUBLE(asdecimal=False)) # 涨停价
    limit_down = Column(DOUBLE(asdecimal=False)) # 跌停价
    total_turnover = Column(DOUBLE(asdecimal=False)) # 交易额
    volume = Column(DOUBLE(asdecimal=False)) # 交易量  不复权和后复权的交易量不同
    num_trades = Column(DOUBLE(asdecimal=False)) # 交易笔数
    datetime = Column(DATE) # 日期
    order_book_id = Column(CHAR(20)) # 股票ID
    
    
class RqStockPostPrice(Base):
    '''米筐股票后复权数据表'''

    __tablename__ = 'rq_stock_post_price'
    id = Column(Integer, primary_key=True)

    open = Column(DOUBLE(asdecimal=False)) # 开盘价
    close = Column(DOUBLE(asdecimal=False)) # 收盘价
    high = Column(DOUBLE(asdecimal=False)) # 最高价
    low = Column(DOUBLE(asdecimal=False)) # 最低价
    limit_up = Column(DOUBLE(asdecimal=False)) # 涨停价
    limit_down = Column(DOUBLE(asdecimal=False)) # 跌停价
    total_turnover = Column(DOUBLE(asdecimal=False)) # 交易额
    volume = Column(DOUBLE(asdecimal=False)) # 交易量  不复权和后复权的交易量不同
    num_trades = Column(DOUBLE(asdecimal=False)) # 交易笔数
    datetime = Column(DATE) # 日期
    order_book_id = Column(CHAR(20)) # 股票ID


class RqFundNav(Base):
    '''米筐基金净值表'''

    __tablename__ = 'rq_fund_nav'
    order_book_id = Column(CHAR(10), primary_key=True) # 合约代码
    datetime = Column(DATE, primary_key=True) # 日期

    unit_net_value = Column(DOUBLE(asdecimal=False)) # 单位净值
    acc_net_value = Column(DOUBLE(asdecimal=False)) # 累积单位净值
    adjusted_net_value = Column(DOUBLE(asdecimal=False)) # 复权净值
    change_rate = Column(DOUBLE(asdecimal=False)) # 涨跌幅
    daily_profit = Column(DOUBLE(asdecimal=False)) # 每万元收益（日结型货币基金专用）
    weekly_yield = Column(DOUBLE(asdecimal=False)) # 7日年化收益率（日结型货币基金专用）
    redeem_status = Column(CHAR(10)) # 赎回状态，开放 - Open, 暂停 - Suspended, 限制大额申赎 - Limited, 封闭期 - Close
    subscribe_status = Column(CHAR(10)) # 订阅状态，开放 - Open, 暂停 - Suspended, 限制大额申赎 - Limited, 封闭期 - Close
    
    
class RqStockValuation(Base):
    '''
    股票每日估值
    LF, Last File 时效性最好
    LYR, Last Year Ratio 上市公司年报有审计要求，数据可靠性最高
    TTM, Trailing Twelve Months 时效性较好，滚动4个报告期计算，可避免某一期财报数据的偶然性
    '''

    __tablename__ = 'rq_stock_valuation'
    id = Column(Integer, primary_key=True)

    stock_id = Column(CHAR(20)) # 股票id
    datetime = Column(DATE) # 日期
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
    

class RqFundIndicator(Base):
    '''米筐基金指标'''

    __tablename__ = 'rq_fund_indicator'
    id = Column(Integer, primary_key=True)

    order_book_id = Column(CHAR(10)) # 原始基金ID
    datetime = Column(DATE) # 日期

    last_week_return= Column(DOUBLE(asdecimal=False)) # 近一周收益率
    last_month_return= Column(DOUBLE(asdecimal=False)) # 近一月收益率
    last_three_month_return= Column(DOUBLE(asdecimal=False)) # 近一季度收益率
    last_six_month_return= Column(DOUBLE(asdecimal=False)) # 近半年收益率
    last_twelve_month_return= Column(DOUBLE(asdecimal=False)) # 近一年收益率
    year_to_date_return= Column(DOUBLE(asdecimal=False)) # 今年以来收益率
    to_date_return= Column(DOUBLE(asdecimal=False)) # 成立至今收益率
    average_size= Column(DOUBLE(asdecimal=False)) # 平均规模
    annualized_returns= Column(DOUBLE(asdecimal=False)) # 成立以来年化收益率
    annualized_risk= Column(DOUBLE(asdecimal=False)) # 成立以来年化风险
    sharp_ratio= Column(DOUBLE(asdecimal=False)) # 成立以来夏普比率
    max_drop_down= Column(DOUBLE(asdecimal=False)) # 成立以来最大回撤
    information_ratio= Column(DOUBLE(asdecimal=False)) # 成立以来信息比率


class RqIndexPrice(Base):
    '''米筐指数数据'''

    __tablename__ = 'rq_index_price'
    id = Column(Integer, primary_key=True)

    datetime = Column(DATE) # 日期
    order_book_id = Column(CHAR(20)) # 米筐代码
    high = Column(DOUBLE(asdecimal=False)) #最高价
    open = Column(DOUBLE(asdecimal=False)) #开盘价
    total_turnover = Column(DOUBLE(asdecimal=False)) # 交易额
    low = Column(DOUBLE(asdecimal=False)) # 最低价
    close = Column(DOUBLE(asdecimal=False)) # 收盘价
    volume = Column(DOUBLE(asdecimal=False)) # 交易量

class FundFee(Base):
    '''基金费率表'''

    __tablename__ = 'fund_fee'
    id = Column(Integer, primary_key=True)

    desc_name = Column(CHAR(32)) # 名称
    manage_fee = Column(DOUBLE(asdecimal=False)) # 管理费
    trustee_fee = Column(DOUBLE(asdecimal=False)) # 托管费
    purchase_fee = Column(DOUBLE(asdecimal=False)) # 申购费
    redeem_fee = Column(DOUBLE(asdecimal=False)) # 赎回费
    note = Column(CHAR(64)) # 附加信息
    fund_id = Column(CHAR(20)) # 基金id


class CxindexIndexPrice(Base):
    '''中证指数数据'''

    __tablename__ = 'cxindex_index_price'
    id = Column(Integer, primary_key=True)

    index_id = Column(CHAR(20)) # 指数名称
    datetime = Column(DATE) # 日期
    open = Column(DOUBLE(asdecimal=False)) # 开盘价
    close = Column(DOUBLE(asdecimal=False)) # 收盘价
    high = Column(DOUBLE(asdecimal=False)) # 最高价
    low = Column(DOUBLE(asdecimal=False)) # 最低价
    volume = Column(DOUBLE(asdecimal=False)) # 交易量
    total_turnover = Column(DOUBLE(asdecimal=False)) # 交易额
    ret = Column(DOUBLE(asdecimal=False)) # 收益率
    

class YahooIndexPrice(Base):
    '''雅虎指数数据'''

    __tablename__ = 'yahoo_index_price'
    id = Column(Integer, primary_key=True)

    index_id = Column(CHAR(20)) # 指数名称
    datetime = Column(DATE) # 日期
    open = Column(DOUBLE(asdecimal=False)) # 开盘价
    close = Column(DOUBLE(asdecimal=False)) # 收盘价
    high = Column(DOUBLE(asdecimal=False)) # 最高价
    low = Column(DOUBLE(asdecimal=False)) # 最低价
    volume = Column(DOUBLE(asdecimal=False)) # 交易量
    total_turnover = Column(DOUBLE(asdecimal=False)) # 交易额
    ret = Column(DOUBLE(asdecimal=False)) # 收益率


class CmIndexPrice(Base):
    '''汇率数据'''

    __tablename__ = 'cm_index_price'
    datetime = Column(DATE, primary_key=True) # 日期

    usd_central_parity_rate = Column(DOUBLE(asdecimal=False)) # 美元人民币汇率中间价
    eur_central_parity_rate = Column(DOUBLE(asdecimal=False)) # 欧元人民币汇率中间价
    jpy_central_parity_rate = Column(DOUBLE(asdecimal=False)) # 日元人民币汇率中间价
    usd_cfets = Column(DOUBLE(asdecimal=False)) # 美元人民币市询价
    eur_cfets = Column(DOUBLE(asdecimal=False)) # 欧元人民币市询价
    jpy_cfets = Column(DOUBLE(asdecimal=False)) # 日元人民币市询价


class FundRating(Base):
    '''基金评级'''

    __tablename__ = 'fund_rating'
    id = Column(Integer, primary_key=True)

    order_book_id = Column(CHAR(10)) # 米筐基金id
    datetime = Column(DATE) # 日期
    zs = Column(DOUBLE(asdecimal=False)) # 招商评级
    sh3 = Column(DOUBLE(asdecimal=False)) # 上海证券评级三年期
    sh5 = Column(DOUBLE(asdecimal=False)) # 上海证券评级五年期
    jajx = Column(DOUBLE(asdecimal=False)) # 济安金信评级


class RqIndexWeight(Base):
    '''指数成分权重'''

    __tablename__ = 'rq_index_weight'
    id = Column(Integer, primary_key=True)

    datetime = Column(DATE) # 日期
    index_id = Column(CHAR(20)) # 股票
    weight_list = Column(TEXT) # 权重列表 json 格式str 两者顺位对应
    stock_list = Column(TEXT) # 股票列表 json 格式str 两者顺位对应


class RqStockFinFac(Base):
    '''米筐股票财务因子'''

    __tablename__ = 'rq_stock_fin_fac'
    id = Column(Integer, primary_key=True)

    datetime = Column(DATE) # 日期
    stock_id =  Column(CHAR(20)) # 股票
    return_on_equity_ttm = Column(DOUBLE(asdecimal=False)) # 净资产收益率ttm
    

class RqFundSize(Base):
    '''米筐基金最新规模'''
    
    __tablename__ = 'rq_fund_size'
    order_book_id = Column(CHAR(10), primary_key=True) # 米筐基金id
    latest_size = Column(DOUBLE(asdecimal=False)) # 最新规模
    update_time = Column(DATE) # 更新日期


class StockInfo(Base):
    '''股票信息表'''

    __tablename__ = 'rq_stock_info'
    stock_id = Column(CHAR(20), primary_key=True) # 股票ID
    rq_id = Column(CHAR(20)) # 米筐ID


class TradingDayList(Base):
    '''交易日列表'''

    __tablename__ = 'rq_trading_day_list'
    datetime = Column(DATE, primary_key=True)


class IndexValPct(Base):
    '''指数估值'''
    
    __tablename__ = 'index_valpct'
    
    id = Column(Integer, primary_key=True)
    datetime = Column(DATE) # 更新日期
    index_id = Column(CHAR(20)) # 指数
    pe_ratio_ttm  = Column(DOUBLE(asdecimal=False)) # pe
    pe_pct = Column(DOUBLE(asdecimal=False)) # pe 百分位
    
