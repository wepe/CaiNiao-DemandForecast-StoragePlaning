#coding=utf-8

"""
对原始数据做预处理，添加字段名，划分补少、补多成本字段

"""

import pandas as pd

config = pd.read_csv('../data/config1.csv',header=None)
config.columns = ['item_id','store_code','a_b']
config['a'] = config['a_b'].apply(lambda x:float(x.split('_')[0]))
config['b'] = config['a_b'].apply(lambda x:float(x.split('_')[1]))
config.to_csv('../data/config1.csv',index=None)


item_feature = pd.read_csv('../data/item_feature1.csv',header=None)
item_feature.columns = ['date','item_id','cate_id','cate_level_id','brand_id','supplier_id','pv_ipv','pv_uv','cart_ipv','cart_uv','collect_uv','num_gmv',
'amt_gmv','qty_gmv','unum_gmv','amt_alipay','num_alipay','qty_alipay','unum_alipay','ztc_pv_ipv','tbk_pv_ipv','ss_pv_ipv','jhs_pv_ipv','ztc_pv_uv',
'tbk_pv_uv','ss_pv_uv','jhs_pv_uv','num_alipay_njhs','amt_alipay_njhs','qty_alipay_njhs','unum_alipay_njhs']
item_feature.to_csv('../data/item_feature1.csv',index=None)

item_store_feature = pd.read_csv('../data/item_store_feature1.csv',header=None)
item_store_feature.columns = ['date','item_id','store_code','cate_id','cate_level_id','brand_id','supplier_id','pv_ipv','pv_uv','cart_ipv','cart_uv','collect_uv','num_gmv',
'amt_gmv','qty_gmv','unum_gmv','amt_alipay','num_alipay','qty_alipay','unum_alipay','ztc_pv_ipv','tbk_pv_ipv','ss_pv_ipv','jhs_pv_ipv',
'ztc_pv_uv','tbk_pv_uv','ss_pv_uv','jhs_pv_uv','num_alipay_njhs','amt_alipay_njhs','qty_alipay_njhs','unum_alipay_njhs']
item_store_feature.to_csv('../data/item_store_feature1.csv',index=None)

