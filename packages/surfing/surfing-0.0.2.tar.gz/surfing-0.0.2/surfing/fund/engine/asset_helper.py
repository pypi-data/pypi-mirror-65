from ...data.struct import AssetWeight, AssetPrice, AssetPosition, AssetValue
from ...data.struct import TAAParam
from . import Helper


class SAAHelper(Helper):

    def __init__(self):
        pass

    def setup(self, saa: AssetWeight):
        self.saa = saa

    def on_price(self, dt, asset_price: AssetPrice):
        cur_saa = self.saa.copy()
        for k, v in asset_price.__dict__.items():
            if asset_price.isnan(v):
                cur_saa.__dict__[k] = 0
        cur_saa.rebalance()
        return cur_saa


class TAAStatusMode:
    NORMAL = 'normal'
    IN_LOW = 'low'
    IN_HIGH = 'high'

class TAAHelper(Helper):

    def __init__(self, taa_params: TAAParam=None):
        self.params = taa_params or TAAParam()
        self.tactic_status = {}

    def on_price(self, dt, asset_price: AssetPrice, cur_saa: AssetWeight, asset_pct: dict):
        taa = cur_saa.copy()
        taa_effected = False
        mode_changed = False
        for index_id, target_w in taa.__dict__.items():

            if index_id in asset_pct:
                val_pct = asset_pct[index_id]
                cur_mode = self.tactic_status.get(index_id, TAAStatusMode.NORMAL)
                new_mode = TAAStatusMode.NORMAL
                tactic_w = target_w

                if cur_mode == TAAStatusMode.NORMAL:

                    if val_pct >= self.params.HighThreshold:
                        tactic_w = max(target_w - self.params.HighMinus, 0)
                        new_mode = TAAStatusMode.IN_HIGH
                    elif val_pct <= self.params.LowThreshold:
                        tactic_w = min(target_w + self.params.LowPlus, 1)
                        new_mode = TAAStatusMode.IN_LOW
                    
                elif cur_mode == TAAStatusMode.IN_LOW:

                    if val_pct < self.params.LowStop:
                        tactic_w = min(target_w + self.params.LowPlus, 1)
                        new_mode = TAAStatusMode.IN_LOW

                elif cur_mode == TAAStatusMode.IN_HIGH:

                    if val_pct > self.params.HighStop:
                        tactic_w = max(target_w - self.params.HighMinus, 0)
                        new_mode = TAAStatusMode.IN_HIGH
                    
                else:
                    assert False, 'should not be here!'

                self.tactic_status[index_id] = new_mode
                if new_mode != TAAStatusMode.NORMAL:
                    taa.__dict__[index_id] = tactic_w

                mode_changed = mode_changed or new_mode != cur_mode
                taa_effected = taa_effected or new_mode != TAAStatusMode.NORMAL
        taa.rebalance()
        if taa_effected:
            print(f'taa: {dt} (mode){mode_changed} (taa){taa_effected} (saa){cur_saa} (taa){taa}')
        return taa

    