from clean.load_method import Load


if __name__ == "__main__": 
    daily_stock = ['post_close', 'index_close', 'close','post_vwap','post_open', 'post_vwap_preclose_diff', 'st', 'post_preclose', 'suspended', 'factor_example/oversold_5', 'factor_example/singel_ticker', 'stock_pool/000300.XSHG', 'stock_info']
    Load(daily_stock = daily_stock).load_daily_backtest_data()