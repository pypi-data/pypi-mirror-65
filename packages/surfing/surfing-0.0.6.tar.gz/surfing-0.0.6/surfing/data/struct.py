import dataclasses
import copy
import datetime
import numpy as np
import copy

@dataclasses.dataclass
class AssetDict:
    # 战略配置参数
    hs300: float=0.0
    csi500: float=0.0
    gem: float=0.0
    sp500rmb: float=0.0
    national_debt: float=0.0
    gold: float=0.0
    cash: float=0.0
    credit_debt: float=0.0

    def __repr__(self):
        s = f'<{self.__class__.__name__}'
        for k, v in self.__dict__.items():
            s += f' {k}={v}'
        s += '>'
        return s

    def copy(self):
        return copy.deepcopy(self)

    def isnan(self, v):
        return v is None or np.isnan(v)

@dataclasses.dataclass
class AssetWeight(AssetDict):

    def __post_init__(self):
        self.rebalance()

    def rebalance(self):
        _sum = 0.0
        for k, v in self.__dict__.items():
            assert round(v,8) >= 0, f'{k} has negative value'
            _sum += v
        assert _sum > 0, 'param sum value must be positive'
        # normalize, make sure change is correct
        for k, v in self.__dict__.items():
            self.__dict__[k] /= _sum
    
    def __repr__(self):
        s = f'<{self.__class__.__name__}'
        for k, v in self.__dict__.items():
            s += f' {k}={v*100}%'
        s += '>'
        return s

@dataclasses.dataclass
class AssetPrice(AssetDict):

    def __post_init__(self):
        for k, v in self.__dict__.items():
            assert v is None or np.isnan(v) or round(v,8) >= 0, f'{k} has negative value: {v}'
        self.cash = 1 # cash price is always 1
    
    def __repr__(self):
        s = f'<{self.__class__.__name__}'
        for k, v in self.__dict__.items():
            s += f' {k}={v}'
        s += '>'
        return s

@dataclasses.dataclass
class AssetTrade:

    index_id: str
    is_buy: bool
    mark_price: float
    submit_date: datetime.date
    amount: float=None
    volume: float=None
    trade_price: float=None
    commission: float=0.0
    trade_date: datetime.date=None

    def __post_init__(self):
        assert (self.amount and not self.volume) or (not self.amount and self.volume), \
            f'amount and volume, one and only one is valid (index){self.index_id} (vol){self.volume} (amt){self.amount}'

@dataclasses.dataclass
class AssetPosition(AssetDict):

    def __post_init__(self):
        for k, v in self.__dict__.items():
            assert round(v,8) >= 0, f'{k} has negative value: {v}'
    
    def __repr__(self):
        s = f'<{self.__class__.__name__}'
        for k, v in self.__dict__.items():
            s += f' {k}={v}'
        s += '>'
        return s

    def update(self, trd: AssetTrade):
        self.__dict__[trd.index_id] += trd.volume if trd.is_buy else -trd.volume
        amt = trd.amount if trd.amount else (trd.volume * trd.mark_price)
        self.cash += (-amt if trd.is_buy else amt) - trd.commission


@dataclasses.dataclass
class AssetValue(AssetDict):

    prices: AssetPrice=None
    positions: AssetPosition=None

    def __post_init__(self):
        for index_id, p in self.prices.__dict__.items():
            self.__dict__[index_id] = 0 if self.isnan(p) else p * self.positions.__dict__[index_id]
            # 不允许出现价格为空，但是仓位为正的情况
            assert not (self.isnan(p) and self.positions.__dict__[index_id] > 0), \
                f'price is nan but position is not zero... (index){index_id} (p){p} (pos){self.positions.__dict__[index_id]}'

    def sum(self):
        _sum = 0.0
        for k in AssetDict.__dataclass_fields__.keys():
            _sum += self.__dict__[k]
        return _sum

    def __repr__(self):
        s = f'<{self.__class__.__name__}'
        for k, v in self.__dict__.items():
            s += f' {k}={v}'
        s += '>'
        return s

    def get_weight(self):
        wgts = AssetWeight(cash=1)
        for index_id, p in self.prices.__dict__.items():
            wgts.__dict__[index_id] = self.__dict__[index_id]
        wgts.rebalance()
        return wgts
        

@dataclasses.dataclass
class FundTrade(AssetTrade):

    fund_id: str=None

@dataclasses.dataclass
class FundPosItem:

    fund_id: str            # 基金ID
    index_id: str           # 基金所属的大类资产
    volume: int             # 基金份额
    avg_cost: float=None    # 平均成本
    update_time: datetime.date=None # 更新时间

    def update(self, trade: FundTrade):
        if self.fund_id != trade.fund_id:
            return False
        if not trade.is_buy and trade.volume > self.volume:
            return False
        vol_diff = trade.volume if trade.is_buy else -trade.volume
        amt_diff = (trade.amount if trade.is_buy else -trade.amount) if trade.amount else trade.mark_price * vol_diff
        volume = self.volume + vol_diff
        amt = self.volume * self.avg_cost + amt_diff
        self.volume = volume
        self.avg_cost = amt / volume if volume > 0 else 0
        self.update_time = trade.trade_date
        return True
        
    def __repr__(self):
        return f'<{self.fund_id} (v){self.volume} (c){self.avg_cost}>'

