from raw.download_1token import Download1Token

"""
    'a365mex', 'anchor', 'basefex', 'bequant', 'bibox', 'bigone', 'biki', 'binance', 
    'binancef', 'bitbank', 'bitfinex', 'bitflyer', 'bitflyex', 'bitforex', 'bitget', 
    'bithumb', 'bitmax', 'bitmex', 'bitstamp', 'bittrex', 'bitz', 'biz', 'btcbox', 
    'bybit', 'cobinhood', 'coinbase', 'coinbene', 'coinbeneswap', 'coincheck', 'coinegg', 
    'coinex', 'coinone', 'coint', 'copyfuntest', 'currency', 'deribit', 'fcoin', 'ftxf', 
    'gaea', 'gaef', 'gate', 'gemini', 'gopax', 'hbjp', 'hbus', 'hcoin', 'hiex', 'hoo', 
    'huobif', 'huobiflimit', 'huobiotc', 'huobip', 'itbit', 'jexop', 'korbit', 'kraken', 
    'kucoin', 'kumex', 'lark', 'lazy', 'lbank', 'lbc', 'match', 'matchfmock', 'middle', 
    'mxc', 'okef', 'okeflimit', 'okex', 'okswap', 'okusd', 'piexgo', 'poloniex', 
    'quoinex', 'rightbtc', 'sinax', 'ublex', 'upbit', 'zaif', 'zb' 
"""

def get_contract(date=None, check_exchange=None):
    res = Download1Token().download_contract_list(date)   
    exchange_list = []
    for i in res:
        exchange_list.append(i.split('/')[0])
    exchange_list = sorted(list(set(exchange_list)))
    
    if check_exchange is None:
        print('exchange_list')
        print(exchange_list)
    else:
        result = []
        for i in res:
            if i.split('/')[0] == check_exchange:
                result.append(i)
        result = sorted(result)
        print('contract')
        print(result)

if __name__ == "__main__":
    
    date = '20191110'
    exchange = 'huobif'
    get_contract(date)
    get_contract(date,exchange)
    