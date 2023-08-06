from sqlalchemy import CHAR, Column, Integer
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.dialects.mysql import DOUBLE, DATE, TINYINT

Base = declarative_base()

class IndexVolatility(Base):
    '''指数波动率'''

    __tablename__ = 'index_volatility'
    id = Column(Integer, primary_key=True)

    index_id = Column(CHAR(20)) #指数ID
    datetime = Column(DATE) # 日期
    w1_vol = Column(DOUBLE(asdecimal=False)) # 近一周波动率
    m1_vol = Column(DOUBLE(asdecimal=False)) # 近一月波动率
    m3_vol = Column(DOUBLE(asdecimal=False)) # 近三月波动率
    m6_vol = Column(DOUBLE(asdecimal=False)) # 近半年波动率
    y1_vol = Column(DOUBLE(asdecimal=False)) # 近一年波动率
    y3_vol = Column(DOUBLE(asdecimal=False)) # 近三年波动率
    y5_vol = Column(DOUBLE(asdecimal=False)) # 近五年波动率
    y10_vol = Column(DOUBLE(asdecimal=False)) # 近十年波动率
    this_y_vol = Column(DOUBLE(asdecimal=False)) # 今年以来波动率
    cumulative_vol = Column(DOUBLE(asdecimal=False)) # 成立至今波动率


class IndexReturn(Base):
    '''指数波动率'''

    __tablename__ = 'index_return'
    id = Column(Integer, primary_key=True)

    index_id = Column(CHAR(20)) #指数ID
    datetime = Column(DATE) # 日期
    w1_ret = Column(DOUBLE(asdecimal=False)) # 近一周收益率
    m1_ret = Column(DOUBLE(asdecimal=False)) # 近一月收益率
    m3_ret = Column(DOUBLE(asdecimal=False)) # 近三月收益率
    m6_ret = Column(DOUBLE(asdecimal=False)) # 近半年收益率
    y1_ret = Column(DOUBLE(asdecimal=False)) # 近一年收益率
    y3_ret = Column(DOUBLE(asdecimal=False)) # 近三年收益率
    y5_ret = Column(DOUBLE(asdecimal=False)) # 近五年收益率
    y10_ret = Column(DOUBLE(asdecimal=False)) # 近十年收益率
    this_y_ret = Column(DOUBLE(asdecimal=False)) # 今年以来收益率
    cumulative_ret = Column(DOUBLE(asdecimal=False)) # 成立至今收益率


class FundAlpha(Base):
    '''基金超额收益'''

    __tablename__ = 'fund_alpha'
    id = Column(Integer, primary_key=True)

    track_err	= Column(DOUBLE(asdecimal=False)) # 跟踪误差
    this_y_alpha	= Column(DOUBLE(asdecimal=False)) # 今年以来超额收益
    cumulative_alpha	= Column(DOUBLE(asdecimal=False)) # 成立以来超额收益
    w1_alpha	= Column(DOUBLE(asdecimal=False)) # 近一周收益率
    m1_alpha    = Column(DOUBLE(asdecimal=False)) # 近一月超额收益
    m3_alpha	= Column(DOUBLE(asdecimal=False)) # 近三月超额收益
    m6_alpha	= Column(DOUBLE(asdecimal=False)) # 近半年超额收益
    y1_alpha	= Column(DOUBLE(asdecimal=False)) # 近一年超额收益
    y3_alpha	= Column(DOUBLE(asdecimal=False)) # 近三年超额收益
    y5_alpha	= Column(DOUBLE(asdecimal=False)) # 近五年超额收益
    y10_alpha	= Column(DOUBLE(asdecimal=False)) # 近十年超额收益
    fund_id	= Column(CHAR(20)) #基金ID
    datetime= Column(DATE) # 日期


class IndexValuation(Base):
    '''基金超额收益'''

    __tablename__ = 'index_valuation'
    id = Column(Integer, primary_key=True)
    
    index_id = Column(CHAR(20)) #指数ID
    pb_mrq = Column(DOUBLE(asdecimal=False)) # 市净率-MRQ
    pe_ttm = Column(DOUBLE(asdecimal=False)) # 市盈率-MMT
    peg_ttm = Column(DOUBLE(asdecimal=False)) # PEG-MMT
    roe_ttm = Column(DOUBLE(asdecimal=False)) # 净资产收益率-MMT
    dy_ttm = Column(DOUBLE(asdecimal=False)) # 股息率-MMT
    pe_pct = Column(DOUBLE(asdecimal=False)) # PE百分位
    pb_pct = Column(DOUBLE(asdecimal=False)) # PB百分位
    val_score = Column(DOUBLE(asdecimal=False)) # 估值评分
    datetime = Column(DATE) # 日期


class FundIndicator(Base):
    '''基金评价指标'''

    __tablename__ = 'fund_indicator'
    id = Column(Integer, primary_key=True)

    fund_id = Column(CHAR(10)) #基金ID
    datetime =  Column(DATE) # 日期

    beta = Column(DOUBLE(asdecimal=False)) #风险指数
    alpha = Column(DOUBLE(asdecimal=False)) #投资回报
    track_err = Column(DOUBLE(asdecimal=False)) #跟踪误差
    timespan = Column(DOUBLE(asdecimal=False)) #历史数据跨度(年)
    fee_rate = Column(DOUBLE(asdecimal=False)) #费率
    # treynor = Column(DOUBLE(asdecimal=False)) #特雷诺比率 
    # mdd = Column(DOUBLE(asdecimal=False)) #净值最大回撤
    # down_risk = Column(DOUBLE(asdecimal=False)) #下行风险
    # ret_over_period = Column(DOUBLE(asdecimal=False)) #区间收益率
    # annual_avg_daily_ret = Column(DOUBLE(asdecimal=False)) #年化日均收益
    # vol = Column(DOUBLE(asdecimal=False)) #波动率
    # m_square = Column(DOUBLE(asdecimal=False)) #M平方测度 风险调整收益指标
    # time_ret = Column(DOUBLE(asdecimal=False)) #择时收益
    # var = Column(DOUBLE(asdecimal=False)) #资产在险值
    # r_square = Column(DOUBLE(asdecimal=False)) #决定系数R方
    # sharpe = Column(DOUBLE(asdecimal=False)) #夏普率
    # tm_coef = Column(DOUBLE(asdecimal=False)) #风险收益指标
    

class FundScore(Base):
    '''基金评分'''

    __tablename__ = 'fund_score'
    id = Column(Integer, primary_key=True)

    fund_id = Column(CHAR(10)) #基金ID
    datetime =  Column(DATE) # 日期
    score = Column(DOUBLE(asdecimal=False)) #评分
    tag_name = Column(CHAR(64)) #基金类别
    tag_type = Column(Integer)#	1 '大类资产评分'
    tag_method = Column(CHAR(40)) #打标签版本号
    is_full = Column(Integer)#	1 true
    update_time	=  Column(DATE) # 更新时间
    score_method = Column(Integer)
    desc_name = Column(CHAR(64))

