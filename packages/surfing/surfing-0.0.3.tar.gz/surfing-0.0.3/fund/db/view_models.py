from sqlalchemy import CHAR, Column, Integer, DATE
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.dialects.mysql import DOUBLE

Base = declarative_base()


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
    track_index = Column(CHAR(20)) # 跟踪指数

    unit_net_value = Column(DOUBLE(asdecimal=False))  # 单位净值
    acc_net_value = Column(DOUBLE(asdecimal=False))  # 累积单位净值
    adjusted_net_value = Column(DOUBLE(asdecimal=False))  # 复权净值
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

    zs = Column(DOUBLE(asdecimal=False))  # 招商评级
    sh3 = Column(DOUBLE(asdecimal=False))  # 上海证券评级三年期
    sh5 = Column(DOUBLE(asdecimal=False))  # 上海证券评级五年期
    jajx = Column(DOUBLE(asdecimal=False))  # 济安金信评级

    track_err = Column(DOUBLE(asdecimal=False))  # 跟踪误差
    this_y_alpha = Column(DOUBLE(asdecimal=False))  # 今年以来超额收益
    cumulative_alpha = Column(DOUBLE(asdecimal=False))  # 成立以来超额收益
    w1_alpha = Column(DOUBLE(asdecimal=False))  # 近一周收益率
    m1_alpha = Column(DOUBLE(asdecimal=False))  # 近一月超额收益
    m3_alpha = Column(DOUBLE(asdecimal=False))  # 近三月超额收益
    m6_alpha = Column(DOUBLE(asdecimal=False))  # 近半年超额收益
    y1_alpha = Column(DOUBLE(asdecimal=False))  # 近一年超额收益
    y3_alpha = Column(DOUBLE(asdecimal=False))  # 近三年超额收益
    y5_alpha = Column(DOUBLE(asdecimal=False))  # 近五年超额收益
    y10_alpha = Column(DOUBLE(asdecimal=False))  # 近十年超额收益

    latest_size = Column(DOUBLE(asdecimal=False)) # 最新规模

    beta = Column(DOUBLE(asdecimal=False))  # 风险指数
    alpha = Column(DOUBLE(asdecimal=False))  # 投资回报
    tag_track_err = Column(DOUBLE(asdecimal=False))  # tag跟踪误差
    fee_rate = Column(DOUBLE(asdecimal=False))  # 费率

    tag_name = Column(CHAR(64)) #基金类别
    score = Column(DOUBLE(asdecimal=False)) #评分

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
            'track_index': '跟踪指数',

            'exchange_status': '交易状态',
            'theme': '基金主题',
            'adjusted_net_value': '累计净值',
            'unit_net_value': '净值',
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
            'zs': '招商评级',
            'sh3': '上证三年评级',
            'sh5': '上证五年评级',
            'jajx': '济安评级',

            'track_err': '跟踪误差',
            'this_y_alpha': '今年以来超额收益',
            'cumulative_alpha': '成立以来超额收益',
            'w1_alpha': '近一周收益率',
            'm1_alpha': '近一月超额收益',
            'm3_alpha': '近三月超额收益',
            'm6_alpha': '近半年超额收益',
            'y1_alpha': '近一年超额收益',
            'y3_alpha': '近三年超额收益',
            'y5_alpha': '近五年超额收益',
            'y10_alpha': '近十年超额收益',
            'latest_size': '最新规模',

            'beta': 'beta',
            'alpha': 'alpha',
            'tag_track_err': 'tag跟踪误差',
            'fee_rate': '费率',
            'tag_name': '基金类别',
            'score': '基金评分',
        }


