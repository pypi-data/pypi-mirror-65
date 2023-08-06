from sqlalchemy import CHAR, Column, Integer, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.dialects.mysql import DOUBLE, DATE, TINYINT

Base = declarative_base()


class IndexInfo(Base):
    '''指数信息表'''

    __tablename__ = 'index_info'
    index_id = Column(CHAR(20), primary_key=True)

    order_book_id= Column(CHAR(20)) #米筐ID
    #web_id= Column(CHAR(20)) # 数据所在网页ID
    industry_tag= Column(CHAR(64)) # 行业标签
    tag_method= Column(CHAR(64)) # 估值评分采用方法
    desc_name= Column(CHAR(64)) # 名称

class StockInfo(Base):
    '''股票信息表'''

    __tablename__ = 'stock_info'
    stock_id = Column(CHAR(20), primary_key=True) # 股票ID
    rq_id = Column(CHAR(20)) # 米筐ID


class FundSize(Base):
    '''米筐基金最新规模'''
    
    __tablename__ = 'fund_size'

    fund_id = Column(CHAR(10), primary_key=True) # 基金id
    latest_size = Column(DOUBLE(asdecimal=False)) # 最新规模
    update_time = Column(DATE) # 更新日期


class FundInfo(Base):
    '''基金信息表'''

    __tablename__ = 'fund_info'
    fund_id = Column(CHAR(10),primary_key=True) # 基金ID
    
    wind_id = Column(CHAR(10)) # Wind基金ID
    transition = Column(Integer) # 基金变更次数
    order_book_id = Column(CHAR(10)) # RiceQuant基金ID
    desc_name = Column(CHAR(64)) # 基金名称
    start_date = Column(DATE) # 成立日期
    end_date = Column(DATE) # 关闭日期
    wind_class_1 = Column(CHAR(64)) # Wind基金类型
    wind_class_2 = Column(CHAR(64)) # Wind基金二级类型
    manager_id = Column(Text) # 基金经理
    company_id = Column(CHAR(64)) # 基金公司
    benchmark = Column(CHAR(255)) # 业绩基准
    full_name = Column(CHAR(255)) # 基金全名
    currency = Column(CHAR(20)) # 币种
    base_fund_id = Column(CHAR(20)) # 分级基金基础基金代号
    is_structured = Column(TINYINT(1)) # 是否为分级基金
    is_open = Column(TINYINT(1)) # 是否为开放式基金
    asset_type = Column(CHAR(32)) #资产类别
    update_time = Column(DATE) # 更新时间
    manage_fee = Column(DOUBLE(asdecimal=False)) # 管理费
    trustee_fee = Column(DOUBLE(asdecimal=False)) # 托管费
    purchase_fee = Column(DOUBLE(asdecimal=False)) # 申购费
    redeem_fee = Column(DOUBLE(asdecimal=False)) # 赎回费
    note = Column(CHAR(64)) # 附加信息
    track_index = Column(CHAR(20)) # 跟踪指数


class TradingDayList(Base):
    '''交易日列表'''

    __tablename__ = 'trading_day_list'
    datetime = Column(DATE, primary_key=True)


class FundNav(Base):
    '''基金净值表'''

    __tablename__ = 'fund_nav'
    fund_id = Column(CHAR(20), primary_key=True) # 合约代码
    datetime = Column(DATE, primary_key=True) # 日期

    unit_net_value = Column(DOUBLE(asdecimal=False)) # 单位净值
    acc_net_value = Column(DOUBLE(asdecimal=False)) # 累积单位净值
    adjusted_net_value = Column(DOUBLE(asdecimal=False)) # 复权净值
    change_rate = Column(DOUBLE(asdecimal=False)) # 涨跌幅
    daily_profit = Column(DOUBLE(asdecimal=False)) # 每万元收益（日结型货币基金专用）
    weekly_yield = Column(DOUBLE(asdecimal=False)) # 7日年化收益率（日结型货币基金专用）
    redeem_status = Column(Integer) # 赎回状态，开放 - Open, 暂停 - Suspended, 限制大额申赎 - Limited, 封闭期 - Close
    subscribe_status = Column(Integer) # 订阅状态，开放 - Open, 暂停 - Suspended, 限制大额申赎 - Limited, 封闭期 - Close
    order_book_id = Column(CHAR(10)) # RiceQuant基金ID
    

