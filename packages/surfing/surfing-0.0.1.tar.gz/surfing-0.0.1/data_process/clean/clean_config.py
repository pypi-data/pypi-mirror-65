from .clean_method import *

METHOD_1Token = {
    'ticks':{   
        'default'   :   OneTokenTicksClean,
        'okef'      :   OkefTicksClean,
        'huobif'    :   OkefTicksClean,
    },    
    'trades':{
        'default'   :   OneTokenTradesClean,
    }
}

METHOD_btcta = {
    'spot':{
        'candle'    :   BtctaSpotBarClean,
        'ticker'    :   BtctaSpotTickClean,
        'trade'     :   BtctaSpotTradeClean,
        'depth'     :   BtctaSpotDepthClean,
    },
    'futures':{
        'candle'    :   BtctaFutureBarClean,
        'ticker'    :   BtctaFutureTickClean,
        'trade'     :   BtctaFutureTradeClean,
        'depth'     :   BtctaFutureDepthClean,
    }
}

def find_method_1token(data_type, exchange):
    try:
        return METHOD_1Token[data_type][exchange]
    except:
        return METHOD_1Token[data_type]['default'] 

def find_method_btcta(asset_type, data_type):
    return METHOD_btcta[asset_type][data_type]

def find_method_all(source=None, data_type=None, exchange=None, asset_type=None):
    print('source = ', source)
    print('data_type = ', data_type)
    print('exchange = ', exchange)
    print('asset_type = ', asset_type)
    if source == 'btcta':
        return find_method_btcta(asset_type, data_type)
    elif source == '1token':
        return find_method_1token(data_type, exchange)
    else:
        print('plz choose source between btcta and 1token')
