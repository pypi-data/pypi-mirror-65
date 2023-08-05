import os
import sys
import argparse
import json
from raw.download_1token import Download1Token
from raw.download_base import Utility
from raw.download_btcta import download_btcta
from raw.download_rqdata import DownloadRqdata
from clean.clean_crypto import CryptoClean
from clean.clean_base import CleanBase
from clean.clean_config import find_method_1token, find_method_btcta
from notify_master import MSG

def get_attr(dic, key):
    if key in list(dic.keys()):
        return dic[key]
    else:
        return None

if __name__ == "__main__":

    code_name = os.path.basename(sys.argv[0])
    parser = argparse.ArgumentParser()
    parser.add_argument("--jobinfo",  help = "input job info", type = json.loads)
    args = parser.parse_args()
    assert args.jobinfo is not None, parser.print_help()
    
    dic         = args.jobinfo
    task        = get_attr(dic, 'task')
    market      = get_attr(dic, 'market')
    asset       = get_attr(dic, 'asset')
    datatype    = get_attr(dic, 'datatype')
    beginday    = get_attr(dic, 'beginday')
    endday      = get_attr(dic, 'endday')
    timelist    = get_attr(dic, 'timelist')
    tickerList  = get_attr(dic, 'tickerList')
    subtask     = get_attr(dic, 'subtask')
    quicktest   = get_attr(dic, 'quicktest')
    surfboard   = get_attr(dic, 'surfboard')
    minutes     = get_attr(dic, 'minutes')
    key         = get_attr(dic, 'key')
    job_id      = get_attr(dic, 'job_id')
    
    msg = MSG(job_id = job_id, source = code_name)
    msg.send(content = f"batch start, data process receive job info : '{str(dic)}'.", is_error=False, chat_con=True)

    if task == '1token_raw_clean':
        content =  "\n#################################################\
                    \n####1token data process,  pattern selected: {}\
                    \n####begin = {}          end = {}\
                    \n####ticker list = {}    data type = {}\
                    \n#################################################\
                    ".format(subtask, beginday, endday, tickerList, datatype)
        msg.send(content=content, is_error=False, chat_con=True)
        if subtask in ['download_only', 'download_clean']:
            try:
                get_1token = Download1Token(beginday, endday, tickerList, msg)
                get_1token.process_data(datatype)
            except Exception as e:
                msg.send(content=e, is_error=True, chat_con=True)
                raise SystemExit

        if subtask in  ['clean_only', 'download_clean']:
            source = '1token'
            try:
                for ticker in tickerList:
                    exchange = ticker.split('/')[0] 
                    data_class = find_method_1token(datatype, exchange)
                    download_inputs = [(beginday, endday, ticker)]
                    CleanBase(msg = msg).clean_group(source, download_inputs, datatype, data_class, Utility)
            except Exception as e:
                msg.send(content=e, is_error=True, chat_con=True)
                raise SystemExit
        content =  "\n#################################################\
                    \n####1token data process finish\
                    \n#################################################"
        msg.send(content=content, is_error=False, chat_con=True)
    
    elif task == 'crypto_clean':
        try: 
            if quicktest:
                content =  '\n#################################################\
                            \n####crypto_clean_test start\
                            \n#################################################'
                msg.send(content=content, is_error=False, chat_con=True)
                CryptoClean(msg         =   msg, 
                            surfboard   =   surfboard,
                        ).clean_process_quick_test(CleanBase, Utility)
                
                content =  '\n#################################################\
                            \n####crypto_clean quicktest finish\
                            \n#################################################'
                msg.send(content=content, is_error=False, chat_con=True)

            
            else:
                content =  '\n#################################################\
                            \n####crypto_clean {} start   \
                            \n#################################################'.format(datatype)
                msg.send(content=content, is_error=False, chat_con=True)
                CryptoClean(msg         =   msg, 
                            data_type   =   datatype,
                            surfboard   =   surfboard,
                        ).clean_process(CleanBase, Utility)
                
                content =  '\n#################################################\
                            \n####crypto_clean {} finish\
                            \n#################################################'.format(datatype)
                msg.send(content=content, is_error=False, chat_con=True)
        except Exception as e:
            msg.send(content=e, is_error=True, chat_con=True)
            print(e)
            raise SystemExit
    
    elif task == 'btcta_raw_clean':
        source = 'btcta'
        try: 
            content =  '\n#################################################\
                        \n####btcta data process  \
                        \n####market: {}  asset type :{} \
                        \n####coin: {}    data type: {} \
                        \n####begin: {}   end: {} \
                        \n#################################################\
                        '.format(market, asset, tickerList, datatype, beginday, endday)
            msg.send(content=content, is_error=False, chat_con=True)
            
            for ticker in tickerList:
                if subtask in ['download_only', 'download_clean']:
                    d = download_btcta( exchange    = market,
                                        coin        = ticker,
                                        begin_date  = beginday,
                                        end_date    = endday,
                                        asset_type  = asset,
                                        data_type   = datatype,
                                        msg         = msg,
                                        )
                    d.test_network()
                    d.download()
                if subtask in ['clean_only', 'download_clean']:
                    download_inputs = [(beginday, endday, ticker, market)]
                    data_class = find_method_btcta(asset, datatype)
                    CleanBase(msg = msg).clean_group(source, download_inputs, datatype, data_class, Utility)

        except Exception as e:
            msg.send(content=e, is_error=True, chat_con=True)
            print(e)
            raise SystemExit
        
        content =  '\n#################################################\
                    \n####btcta_ {} finish\
                    \n#################################################'.format(datatype)
        msg.send(content=content, is_error=False, chat_con=True)
    
    elif task == 'crypto_clean_check':
        c = CryptoClean(    msg         =   msg, 
                            surfboard   =   surfboard
                        )
        res = c.clean_check_element(key, datatype, int(minutes))

        msg.send(content=str(res), is_error=False, chat_con=True)
    
    elif task == 'rqdata_download':
        content =  '\n#################################################\
                    \n####rqdata_download start \
                    \n####data type {}  \
                    \n####time list {}  \
                    \n#################################################\
                    '.format(datatype, timelist)
        msg.send(content=content, is_error=False, chat_con=True)

        if datatype == 'ticks':
            DownloadRqdata(months=timelist, msg = msg).download_months()
    
        content =  '\n#################################################\
                    \n####rqdata_download  finish\
                    \n####data type {}  \
                    \n####time list {}  \
                    \n#################################################\
                    '.format(datatype, timelist)
        msg.send(content=content, is_error=False, chat_con=True)
    
    elif task == 'check_file':
        content =  '\n#################################################\
                    \n####check file free space  start \
                    \n#################################################'
        msg.send(content=content, is_error=False, chat_con=True)
        
        folder = 'data'
        st = os.statvfs(folder)
        free_space_gb =  round(st.f_bavail * st.f_frsize/1024/1024/1024, 2)
        content = f'check file finish  path :{folder} with free space {free_space_gb} GB'
        msg.send(content=content, is_error=False, chat_con=True)
