import numpy as np
import pandas as pd
import datetime
from datetime import date
from pyfinance.ols import PandasRollingOLS
from fund.db.database import BasicDatabaseConnector,DerivedDatabaseConnector
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score
from fund.data_api.basic import get_index_info, get_trading_day_list, get_index_price, get_fund_ret,get_fund_info,get_fund_nav
from fund.data_api.derived import get_fund_nav_adjusted_nv, get_index_benchmark_data,get_fund_list,get_fund_fee,get_fund_asset

class fund_indicators:
    
    # 优化日志
    # 计算前统一取数据
    # log return  <- normal return
    # 滚动定期回归算beta 定期 time_span， 不足time_span, beta nan
    # beta 计算 考虑无风险利率 基金每日ret -无风险利率/242（即每日无风险利率）
    # 日更 <- 一个季度算一次
    # 重现按照延报实现计算逻辑
    
    no_risk_ret = 0.03
    year = 242
    index_id = 'hs300'
    start_date  = date(2012,1,1)
    end_date = date(2020,3,30)
    
    long_time_span = 242 * 3 
    short_time_span = 242
    
    asset_dic = {
        '利率债' : 'national_debt',
        '美股大盘':'sp500rmb',
        '德国大盘':'dax30rmb',
        '信用债':'credit_debt',
        '房地产':'real_state',
        'A股大盘':'hs300',
        '原油': 'oil',
        '黄金': 'gold',
        '创业板':'gem',
        '日本大盘': 'n225rmb',
        'A股中盘':'csi500',
    }

    
    def __init__(self):
        
        self.data_prepare()
        self.build_history()
        self.upload_derived(self.result.dropna(), 'fund_indicator')
        
    def upload_derived(self, df, table_name):
        df.to_sql(table_name, DerivedDatabaseConnector().get_engine(), index=False, if_exists='append')
         
    def data_prepare(self):
        #self.fund_list = sorted(get_fund_list()['fund_id'].tolist())[:200]
        # asset exit
        fund_info = get_fund_info()[['fund_id','asset_type']]
        #TODO now only calculate funds which have tag 
        self.fund_list  = fund_info[fund_info['asset_type'] != 'null'].fund_id.tolist()
        #self.fund_list  = sorted(fund_info[fund_info['asset_type'] == 'null'].fund_id.tolist())[6000:]
        
        self.fund_nav = get_fund_nav_adjusted_nv(self.fund_list, self.start_date, self.end_date).drop_duplicates()
        self.fund_nav = self.fund_nav.pivot_table(index='datetime', columns='fund_id',values='adjusted_net_value')
        self.benchmark = get_index_benchmark_data([self.index_id], self.start_date, self.end_date)
        self.fund_fee = get_fund_fee() #基金费率
        self.fund_asset = get_fund_asset() # 基金资产类别
        asset_list = list(self.asset_dic.values())
        
        self.asset_data = get_index_benchmark_data(asset_list, self.start_date, self.end_date)
        self.asset_data = self.asset_data.pivot_table(index='datetime', columns='index_id',values='close')
        self.asset_data = np.log(self.asset_data) - np.log(self.asset_data.shift(1)) #各资产日收益 
        
        
        self.rm = self.benchmark[['close','datetime']].set_index('datetime')
        self.rm = np.log(self.rm) - np.log(self.rm.shift(1)) # 基准日收益log ret
        
        self.rb = self.no_risk_ret # 无风险利率 b -> bank
        self.rb_d = self.no_risk_ret / self.year # 无风险日利率
        self.rm_no_rb = self.rm - self.rb_d 
        self.rm_no_rb.columns = ['benchmark-risk_free'] # 基准日收益  - 无风险日利率
         
        self.rf = (np.log(self.fund_nav) - np.log(self.fund_nav.shift(1))) # 基金日收益log ret
        self.rf_no_rb = self.rf - self.rb_d # 基金日收益 - 日无风险利率 
        self.fund_info = get_fund_info()[['fund_id','asset_type','start_date','end_date']]
        
    def ployfit(self, x, df):
        # 返回多元回归系数 当前2
        df_i = df.reset_index().loc[x[0] : x[-1],]
        if set(df.head()['close'].isnull()) == {True}:
            return np.nan
        try:
            return np.polyfit(df_i['benchmark-risk_free'],df_i['close'],2)[0]
        except:
            return np.nan
    
    def rolling_beta(self, x, df, i ):
        # y在前 x在后
        # y =[2,4] ;x = [1,2]
        #np.polyfit(y,x,1)[0]  = 2
        df_i = df.reset_index().loc[x[0] : x[-1],].dropna()
        return np.polyfit(df_i[i],df_i['benchmark-risk_free'],1)[0]
        
    def get_beta(self, t_range, fund_list):
        # beta 贝塔 
        # 表示基金的收益相对与基准对变化， 绝对值越大， 相对于基准波动越大， 体现为风险越大
        # rf_no_rb = 基金日收益 - 无风险日收益  
        # rm_no_rb = 基准日收益 - 无风险日收益
        # v1 对 v2 做回归 beta是一次项系数   rf_no_rb = beta * rm_no_rb + C （滚动计算）
        # 回归的时间长度取 time_span
        res = []
        date_list = self.rf_no_rb.index
        for i in fund_list:
            try:
                df = self.rf_no_rb[[i]].join(self.rm_no_rb).dropna()
                x = df['benchmark-risk_free']
                y = df[i]
                model = PandasRollingOLS(y=y, x=x, window=t_range)
                res_i = model.beta
                res_i.columns = [i]
                res.append(res_i)
            except:
                continue
        return pd.concat(res, axis =1, sort=True)
        
    def get_treynor(self):
        # treynor 特雷诺
        # 表示评价时间范围内 基金单位风险对无风险收益
        # rf = 基金一段时间平均收益 - 无风险收益 （根据参考时间做年化 这里日收益* time_span） （滚动计算）
        # beta 参考上面
        # treynor = rf / beta
        
        tr_up = self.rf_avg
        tr_up = tr_up.loc[self.beta.index,].copy() * self.time_span -  self.rb_d * self.time_span
        self.treynor = tr_up / self.beta
        self.treynor = self.treynor.loc[self.beta.index[0]:,]
        
    def get_alpha(self, fund_list, beta):
        # alpha 阿尔法
        # 表示超越市场对收益
        # rf_avg = 基金评价期间平均日收益  （滚动计算）
        # rb_d = 无风险日利率 
        # rm_avg = 基准评价期间平均日收益  （滚动计算）
        # alpha = (rf_avg - rb_d - beta*(rm_avg - rb_d) ) * year
        c = [_ for _ in self.rf_avg.columns if _ in fund_list]
        v1 = (self.rm_avg - self.rb_d).loc[beta.index,].copy()
        v2 = beta.multiply(v1.values, axis='close').copy()
        alpha = ((self.rf_avg[c] - self.rb_d - v2) * self.year).copy()
        alpha = alpha.loc[beta.index[0]:,].copy()
        return alpha
    
    def get_mdd(self):
        # mdd 最大回撤
        # pandas :  1 - (df / df.cummax()).min()
        mdd_fuc = lambda x: 1 - (x /np.maximum.accumulate(x)).min(axis=0)
        self.mdd = self.fund_nav.rolling(self.time_span).apply(mdd_fuc, raw=True)
        self.mdd = self.mdd.loc[self.beta.index[0]:,]
    
    def get_downside_risk(self):
        # downside risk 下行风险
        # sqrt(year) / T * sum( min(0, rf - rb_d))
        df = self.rf - self.rb_d
        df = (np.sign(df)*-1+1 )/2 * df * -1
        self.down_risk = df.rolling(self.time_span).sum() * np.sqrt(self.time_span / self.year) / self.year
        self.down_risk = self.down_risk.loc[self.beta.index[0]:,]
        
    def get_return_over_period(self):
        self.ret_over_period = np.log(self.fund_nav) - np.log(self.fund_nav.shift(self.time_span))
        self.ret_over_period = self.ret_over_period.loc[self.beta.index[0]:,]
    
    def get_annulized_average_daily_return(self):
        self.annual_avg_daily_ret = (self.rf.rolling(self.time_span).sum()*self.year/self.time_span).loc[self.beta.index,]
        self.annual_avg_daily_ret = self.annual_avg_daily_ret.loc[self.beta.index[0]:,]
    
    def get_volatility(self):
        self.vol = self.rf.rolling(self.time_span).std().loc[self.beta.index,]
        self.vol = self.vol.loc[self.beta.index[0]:,]
    
    def get_m_square(self):
        # m_square  m2测度
        # 风险调整指标，与sharpe完全线性关系，在排序上与sharpe等价
        # 含义更直观，同风险下相对与市场组合的超额收益率
        # rf_avg = 基金在评价期的平均收益率
        # vol = 波动率 收益率标准差
        # rm_avg = 评价期上市场指数平均收益率
        # vol_m = 市场指数波动率
        # rb_d = 无风险日利率
        # m2 = (vol_m / vol * (rf_avg - rb_d) + rb_d) - rm_avg
        v1 = (self.rf_avg - self.rb_d).loc[self.beta.index,]
        v2 = self.vol_m.loc[self.beta.index,]
        v3 = v1.multiply(v2.values, axis='close')
        v4 = v3 / self.vol
        self.m_square = (v4 + self.rb_d).sub(self.rm_avg.loc[self.beta.index,].values, axis='close') 
        self.m_square = self.m_square.loc[self.beta.index[0]:,]
    
    def get_time_return(self):
        # time_return 择时收益
        # 择时收益是一种业绩归因指标，衡量基金在评价期上通过择时获得的超额收益
        # beta_i 基金在自区间beta
        # beta_0 基金在评价期上的beta
        # rm_i 基准在区间收益率
        # rb_i 无风险资产在自区间收益率
        # 区间 当前取 3M ->60
        # time_ret = sum[(beta_i - beta_0) * (rm_i - rb_i)]
        self.day_range = 60
        rb_i = self.no_risk_ret / self.year * self.day_range
        self.beta_i = self.get_beta(self.day_range)
        self.rm_i = self.rm.rolling(self.day_range).sum()
        self.rm_i = self.beta_i.join(self.rm_i).fillna(method = 'ffill')[['close']].copy()
        date_list = self.beta_i.index.tolist()
        i_num = int(self.time_span / self.day_range) - 1

        res = []
        for d in self.beta.index:
            idx = date_list.index(d)
            time_ret = 0
            for i in range(i_num):
                idx_i = idx  - (1+i) * self.day_range
                d_i = date_list[idx_i]
                v1 = self.beta_i.loc[d_i,] - self.beta.loc[d,]
                v2 = self.rm_i.loc[d_i,] - rb_i
                time_ret_i = v1 * v2.values
                time_ret += time_ret_i
            res.append(time_ret.copy())
        self.time_ret = pd.DataFrame(res)
        self.time_ret.index = self.beta.index
        
    def get_value_at_risk(self):
        # value at risk 资产在险值
        # 在评价期间内，基金95%的日跌幅不会大于该数值
        # var = -min{0, r(t) 大到小排序 95分位数}
        self.var = self.rf.rolling(self.time_span).quantile(0.05)
        self.var[self.var>0] = 0
        self.var = -1 * self.var
        self.var = self.var.loc[self.beta.index[0]:,]
    
    def get_r_square(self):
        # r2 决定系数r方
        # 衡量基金收益波动的方差中，市场决定比例， 简单理解市场风险占总风险权重
        res = []
        date_list = self.rf_no_rb.index
        for i in self.fund_list:
            df = self.rf_no_rb[[i]].join(self.rm_no_rb).fillna(method = 'ffill')[1:]
            x = df['benchmark-risk_free']
            y = df[i]
            model = PandasRollingOLS(y=y, x=x, window=self.time_span)
            res.append(model.rsq)
        df = pd.DataFrame(res).T
        df.columns = self.fund_list
        df.index   = self.rf_no_rb.index[-df.shape[0]:]    
        self.r_square = df.loc[self.beta.index[0]:,]
        
    def get_sharpe_ratio(self):
        # sharpe 夏普
        # 简单年化 ret * year , vol * sqrt( year )
        sr_ret = self.rf_no_rb.rolling(self.time_span).mean() * self.year
        sr_vol = self.rf.rolling(self.time_span).std() * np.sqrt(self.year)
        self.sharpe = (sr_ret/ sr_vol).loc[self.beta.index[0]:,]
    
    def get_treynor_mazuy_coefficient(self):
        # tm 系数描述基金在评价期上的择时收益
        # 以 rf_no_rb 为因变量对  rm_no_rb 及其平方进行回归的二次项系数
        # 以df的index 序数做 rolling apply, 输入多个列的， 可以此法实现pyfinance.PandasRollingOLS
        res = []
        date_list = self.rf_no_rb.index
        for i in self.fund_list:
            df = self.rf_no_rb[[i]].join(self.rm_no_rb).fillna(method = 'ffill')[1:]
            x = df['benchmark-risk_free']
            y = df[i]
            y.name = 'close'
            df = pd.DataFrame([x,y]).T
            df['idx'] = range(df.shape[0])
            res_i = df[['idx']].rolling(self.time_span).apply(lambda x : self.ployfit(x, df), raw= True)
            res_i.columns = [i]
            res.append(res_i)
        self.tm_coef = pd.concat(res, axis = 1).loc[self.beta.index[0]:,]
        
    def get_fee_rate(self):
        self.fee_rate = self.fund_fee[self.fund_fee['fund_id'].isin(self.fund_list)]
        self.fee_rate.loc[:,'fee_rate'] = ((self.fee_rate['manage_fee'] + self.fee_rate['trustee_fee'])/100).copy()
        self.fee_rate = self.fee_rate[['fund_id', 'fee_rate']]
        
    def get_track_error(self, t_range, fund_list, beta):
        df_asset = self.fund_asset[self.fund_asset['fund_id'].isin(fund_list)]
        con_cal = df_asset['asset_type'] != 'null'
        con_pas = df_asset['asset_type'] == 'null'
        fl_pas = df_asset[con_pas]['fund_id']
        res = []
        c = []
        for idx,f in df_asset[con_cal].iterrows(): 
            try:
                f_i = f.fund_id
                a_t = f.asset_type
                a_i = self.asset_dic[a_t]
                ret_b = self.asset_data[[a_i]]
                ret_f = self.rf[[f_i]]
                df_tmp = ret_f.join(ret_b).fillna(0)
                df_tmp = (df_tmp[f_i] - df_tmp[a_i]).rolling(t_range).std()*np.sqrt(242).copy()
                df_tmp.columns = [f_i]
                res.append(df_tmp.copy())
                c.append(f_i)
            except:
                continue
        
        track_err = pd.concat(res, axis = 1, sort=True)
        track_err.columns = c
        for i in fl_pas:
            track_err[i] =  np.nan
        track_err = track_err.loc[beta.index[0]:,]
        return track_err

    def build_history(self):
        # ['A股中盘','A股大盘','创业板'] 3年 历史数据 注重alpha 
        # 其他 用1年  成立较晚 注重track_err 
        fund_info = self.fund_info
        fund_info = fund_info[fund_info['asset_type'] != 'null']
        type_lterm = ['A股中盘','A股大盘','创业板']
        asset_list = list(self.asset_dic.keys()) 
        type_sterm = [_ for _ in asset_list if not _ in type_lterm]
        fl_lterm  = fund_info[fund_info['asset_type'].isin(type_lterm)].fund_id.tolist()
        fl_sterm  = fund_info[fund_info['asset_type'].isin(type_sterm)].fund_id.tolist()
        self.get_fee_rate()
        result_df = []
        for fl, time_span in zip([fl_lterm, fl_sterm],  [ self.long_time_span,  self.short_time_span]):
            self.rm_avg = self.rm.rolling(time_span).mean()# 基准评价期间平均日收益
            self.vol_m = self.rm.rolling(time_span).std() # 基准评价期间波动率
            self.rf_avg = self.rf.fillna(0).rolling(time_span).mean() # 基金评价期间平均日收益
            
            beta = self.get_beta(time_span, fl)
            alpha = self.get_alpha(fl, beta)
            track_err = self.get_track_error(time_span, fl, beta)
            date_last = track_err.index[-1]
            fact_l = ['beta','alpha','track_err']
            data_l = [beta, alpha, track_err]
            res = []
            for fun_i in fl:
                for f, d in zip(fact_l, data_l):
                    if fun_i not in d.columns:
                        continue
                    d = d.loc[:date_last][[fun_i]].stack().reset_index(level=[0,1]).copy()
                    d.columns = ['datetime','fund_id','value']
                    d['name'] = f
                    res.append(d.copy())
            result = pd.concat(res).pivot_table(index=['datetime','fund_id'], columns='name',values='value')
            result = result.join(self.fee_rate.set_index('fund_id'))   
            result = result.reset_index(level=[0,1])
            result['timespan'] = time_span / self.year
            result = result.replace(np.inf,np.nan)
            result = result.replace(-np.inf,np.nan)
            result_df.append(result)
        self.result = pd.concat(result_df).dropna()
        
f_i = fund_indicators()
