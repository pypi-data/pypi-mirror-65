from clean.clean_base import CleanBase
from clean.load_method import Load
from raw.download_base import Utility
from clean.clean_config import find_method_all

'''
inputs:
    1token:  data_type exchange
    btcta :  asset_type, data_type
'''
if __name__ == "__main__":
 
    begin_date       = '20190128'
    end_date         = '20191029'
    ticker           = 'huobif/btc.usd.q'
    exchange         = 'huobif'                 #1token loader parameter
    data_type        = 'ticks'
    source           = '1token'
    daily_or_monthly = 'monthly'
    folder_name      = '/Users/huangkejia/Downloads/1125' 
    asset_type       = 'None'                   #btcta loader parameter
    
    
    loader = Load(
        begin_date          = begin_date,
        end_date            = end_date,
        ticker              = ticker,
        exchange            = exchange,
        data_type           = data_type,
        source              = source,
        daily_or_monthly    = daily_or_monthly,
        folder_name         = folder_name,
        asset_type          = asset_type,
    )
    loader.load_clean_from_s3()


DAILY_BACKTEST_EXAMPLE = ['post_close', 'close','post_vwap', 'post_vwap_preclose_diff', 'st', 'post_preclose', 'suspended', 'factor_example/oversold_5', 'factor_example/singel_ticker', 'stock_pool/000300.XSHG']



