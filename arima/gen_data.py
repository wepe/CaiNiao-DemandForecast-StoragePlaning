#coding=utf-8
import pandas as pd
from datetime import date


item_all = pd.read_csv('../data/item_feature1.csv')
item_all['store_code'] = ['all' for _ in range(len(item_all))]
item_store = pd.read_csv('../data/item_store_feature1.csv')

items = pd.concat([item_all,item_store])
items = items[(items.date!=20151111)&(items.date!=20151212)]



def transform_date(x):
    end = date(2015,12,28)
    if x>20151212:
        return (end-date(x/10000,x%10000/100,x%100)).days
    elif 20151111<x<20151212:
        return (end-date(x/10000,x%10000/100,x%100)).days - 1
    else:
        return (end-date(x/10000,x%10000/100,x%100)).days - 2

items.date = items.date.apply(transform_date)
items.date = items.date.apply(lambda x:(1+(x-1)/14))

items = items[['item_id','store_code','date','qty_alipay_njhs']].groupby(['item_id','store_code','date']).agg('sum')
items.reset_index(inplace=True)  
items.rename(columns={'date':'week_reverse'},inplace=True)



d = items
d = d[d.week_reverse<=30]

#每两周的销量当成一个时间节点
d['item_id_store_code'] = d.item_id.map(str) +'_'+ d.store_code.map(str)
d = d.pivot(index='item_id_store_code', columns='week_reverse', values='qty_alipay_njhs')
d.fillna(0,inplace=True)
d.rename(columns={i:'week_'+str(i) for i in range(1,31)},inplace=True)
d['item_id'] = d.index
d['store_code'] = d.item_id
d.item_id = d.item_id.apply(lambda x:x.split('_')[0])
d.store_code = d.store_code.apply(lambda x:x.split('_')[1])
d.item_id = d.item_id.apply(lambda x:str(x))

"""
window1_pred_y = pd.read_csv('../val/window1_pred_y.csv')
top20 = window1_pred_y.iloc[:,:][['item_id','store_code']]
top20.item_id = top20.item_id.apply(lambda x:str(x))

d = pd.merge(top20,d,on=['item_id','store_code'],how='left')
"""
d.to_csv('data.csv',index=None,header=None)