class IndexPrice(Base):
    '''指数价格表'''

    __tablename__ = 'index_price'
    id = Column(Integer, primary_key=True)
    # TODO: (index_id, datetime) as primary_key
    index_id = Column(CHAR(20)) # 指数id
    datetime = Column(DATE) # 日期
    volume = Column(DOUBLE(asdecimal=False)) # 交易量
    low = Column(DOUBLE(asdecimal=False)) # 最低价
    close = Column(DOUBLE(asdecimal=False)) # 收盘价
    high = Column(DOUBLE(asdecimal=False)) # 最高价
    open = Column(DOUBLE(asdecimal=False)) # 开盘价
    total_turnover = Column(DOUBLE(asdecimal=False)) # 成交额
    ret = Column(DOUBLE(asdecimal=False)) # 收益率


class StockPrice(Base):
    '''股票价格表'''

    __tablename__ = 'stock_price'
    id = Column(Integer, primary_key=True)
    # TODO: (stock_id, datetime) as primary_key
    stock_id = Column(CHAR(20)) # 指数id
    datetime = Column(DATE) # 日期
    open = Column(DOUBLE(asdecimal=False)) # 开盘价
    close = Column(DOUBLE(asdecimal=False)) # 收盘价
    high = Column(DOUBLE(asdecimal=False)) # 最高价
    low = Column(DOUBLE(asdecimal=False)) # 最低价
    limit_up = Column(DOUBLE(asdecimal=False)) # 涨停价
    limit_down = Column(DOUBLE(asdecimal=False)) # 跌停价
    total_turnover = Column(DOUBLE(asdecimal=False)) # 交易额
    volume = Column(DOUBLE(asdecimal=False)) # 交易量  
    num_trades = Column(DOUBLE(asdecimal=False)) # 交易笔数
    adj_close = Column(DOUBLE(asdecimal=False)) # 后复权价格
    post_adj_factor = Column(DOUBLE(asdecimal=False)) # 后复权因子
    ret = Column(DOUBLE(asdecimal=False)) # 日收益


class FundRet(Base):
    '''基金历史收益'''

    __tablename__ = 'fund_ret'
    id = Column(Integer, primary_key=True)
    # TODO: (fund_id, datetime) as primary_key
    fund_id = Column(CHAR(10)) # 原始基金ID
    datetime = Column(DATE) # 日期
    w1_ret = Column(DOUBLE(asdecimal=False)) # 近一周收益率
    m1_ret = Column(DOUBLE(asdecimal=False)) # 近一月收益率
    m3_ret = Column(DOUBLE(asdecimal=False)) # 近一季度收益率
    m6_ret = Column(DOUBLE(asdecimal=False)) # 近半年收益率
    y1_ret = Column(DOUBLE(asdecimal=False)) # 近一年收益率
    mdd = Column(DOUBLE(asdecimal=False)) # 最大回撤（成立以来）
    annual_ret = Column(DOUBLE(asdecimal=False)) # 年化收益（成立以来）
    avg_size = Column(DOUBLE(asdecimal=False)) # 平均规模（成立以来）
    sharpe_ratio = Column(DOUBLE(asdecimal=False)) # 夏普率（成立以来）
    info_ratio = Column(DOUBLE(asdecimal=False)) # 夏普率（成立以来）


class FundRatingLatest(Base):
    '''基金最新评级'''
    

    __tablename__ = 'fund_rating_latest'

    fund_id = Column(CHAR(10), primary_key=True)  # 基金id
    zs = Column(DOUBLE(asdecimal=False))  # 招商评级
    sh3 = Column(DOUBLE(asdecimal=False))  # 上海证券评级三年期
    sh5 = Column(DOUBLE(asdecimal=False))  # 上海证券评级五年期
    jajx = Column(DOUBLE(asdecimal=False))  # 济安金信评级
    update_time = Column(DATE)  # 更新日期