@dataclasses.dataclass
class AssetTradeParam:

    MinCountAmtDiff: float=0.001 # 少于总资产千分之一的资产Amount差异，不计在内
    MinActionAmtDiff: float=0.03 # 如果没有资产的偏离达到这个比例，那就不调仓

@dataclasses.dataclass
class FundTradeParam:

    MaxFundNumUnderAsset: float=3 # 同一个大类资产下基金最多数
    MinCountAmtDiff: float=0.003 # 少于总资产千分之三的资产Amount差异，不做基金调仓处理
    MinActionAmtDiff: float=0.03 # 如果没有资产的基金市值偏离达到这个比例，那就不调仓

@dataclasses.dataclass
class TAAParam:

    HighThreshold: float=0.9    # 超过多少算作进入估值偏高的区域
    LowThreshold: float=0.1     # 低于多少算作进入估值偏低的区域
    HighMinus:    float=0.05    # 估值偏高时应该调低的占比
    LowPlus:      float=0.05    # 估值偏低是应该调高的占比
    HighStop:     float=0.5     # 进入估值偏高区后，什么时候算作退出
    LowStop:      float=0.5     # 进入估值偏低区后，什么时候算作退出

@dataclasses.dataclass
class FundScoreParam:
    tag_type: int=1
    score_method: int=1
    is_full: int=1

    def __repr__(self):
        return f'<fund_score_param tag_type={self.tag_type} score_method={self.score_method} is_full={self.is_full}'


class FundPosition:

    def __init__(self, cash):
        self.funds = {} # fund_id -> FundPosItem
        self.index_fund_list = {} # index_id -> [fund_id]
        self.cash = cash

    def calc_mv(self, 
                fund_navs: dict, # fund_id -> nav(adjusted net value)
                index_id=None): # filter: 只计算某个index_id
        mv = 0
        for pos_item in self.funds.values():
            if index_id and pos_item.index_id != index_id:
                continue
            nav = fund_navs.get(pos_item.fund_id, np.nan)
            if np.isnan(nav):
                print('warning!!!! nav in nan')
            else:
                mv += nav * pos_item.volume
        return mv

    def get_volume(self, fund_id):
        item = self.funds.get(fund_id)
        if not item:
            return None
        return item.volume

    def get_funds(self, index_id):
        return self.index_fund_list.get(index_id, [])

    def add(self, fund_id, index_id, volume, avg_cost, update_time):
        pos_item = FundPosItem(fund_id=fund_id, index_id=index_id, volume=volume, avg_cost=avg_cost, update_time=update_time)
        self.funds[fund_id] = pos_item
        if index_id not in self.index_fund_list:
            self.index_fund_list[index_id] = []
        self.index_fund_list[index_id].append(fund_id)
        return pos_item

    def update(self, trade: FundTrade):
        pos_item = self.funds.get(trade.fund_id)
        if pos_item is None:
            assert trade.is_buy, "fund volume cannot be negative"
            pos_item = self.add(trade.fund_id, trade.index_id, 0, 0, trade.trade_date or trade.submit_date)
            
        if pos_item.update(trade):
            amt = trade.amount if trade.amount else trade.volume * trade.mark_price
            self.cash += (-amt if trade.is_buy else amt) - trade.commission
            assert self.cash >= -1e-8, f"cash should not be negative! (cash){self.cash} (trade){trade}"
            return True
        else:
            return False

    def copy(self):
        n = FundPosition(cash=self.cash)
        n.funds = copy.deepcopy(self.funds)
        n.index_fund_list = copy.deepcopy(self.index_fund_list)
        return n

    def __repr__(self):
        s = f'<FP cash={self.cash}'
        for fund_id, pos_item in self.funds.items():
            s += f' {pos_item}'
        s += '>'
        return s

class FundScoreHelper:
    ASSET_DICT = {
        '利率债' : 'national_debt',
        '美股大盘': 'sp500rmb',
        '德国大盘': 'dax30rmb',
        '信用债': 'credit_debt',
        '房地产': 'real_state',
        'A股大盘': 'hs300',
        '原油': 'oil',
        '黄金': 'gold',
        '创业板': 'gem',
        '日本大盘': 'n225rmb',
        'A股中盘': 'csi500',
    }
    TACTIC_ASSET_CONVERT = {
        '000300.XSHG': 'hs300',
        '000905.XSHG': 'csi500'
    }

    @staticmethod
    def keys():
        return FundScoreHelper.ASSET_DICT.keys()

    @staticmethod
    def get(index_id):
        for k, v in FundScoreHelper.ASSET_DICT.items():
            if v == index_id:
                return k
        return None
    
    @staticmethod
    def parse(tag_name):
        return FundScoreHelper.ASSET_DICT.get(tag_name)

if __name__ == '__main__':
    a = AssetWeight(hs300=0.1, csi500=0.1, cash=0.8)
    print(a)