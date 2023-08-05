from ...data.struct import AssetWeight, AssetPrice, AssetPosition, AssetValue
from ...data.struct import AssetTrade, AssetTradeParam
from . import Helper

class AssetTrader(Helper):

    def __init__(self, param: AssetTradeParam=None):
        self.param = param or AssetTradeParam()

    def calc_trade(self, dt, cur_position: AssetPosition, cur_price: AssetPrice, target_allocation: AssetWeight):

        cur_mv = AssetValue(prices=cur_price, positions=cur_position)
        new_position = cur_position.copy()
        new_position.cash = 0
        tot_mv = cur_mv.sum()

        trades = []
        launch_trade = False
        for index_id, target_weight in target_allocation.__dict__.items():
            if index_id != 'cash':
                target_amt = tot_mv * target_weight
                p = cur_price.__dict__[index_id]
                cur_amt = cur_mv.__dict__[index_id]
                if abs(target_amt - cur_amt) > tot_mv * self.param.MinCountAmtDiff:
                    volume = abs(target_amt - cur_amt) / p
                    is_buy = target_amt > cur_amt
                    trades.append(AssetTrade(
                        index_id=index_id, 
                        mark_price=p, 
                        volume=volume, 
                        is_buy=is_buy,
                        submit_date=dt
                    ))
                    new_position.__dict__[index_id] += volume if is_buy else -volume
                launch_trade = launch_trade or abs(target_amt - cur_amt) > tot_mv * self.param.MinActionAmtDiff
        new_mv = AssetValue(prices=cur_price, positions=new_position)
        new_position.cash = tot_mv - new_mv.sum()
        
        if not launch_trade:
            return cur_position, None
        else:
            print()
            print('----', dt)
            print('old', cur_position)
            print('new', new_position)
            print('old_mv', cur_mv)
            print('new_mv', new_mv)
            print()
            return new_position, trades

    def finalize_trade(self, dt, trades: list, t1_price: AssetPrice, bt_position: AssetPosition):
        pendings = []
        if trades is None or len(trades) == 0:
            return pendings
        # TODO: if some trades needs more time
        for trd in trades:
            trd.trade_price = t1_price.__dict__[trd.index_id]
            trd.trade_date = dt
            if not trd.amount:
                trd.amount = trd.volume * trd.trade_price
            if not trd.volume:
                trd.volume = trd.amount / trd.trade_price
            # TODO: commision calculate
            #trd.commission = ?
            # update position
            bt_position.__dict__[trd.index_id] += trd.volume if trd.is_buy else -trd.volume
            bt_position.cash += (-trd.amount if trd.is_buy else trd.amount) - trd.commission

        print()
        print('trade: ', trades)
        print()

        return pendings