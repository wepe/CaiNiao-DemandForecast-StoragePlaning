#coding=utf-8

import pandas as pd
from datetime import date


data = pd.read_csv('../../../data/train_test.csv')
data = data[data.watch==1][['item_id','store_code','date_counts']]
d = {1:'1',2:'2',3:'3',4:'4',5:'5',6:'all'}
data.store_code = data.store_code.apply(lambda x:d[x])
data.fillna(0,inplace=True)


item_all = pd.read_csv('../../data/item_feature1.csv')
item_all['store_code'] = ['all' for _ in range(len(item_all))]
item_store = pd.read_csv('../../data/item_store_feature1.csv')

#剔除双十一双十二
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






#第一二周为真实label,共5763个item store组合
items_truth = items[items.week_reverse<=2]
items_truth = items_truth[['item_id','store_code','qty_alipay_njhs']].groupby(['item_id','store_code']).agg('sum')
items_truth.reset_index(inplace=True)
items_truth.store_code = items_truth.store_code.apply(lambda x:str(x))
items_truth = pd.merge(items_to_pred,items_truth,on=['item_id','store_code'],how='left')
items_truth.fillna(0,inplace=True)
a_b = pd.read_csv('../../data/config1.csv')
items_truth = pd.merge(items_truth,a_b,on=['item_id','store_code'])

items_truth[['item_id','store_code','qty_alipay_njhs']].to_csv('val_y.csv',index=None)




#规则预测
#计算前2周的最小组合min，最大组合max，如果a>b则预测为max*2，反之min*2
items.store_code = items.store_code.apply(lambda x:str(x))
a_b = pd.read_csv('../../data/config1.csv')
items = pd.merge(items,a_b,on=['item_id','store_code'])

items = items[(3<=items.week_reverse)&(items.week_reverse<=5)]


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
items_pred.pred = items_pred.pred.apply(lambda x:0.0 if x<0.01 else x)


items_truth_pred = pd.merge(items_truth,items_pred,on=['item_id','store_code'],how='left')
items_truth_pred.fillna(0.0,inplace=True)


#计算代价
def cal_cost(y,pred,a,b):
    cost = 0
    nb_sample = len(y)
    for i in range(nb_sample):
        if pred[i]>y[i]:
            cost += b[i]*(pred[i]-y[i])
        else:
            cost += a[i]*(y[i]-pred[i])
    return nb_sample,cost

cost = cal_cost(items_truth_pred.qty_alipay_njhs,items_truth_pred.pred,items_truth_pred.a,items_truth_pred.b)

items_truth_pred[['item_id','store_code','pred']].to_csv('rule_{0}.csv'.format(cost[1]),index=None,header=None)


"""
items_truth_pred['error'] = (items_truth_pred.pred - items_truth_pred.qty_alipay_njhs)/items_truth_pred.qty_alipay_njhs
items_truth_pred['cost'] = 0
for row in range(items_truth_pred.shape[0]):
    a = items_truth_pred.iloc[row,3]
    b = items_truth_pred.iloc[row,4]
    y = items_truth_pred.iloc[row,2] 
    pred = items_truth_pred.iloc[row,5]
    if pred>=y:
        items_truth_pred.iloc[row,7] = b*(pred-y)
    else:
        items_truth_pred.iloc[row,7] = a*(y-pred)

items_truth_pred = items_truth_pred[['item_id','store_code','a','b','qty_alipay_njhs','pred','error','cost']]
for row in range(items_truth_pred.shape[0]):
    if items_truth_pred.iloc[row,4] == 0.0:
        items_truth_pred.iloc[row,6] = -99999

items_truth_pred.sort_values(by='cost',axis=0,ascending=False,inplace=True)
items_truth_pred.to_csv('rule_window1_pred_y.csv',index=None)
"""

