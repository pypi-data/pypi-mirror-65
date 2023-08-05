from sqlalchemy import CHAR, Column, Integer
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.dialects.mysql import DOUBLE

Base = declarative_base()


class FundIndicator(Base):
    '''基金指标'''

    __tablename__ = 'fund_indicator'
    id = Column(Integer, primary_key=True)

    fund_id = Column(CHAR(20)) # 基金ID
    datetime = Column(CHAR(10)) # 日期
    beta = Column(DOUBLE(asdecimal=False)) # 风险指数
    alpha = Column(DOUBLE(asdecimal=False)) # 投资回报
    treynor_ratio = Column(DOUBLE(asdecimal=False)) # 特雷诺比率 基金承担单位系统风险所获得的超额收益
    max_dd = Column(DOUBLE(asdecimal=False)) # 净值最大回撤
    downside_risk = Column(DOUBLE(asdecimal=False)) # 下行风险
    return_over_period = Column(DOUBLE(asdecimal=False)) # 区间收益率
    annualized_average_daily_return = Column(DOUBLE(asdecimal=False)) # 年化日均收益
    volatility = Column(DOUBLE(asdecimal=False)) # 波动率
    m_square = Column(DOUBLE(asdecimal=False)) # M平方测度 风险调整收益指标
    time_return = Column(DOUBLE(asdecimal=False)) # 择时收益
    value_at_risk = Column(DOUBLE(asdecimal=False)) # 资产在险值
    r_square = Column(DOUBLE(asdecimal=False)) # 决定系数R方，基金收益波动的方差中，受市场决定的比例
    sharp_ratio = Column(DOUBLE(asdecimal=False)) # 夏普率
    treynor_mazuy_coefficient = Column(DOUBLE(asdecimal=False)) # 风险收益指标
    fee_rate = Column(DOUBLE(asdecimal=False)) # 费率
    track_error = Column(DOUBLE(asdecimal=False)) # 跟踪误差
    timespan = Column(Integer) # 历史数据跨度(年)
    

class StockBarraFactorCrowding(Base):
    '''股票 Barra 因子拥挤度'''

    __tablename__ = 'factor_crowding_stock_barra'
    id = Column(Integer, primary_key=True)

    factor_volatility = Column(DOUBLE(asdecimal=False)) # 多空波动率比率
    long_term_factor_ret = Column(DOUBLE(asdecimal=False)) # 长期累积收益
    pairwise_correlation = Column(DOUBLE(asdecimal=False)) # 配对相关性
    valuation_spread = Column(DOUBLE(asdecimal=False)) # 估值价差
    barra_factor_type = Column(CHAR(32)) # Barra 因子类型 (BarraFactorType Enum)
    datetime = Column(CHAR(10)) # 日期


class StockBarraFactor(Base):
    '''股票 Barra 因子'''

    __tablename__ = 'stock_barra'
    id = Column(Integer, primary_key=True)

    order_book_id = Column(CHAR(32)) # 股票代码
    factor_value = Column(DOUBLE(asdecimal=False)) # 因子取值
    barra_factor_type = Column(CHAR(32)) # Barra 因子类型 (BarraFactorType Enum)
    datetime = Column(CHAR(10)) # 日期


class FundTagScore(Base):
    '''基金评分'''

    __tablename__ = 'fund_tag_score'
    id = Column(Integer, primary_key=True)

    fund_id = Column(CHAR(20)) # 基金ID
    datetime = Column(CHAR(10)) # 日期
    score = Column(DOUBLE(asdecimal=False)) # 评分
    tag_name = Column(CHAR(64)) # 基金类别
    score_name = Column(CHAR(64)) # 评分名
    beta = Column(DOUBLE(asdecimal=False)) # 风险指数
    timespan = Column(Integer) # 历史数据跨度
    found_date = Column(CHAR(10)) # 基金成立日 TODO, 可从此表删除
    end_date = Column(CHAR(10)) # 基金终止日 TODO, 可从此表删除
    symbol = Column(CHAR(64)) # 中文简称 TODO, 可从此表删除
    is_full = Column(Integer) # 评分所用历史数据是否充足


class IndustryPE(Base):
    '''行业估值'''

    __tablename__ = 'industry_pe'
    id = Column(Integer, primary_key=True)

    industry_name = Column(CHAR(20)) # 行业名称
    datetime = Column(CHAR(10)) # 日期
    p = Column(DOUBLE(asdecimal=False)) # 行业总市值
    e = Column(DOUBLE(asdecimal=False)) # 行业总利润
    pe = Column(DOUBLE(asdecimal=False)) # 行业市盈率
    peq = Column(DOUBLE(asdecimal=False)) # 行业市盈率百分位
    num_stock = Column(DOUBLE(asdecimal=False)) # 行业内股票数


class StockLatestNetProfit(Base):
    '''股票最新年度净利润'''

    __tablename__ = 'industry_pe_stock_latest_net_profit'
    id = Column(Integer, primary_key=True)

    order_book_id = Column(CHAR(20))  # 行业名称
    datetime = Column(CHAR(10))  # 上次程序内数据更新日期
    quarter = Column(CHAR(10))  # 最近季度
    net_profit = Column(DOUBLE(asdecimal=False))  # 年度净利润TTM


