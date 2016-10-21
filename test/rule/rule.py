#coding=utf-8

import pandas as pd
from datetime import date


item_all = pd.read_csv('../../data/item_feature1.csv')
item_all['store_code'] = ['all' for _ in range(len(item_all))]
item_store = pd.read_csv('../../data/item_store_feature1.csv')

items = pd.concat([item_all,item_store])
items = items[(items.date!=20151111)&(items.date!=20151212)]

items_to_pred = items[['item_id','store_code','qty_alipay_njhs']].groupby(['item_id','store_code']).agg('sum')
items_to_pred.reset_index(inplace=True)
items_to_pred.drop('qty_alipay_njhs',axis=1,inplace=True)
items_to_pred.store_code = items_to_pred.store_code.apply(lambda x:str(x))

def transform_date(x):
    end = date(2015,12,28)
    if x>20151212:
        return (end-date(x/10000,x%10000/100,x%100)).days
    elif 20151111<x<20151212:
        return (end-date(x/10000,x%10000/100,x%100)).days - 1
    else:
        return (end-date(x/10000,x%10000/100,x%100)).days - 2

items.date = items.date.apply(transform_date)
items.date = items.date.apply(lambda x:(1+(x-1)/7))

items = items[['item_id','store_code','date','qty_alipay_njhs']].groupby(['item_id','store_code','date']).agg('sum')
items.reset_index(inplace=True)  
items.rename(columns={'date':'week_reverse'},inplace=True)


#规则预测
#计算前2周的最小周min，最大周max，预测值为 2*(min+(max-min)*(I(a>b)))
items.store_code = items.store_code.apply(lambda x:str(x))
a_b = pd.read_csv('../../data/config1.csv')
items = pd.merge(items,a_b,on=['item_id','store_code'])

items = items[items.week_reverse<=2]

print items


items.sort(columns=['item_id','store_code','qty_alipay_njhs'],inplace=True)
t0 = items[['item_id','store_code','a','b','qty_alipay_njhs']].groupby(['item_id','store_code','a','b']).agg('nth',0)
t1 = items[['item_id','store_code','a','b','qty_alipay_njhs']].groupby(['item_id','store_code','a','b']).agg('nth',0)
t2 = items[['item_id','store_code','a','b','qty_alipay_njhs']].groupby(['item_id','store_code','a','b']).agg('nth',-1)
t3 = items[['item_id','store_code','a','b','qty_alipay_njhs']].groupby(['item_id','store_code','a','b']).agg('nth',-1)
t0.rename(columns={'qty_alipay_njhs':'min1'},inplace=True)
t1.rename(columns={'qty_alipay_njhs':'min2'},inplace=True)
t2.rename(columns={'qty_alipay_njhs':'max1'},inplace=True)
t3.rename(columns={'qty_alipay_njhs':'max2'},inplace=True)
t0.reset_index(inplace=True)
t1.reset_index(inplace=True)
t2.reset_index(inplace=True)
t3.reset_index(inplace=True)

items = pd.merge(t0,t1,on=['item_id','store_code','a','b'])
items = pd.merge(items,t2,on=['item_id','store_code','a','b'])
items = pd.merge(items,t3,on=['item_id','store_code','a','b'])

items['min_'] = items.min1+items.min2
items['max_'] = items.max1+items.max2



items['pred'] = items.min_ + (items.max_ - items.min_)*(items.a**50/(items.a**50+items.b**50))
items_pred = items[['item_id','store_code','pred']]
items_pred.to_csv('rule.csv',index=None,header=None)

