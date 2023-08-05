
import pandas as pd
import datetime

def work_year(begin, end):
    d1 = datetime.datetime.strptime(begin,'%Y%m%d')
    d2 = datetime.datetime.strptime(end,'%Y%m%d')
    return round((d2 - d1).days / 365, 4)


fund_list = pd.read_excel('/Users/huangkejia/surfing/python/data_process/raw/fund_data/wind_fund_list.xlsx')
fund_list.columns = ['wind_id','symbol','fund_full_name','found_date','end_date','benchmark','wind_class_I','wind_class_II','money','structured_fund_base_fund_code','if_structured_fund','if_regular_open_fund','fund_manager','company_name']
fund_list['update_time'] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
fund_list['rq_id'] = [_.split('!')[0].split('.')[0] for _ in fund_list['wind_id'] ]

fund_mng_list = fund_list['fund_manager'].tolist()
company_list = fund_list['company_name'].tolist()


key_base = []
for i,company_i in zip(fund_mng_list,company_list):
    try:
        manager_info = i.split('\r\n')
    except:
        break    
    for j in manager_info:
        name = j.split('(')[0]
        if '至今' in j:
            begin = j.split('(')[1].split(')')[0].split('至今')[0]
            end = datetime.datetime.now().strftime("%Y%m%d")
            experience = work_year(begin, end)
            key_base.append((name+'_'+company_i ,experience))
            
        else:
            begin = j.split('(')[1].split(')')[0].split('-')[0]
            end = j.split('(')[1].split(')')[0].split('-')[1]
            experience = work_year(begin, end)
            key_base.append((name+'_'+company_i ,experience))
res = []
for i in key_base:
    j = [_ for _ in key_base if _[0] == i[0]]
    work_years  = round(sum([_[1] for _ in j ]),4)
    k1 = i[0]+'_'+str(work_years)
    res.append(k1)
key_base = res
key_base = list(set(key_base))

res = []
for i,company_i in zip(fund_mng_list,company_list):
    try:
        manager_info = i.split('\r\n')
    except:
        res.append('')
    res_i = []
    for j in manager_info:
        name = j.split('(')[0]
        key_i = [_ for _ in key_base if _.split('_')[0] == name and  _.split('_')[1] == company_i]
        
        res_i.append(j+f'[{key_i[0]}]')
    res.append(res_i)

fund_list['fund_manager'] = res