class AssetAllocationBacktestResult(Base):
    '''大类资产回测历史'''

    __tablename__ = 'asset_allocation_bactest_result'
    id = Column(Integer, primary_key=True) 

    mdd = Column(DOUBLE(asdecimal=False)) #最大回撤
    annual_ret = Column(DOUBLE(asdecimal=False)) #年化收益
    sharpe = Column(DOUBLE(asdecimal=False)) #夏普率  
    recent_5_years_ret = Column(DOUBLE(asdecimal=False)) #最近5年累积收益率
    annual_vol = Column(DOUBLE(asdecimal=False)) # 年化波动率
    mdd_d1 = Column(CHAR(10)) # 最大回撤开始日
    mdd_d2 = Column(CHAR(10)) # 最大回撤结束日
    credit_debt = Column(DOUBLE(asdecimal=False)) #信用债权重
    national_debt = Column(DOUBLE(asdecimal=False)) #国债权重
    csi500 = Column(DOUBLE(asdecimal=False)) #中证500权重
    sp500rmb = Column(DOUBLE(asdecimal=False)) #标普500权重
    gold = Column(DOUBLE(asdecimal=False)) #黄金权重 


class AssetAllocationResult(Base):
    '''十档大类资产分配'''

    __tablename__ = 'asset_allocation_result'
    id = Column(Integer, primary_key=True) 

    mdd = Column(DOUBLE(asdecimal=False)) #最大回撤
    annual_ret = Column(DOUBLE(asdecimal=False)) #年化收益
    sharpe = Column(DOUBLE(asdecimal=False)) #夏普率  
    recent_5_years_ret = Column(DOUBLE(asdecimal=False)) #最近5年累积收益率
    annual_vol = Column(DOUBLE(asdecimal=False)) # 年化波动率
    mdd_d1 = Column(CHAR(10)) # 最大回撤开始日
    mdd_d2 = Column(CHAR(10)) # 最大回撤结束日
    credit_debt = Column(DOUBLE(asdecimal=False)) #信用债权重
    national_debt = Column(DOUBLE(asdecimal=False)) #国债权重
    csi500 = Column(DOUBLE(asdecimal=False)) #中证500权重
    sp500rmb = Column(DOUBLE(asdecimal=False)) #标普500权重
    gold = Column(DOUBLE(asdecimal=False)) #黄金权重


class FundDailyCollection(Base):
    """基金信息日度收集"""

    __tablename__ = 'fund_daily_collection'
    id = Column(Integer, primary_key=True)

    datetime = Column(CHAR(20))  # 时间
    fund_id = Column(CHAR(20))  # 基金ID
    order_book_id = Column(CHAR(20))  # 基金代码

    wind_class_I = Column(CHAR(64))  # Wind基金类型
    wind_class_II = Column(CHAR(64))  # Wind基金二级类型
    institution_rating = Column(CHAR(20))  # 机构评级
    found_to_now = Column(DOUBLE(asdecimal=False))  # 成立年限
    average_size = Column(DOUBLE(asdecimal=False))  # 平均规模
    exchange_status = Column(CHAR(20))  # 交易状态
    theme = Column(CHAR(20))  # 基金主题

    nav = Column(DOUBLE(asdecimal=False)) # 净值
    found_date = Column(CHAR(20))  # 成立日期
    annualized_returns = Column(DOUBLE(asdecimal=False))  # 成立以来年化收益率
    annualized_risk = Column(DOUBLE(asdecimal=False))  # 成立以来年化风险
    information_ratio = Column(DOUBLE(asdecimal=False))  # 成立以来信息比率
    last_month_return = Column(DOUBLE(asdecimal=False))  # 近一月收益率
    last_six_month_return = Column(DOUBLE(asdecimal=False))
    last_three_month_return = Column(DOUBLE(asdecimal=False))  # 近一季度收益率
    last_twelve_month_return = Column(DOUBLE(asdecimal=False))  # 近一年收益率
    last_week_return = Column(DOUBLE(asdecimal=False))  # 近一周收益率
    year_to_date_return = Column(DOUBLE(asdecimal=False))  # 今年以来收益率
    to_date_return = Column(DOUBLE(asdecimal=False))  # 成立至今收益率
    sharp_ratio = Column(DOUBLE(asdecimal=False))  # 成立至今夏普比率
    max_drop_down = Column(DOUBLE(asdecimal=False))  # 成立至今最大回撤

    fund_manager = Column(CHAR(255))  # 基金经理
    company_name = Column(CHAR(64))  # 基金公司
    symbol = Column(CHAR(64)) # 基金名称
    benchmark = Column(CHAR(255)) # 业绩基准

    @staticmethod
    def trans_columns():
        return {
            'fund_id': '基金ID',
            'order_book_id': '基金代码',
            'wind_class_I': '基金类型',
            'symbol': '基金名称',
            'institution_rating': '机构评级',
            'found_to_now': '成立年限',
            'average_size': '基金规模',
            'exchange_status': '交易状态',
            'nav': '净值',
            'found_date': '成立日期',
            'annualized_returns': '年化收益',
            'annualized_risk': '成立以来年化风险',
            'information_ratio': '成立以来信息比率',
            'last_week_return': '近1周',
            'last_month_return': '近1月',
            'last_three_month_return': '近3月',
            'last_six_month_return': '近半年',
            'last_twelve_month_return': '近1年',
            'year_to_date_return': '年初至今',
            'to_date_return': '成立至今',
            'sharp_ratio': '夏普比率',
            'max_drop_down': '最大回撤',
            'fund_manager': '基金经理',
            'company_name': '基金公司',
            'benchmark': '业绩基准',
        }