class IndexDailyCollection(Base):
    """基金信息日度收集"""

    __tablename__ = 'index_daily_collection'
    id = Column(Integer, primary_key=True)

    index_id = Column(CHAR(20))  # 指数ID
    datetime = Column(DATE)  # 日期
    pb_mrq = Column(DOUBLE(asdecimal=False))  # 市净率-MRQ
    pe_ttm = Column(DOUBLE(asdecimal=False))  # 市盈率-MMT
    peg_ttm = Column(DOUBLE(asdecimal=False))  # PEG-MMT
    roe_ttm = Column(DOUBLE(asdecimal=False))  # 净资产收益率-MMT
    dy_ttm = Column(DOUBLE(asdecimal=False))  # 股息率-MMT
    pe_pct = Column(DOUBLE(asdecimal=False))  # PE百分位
    pb_pct = Column(DOUBLE(asdecimal=False))  # PB百分位
    val_score = Column(DOUBLE(asdecimal=False))  # 估值评分

    vol_datetime = Column(DATE)  # 日期
    w1_vol = Column(DOUBLE(asdecimal=False))  # 近一周波动率
    m1_vol = Column(DOUBLE(asdecimal=False))  # 近一月波动率
    m3_vol = Column(DOUBLE(asdecimal=False))  # 近三月波动率
    m6_vol = Column(DOUBLE(asdecimal=False))  # 近半年波动率
    y1_vol = Column(DOUBLE(asdecimal=False))  # 近一年波动率
    y3_vol = Column(DOUBLE(asdecimal=False))  # 近三年波动率
    y5_vol = Column(DOUBLE(asdecimal=False))  # 近五年波动率
    y10_vol = Column(DOUBLE(asdecimal=False))  # 近十年波动率
    this_y_vol = Column(DOUBLE(asdecimal=False))  # 今年以来波动率
    cumulative_vol = Column(DOUBLE(asdecimal=False))  # 成立至今波动率

    ret_datetime = Column(DATE)  # 日期
    w1_ret = Column(DOUBLE(asdecimal=False))  # 近一周收益率
    m1_ret = Column(DOUBLE(asdecimal=False))  # 近一月收益率
    m3_ret = Column(DOUBLE(asdecimal=False))  # 近三月收益率
    m6_ret = Column(DOUBLE(asdecimal=False))  # 近半年收益率
    y1_ret = Column(DOUBLE(asdecimal=False))  # 近一年收益率
    y3_ret = Column(DOUBLE(asdecimal=False))  # 近三年收益率
    y5_ret = Column(DOUBLE(asdecimal=False))  # 近五年收益率
    y10_ret = Column(DOUBLE(asdecimal=False))  # 近十年收益率
    this_y_ret = Column(DOUBLE(asdecimal=False))  # 今年以来收益率
    cumulative_ret = Column(DOUBLE(asdecimal=False))  # 成立至今收益率

    price_datetime = Column(DATE)  # 日期
    volume = Column(DOUBLE(asdecimal=False))  # 交易量
    low = Column(DOUBLE(asdecimal=False))  # 最低价
    close = Column(DOUBLE(asdecimal=False))  # 收盘价
    high = Column(DOUBLE(asdecimal=False))  # 最高价
    open = Column(DOUBLE(asdecimal=False))  # 开盘价
    total_turnover = Column(DOUBLE(asdecimal=False))  # 成交额
    ret = Column(DOUBLE(asdecimal=False))  # 收益率

    order_book_id = Column(CHAR(20))  # 米筐ID
    industry_tag = Column(CHAR(64))  # 行业标签
    tag_method = Column(CHAR(64))  # 估值评分采用方法
    desc_name = Column(CHAR(64))  # 名称

    @staticmethod
    def trans_columns():
        return {
            'index_id': '指数ID',
            'datetime': '日期',
            'w1_vol': '近一周波动率',
            'm1_vol': '近一月波动率',
            'm3_vol': '近三月波动率',
            'm6_vol': '近半年波动率',
            'y1_vol': '近一年波动率',
            'y3_vol': '近三年波动率',
            'y5_vol': '近五年波动率',
            'y10_vol': '近十年波动率',
            'this_y_vol': '今年以来波动率',
            'cumulative_vol': '成立至今波动率',

            'ret_datetime': 'ret日期',
            'w1_ret': '近一周收益率',
            'm1_ret': '近一月收益率',
            'm3_ret': '近三月收益率',
            'm6_ret': '近半年收益率',
            'y1_ret': '近一年收益率',
            'y3_ret': '近三年收益率',
            'y5_ret': '近五年收益率',
            'y10_ret': '近十年收益率',
            'this_y_ret': '今年以来收益率',
            'cumulative_ret': '成立至今收益率',

            'pb_mrq': 'PB',
            'pe_ttm': 'PE',
            'peg_ttm': '预测PEG',
            'roe_ttm': 'ROE',
            'dy_ttm': '股息率',
            'pe_pct': 'PE百分位',
            'pb_pct': 'PB百分位',
            'val_score': '估值评分',
            'alpha_datetime': 'alpha日期',

            'price_datetime': '价格日期',
            'volume': '交易量',
            'low': '最低价',
            'close': '收盘价',
            'high': '最高价',
            'open': '开盘价',
            'total_turnover': '成交额',
            'ret': '收益率',

            'order_book_id': '指数代码',
            'industry_tag': '行业标签',
            'tag_method': '估值评分采用方法',
            'desc_name': '指数名称',
        }



