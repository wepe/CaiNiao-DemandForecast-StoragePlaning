#coding=utf-8
"""
以天为单位，将每个item的销量可视化，有助于后续分析


"""


import pandas as pd
from datetime import date
import matplotlib.pyplot as plt
import os

#假期或者淘宝促销日用红色明显标注
holidays = [20141111,20141212,20150101,20150218,20150305,20150405,20150501,20150616,20150617,20150618,20150620,20150903,20150909,20150925,20150927,20151001,20151111,20151212]
holidays = [(date(x/10000,x%10000/100,x%100)-date(2014,10,10)).days for x in holidays]


#全国
data = pd.read_csv('../data/item_feature1.csv')[['item_id','cate_level_id']]
data.drop_duplicates(inplace=True)
data.set_index('item_id',inplace=True)
item_cate = data.to_dict()['cate_level_id']

data = pd.read_csv('../data/item_feature1.csv')[['date','item_id','qty_alipay_njhs']]
data.date = data.date.apply(lambda x:(date(x/10000,x%10000/100,x%100)-date(2014,10,10)).days)

items = list(data.item_id.unique())
os.mkdir('qty_alipay_njhs_all_')
for item in items:
    tmp = data[data.item_id==item]
    tmp = tmp.sort(columns='date')
    tmp.plot.scatter(x='date',y='qty_alipay_njhs',title=str(item))
    for holiday in holidays:
        qty = list(tmp[tmp.date==holiday]['qty_alipay_njhs'].values)
        qty.append(0)
        plt.scatter(holiday,qty[0],color='r')
    plt.xlabel('Date(20141010~20151227)')
    plt.ylabel('qty_alipay_njhs')
    plt.savefig('qty_alipay_njhs_all_/'+str(item_cate[item])+'_'+str(item)+'.jpg')

"""
#分仓1
data = pd.read_csv('../data/item_store_feature1.csv')[['date','item_id','store_code','qty_alipay_njhs']]
data = data[data.store_code==1]
data.date = data.date.apply(lambda x:(date(x/10000,x%10000/100,x%100)-date(2014,10,10)).days)

items = list(data.item_id.unique())
os.mkdir('qty_alipay_njhs_1')
for item in items:
    tmp = data[data.item_id==item]
    tmp = tmp.sort(columns='date')
    tmp.plot.scatter(x='date',y='qty_alipay_njhs',title=str(item))
    for holiday in holidays:
        qty = list(tmp[tmp.date==holiday]['qty_alipay_njhs'].values)
        qty.append(0)
        plt.scatter(holiday,qty[0],color='r')
    plt.xlabel('Date(20141010~20151227)')
    plt.ylabel('qty_alipay_njhs')
    plt.savefig('qty_alipay_njhs_1/'+str(item)+'.jpg')


#分仓2
data = pd.read_csv('../data/item_store_feature1.csv')[['date','item_id','store_code','qty_alipay_njhs']]
data = data[data.store_code==2]
data.date = data.date.apply(lambda x:(date(x/10000,x%10000/100,x%100)-date(2014,10,10)).days)

items = list(data.item_id.unique())
os.mkdir('qty_alipay_njhs_2')
for item in items:
    tmp = data[data.item_id==item]
    tmp = tmp.sort_values(by='date')
    tmp.plot.scatter(x='date',y='qty_alipay_njhs',title=str(item))
    for holiday in holidays:
        qty = list(tmp[tmp.date==holiday]['qty_alipay_njhs'].values)
        qty.append(0)
        plt.scatter(holiday,qty[0],color='r')
    plt.xlabel('Date(20141010~20151227)')
    plt.ylabel('qty_alipay_njhs')
    plt.savefig('qty_alipay_njhs_2/'+str(item)+'.jpg')


#分仓3
data = pd.read_csv('../data/item_store_feature1.csv')[['date','item_id','store_code','qty_alipay_njhs']]
data = data[data.store_code==3]
data.date = data.date.apply(lambda x:(date(x/10000,x%10000/100,x%100)-date(2014,10,10)).days)

items = list(data.item_id.unique())
os.mkdir('qty_alipay_njhs_3')
for item in items:
    tmp = data[data.item_id==item]
    tmp = tmp.sort_values(by='date')
    tmp.plot.scatter(x='date',y='qty_alipay_njhs',title=str(item))
    for holiday in holidays:
        qty = list(tmp[tmp.date==holiday]['qty_alipay_njhs'].values)
        qty.append(0)
        plt.scatter(holiday,qty[0],color='r')
    plt.xlabel('Date(20141010~20151227)')
    plt.ylabel('qty_alipay_njhs')
    plt.savefig('qty_alipay_njhs_3/'+str(item)+'.jpg')


#分仓4
data = pd.read_csv('../data/item_store_feature1.csv')[['date','item_id','store_code','qty_alipay_njhs']]
data = data[data.store_code==4]
data.date = data.date.apply(lambda x:(date(x/10000,x%10000/100,x%100)-date(2014,10,10)).days)

items = list(data.item_id.unique())
os.mkdir('qty_alipay_njhs_4')
for item in items:
    tmp = data[data.item_id==item]
    tmp = tmp.sort_values(by='date')
    tmp.plot.scatter(x='date',y='qty_alipay_njhs',title=str(item))
    for holiday in holidays:
        qty = list(tmp[tmp.date==holiday]['qty_alipay_njhs'].values)
        qty.append(0)
        plt.scatter(holiday,qty[0],color='r')
    plt.xlabel('Date(20141010~20151227)')
    plt.ylabel('qty_alipay_njhs')
    plt.savefig('qty_alipay_njhs_4/'+str(item)+'.jpg')


#分仓5
data = pd.read_csv('../data/item_store_feature1.csv')[['date','item_id','store_code','qty_alipay_njhs']]
data = data[data.store_code==5]
data.date = data.date.apply(lambda x:(date(x/10000,x%10000/100,x%100)-date(2014,10,10)).days)

items = list(data.item_id.unique())
os.mkdir('qty_alipay_njhs_5')
for item in items:
    tmp = data[data.item_id==item]
    tmp = tmp.sort_values(by='date')
    tmp.plot.scatter(x='date',y='qty_alipay_njhs',title=str(item))
    for holiday in holidays:
        qty = list(tmp[tmp.date==holiday]['qty_alipay_njhs'].values)
        qty.append(0)
        plt.scatter(holiday,qty[0],color='r')
    plt.xlabel('Date(20141010~20151227)')
    plt.ylabel('qty_alipay_njhs')
    plt.savefig('qty_alipay_njhs_5/'+str(item)+'.jpg')
"""
