#coding=utf-8
import pandas as pd

#计算代价
def cal_cost(y,pred,a,b):
    y,pred,a,b = y.values,pred.values,a.values,b.values
    cost = 0
    nb_sample = len(y)
    for i in range(nb_sample):
        if pred[i]>y[i]:
            cost += b[i]*(pred[i]-y[i])
        else:
            cost += a[i]*(y[i]-pred[i])
    return nb_sample,cost

#验证集的真实值
val_y = pd.read_csv('rule/val_y.csv')
val_y.rename(columns={'qty_alipay_njhs':'y'},inplace=True)

#单模型
xgb = pd.read_csv('xgb/xgb_181.csv',header=None)
xgb.columns = ['item_id','store_code','xgb']

svr_rbf = pd.read_csv('svr_rbf/svr_rbf_187.csv',header=None)
svr_rbf.columns = ['item_id','store_code','svr_rbf']

svr_linear = pd.read_csv('svr_linear/svr_linear_166.csv',header=None)
svr_linear.columns = ['item_id','store_code','svr_linear']

rule = pd.read_csv('rule/rule_1285073.85901.csv',header=None)
rule.columns = ['item_id','store_code','rule']

rf = pd.read_csv('rf/rf_173.csv',header=None)
rf.columns = ['item_id','store_code','rf']

gbrt = pd.read_csv('gbrt/gbrt_166.csv',header=None)
gbrt.columns = ['item_id','store_code','gbrt']

ada = pd.read_csv('adaboost/adaboost_205.csv',header=None)#以下这4个模型在换数据后没使用
ada.columns = ['item_id','store_code','ada']

mlp = pd.read_csv('adaboost/adaboost_205.csv',header=None)
mlp.columns = ['item_id','store_code','mlp']

extree = pd.read_csv('adaboost/adaboost_205.csv',header=None)
extree.columns = ['item_id','store_code','extree']

bagging = pd.read_csv('adaboost/adaboost_205.csv',header=None)
bagging.columns = ['item_id','store_code','bagging']


#合并单模型
t = pd.merge(xgb,rf,on=['item_id','store_code'],how='outer')
t = pd.merge(t,svr_rbf,on=['item_id','store_code'],how='outer')
t = pd.merge(t,svr_linear,on=['item_id','store_code'],how='outer')
t = pd.merge(t,rule,on=['item_id','store_code'],how='outer')
t = pd.merge(t,gbrt,on=['item_id','store_code'],how='outer')
t = pd.merge(t,ada,on=['item_id','store_code'],how='outer')
t = pd.merge(t,mlp,on=['item_id','store_code'],how='outer')
t = pd.merge(t,extree,on=['item_id','store_code'],how='outer')
t = pd.merge(t,bagging,on=['item_id','store_code'],how='outer')

t.fillna(0.0,inplace=True)


#如果预测值为负的，置为0
t.xgb = t.xgb.apply(lambda x:max(x,0.0))
t.rf = t.rf.apply(lambda x:max(x,0.0))
t.rule = t.rule.apply(lambda x:max(x,0.0))
t.mlp = t.mlp.apply(lambda x:max(x,0.0))
t.svr_rbf = t.svr_rbf.apply(lambda x:max(x,0.0))
t.svr_linear = t.svr_linear.apply(lambda x:max(x,0.0))
t.bagging = t.bagging.apply(lambda x:max(x,0.0))
t.ada = t.ada.apply(lambda x:max(x,0.0))
t.gbrt = t.gbrt.apply(lambda x:max(x,0.0))
t.extree = t.extree.apply(lambda x:max(x,0.0))


a_b = pd.read_csv('../data/config1.csv')
t = pd.merge(t,a_b,on=['item_id','store_code'])

col_num = t.shape[1]



#算出单模型预测值的最大、次大、最小、次小值
t['min_pred'] = 0
t['min2_pred'] = 0
t['max_pred'] = 0
t['max2_pred'] = 0
t['min_pred_norule'] = 0
t['min2_pred_norule'] = 0
t['max_pred_norule'] = 0
t['max2_pred_norule'] = 0


for row in range(t.shape[0]):
    preds = [t.iloc[row,2],t.iloc[row,4],t.iloc[row,5],t.iloc[row,7]]
    preds_norule = [t.iloc[row,3],t.iloc[row,5],t.iloc[row,7]]
    preds.sort()
    preds_norule.sort()
    t.iloc[row,col_num] = preds[0]#min_pred
    t.iloc[row,col_num+1] = preds[1]#min2_pred
    t.iloc[row,col_num+2] = preds[-1]#max_pred
    t.iloc[row,col_num+3] = preds[-2]#max2_pred
    t.iloc[row,col_num+4] = preds_norule[0]#min_pred_norule
    t.iloc[row,col_num+5] = preds_norule[1]#min2_pred_norule
    t.iloc[row,col_num+6] = preds_norule[-1]#max_pred_norule
    t.iloc[row,col_num+7] = preds_norule[-2]#max2_pred_norule


t.to_csv('all_pred.csv',index=None)




#根据补多、补少成本进行模型融合
t = pd.read_csv('all_pred.csv')
col_num = t.shape[1]

t['pred'] = 0
for row in range(t.shape[0]):
    a = t.iloc[row,12]
    b = t.iloc[row,13]
    
    min_pred_norule = t.iloc[row,14]
    min2_pred_norule = t.iloc[row,15]
    max_pred_norule = t.iloc[row,16]
    max2_pred_norule = t.iloc[row,17]
    this_store_code = t.iloc[row,1]

    if a>b:
        t.iloc[row,col_num] = max_pred_norule*1.6
    else:
        t.iloc[row,col_num] = min_pred_norule*0.9


t.pred = t.pred.apply(lambda x:max(x,0.0))


#模型与规则加权融合
t.pred = 0.8*t.pred + 0.2*t.rule


val_y_pred = pd.merge(val_y,t,on=['item_id','store_code'],how='left')
val_y_pred.fillna(0.0,inplace=True)

val_y_pred_all = val_y_pred[val_y_pred.store_code=='all']
val_y_pred_1 = val_y_pred[val_y_pred.store_code=='1']
val_y_pred_2 = val_y_pred[val_y_pred.store_code=='2']
val_y_pred_3 = val_y_pred[val_y_pred.store_code=='3']
val_y_pred_4 = val_y_pred[val_y_pred.store_code=='4']
val_y_pred_5 = val_y_pred[val_y_pred.store_code=='5']
print "all cost:",cal_cost(val_y_pred_all.y,val_y_pred_all.pred,val_y_pred_all.a,val_y_pred_all.b)
print "1 cost:",cal_cost(val_y_pred_1.y,val_y_pred_1.pred,val_y_pred_1.a,val_y_pred_1.b)
print "2 cost:",cal_cost(val_y_pred_2.y,val_y_pred_2.pred,val_y_pred_2.a,val_y_pred_2.b)
print "3 cost:",cal_cost(val_y_pred_3.y,val_y_pred_3.pred,val_y_pred_3.a,val_y_pred_3.b)
print "4 cost:",cal_cost(val_y_pred_4.y,val_y_pred_4.pred,val_y_pred_4.a,val_y_pred_4.b)
print "5 cost:",cal_cost(val_y_pred_5.y,val_y_pred_5.pred,val_y_pred_5.a,val_y_pred_5.b)
print "total cost:",cal_cost(val_y_pred.y,val_y_pred.pred,val_y_pred.a,val_y_pred.b)




#验证集上的每个item产生的代价，从高到低排序，保存为csv文件，test set在预测时会将这部分item的预测值替换为前两周销量
val_y_pred['error'] = (val_y_pred.pred - val_y_pred.y)/val_y_pred.y
val_y_pred['cost'] = 0
for row in range(val_y_pred.shape[0]):
    a = val_y_pred.iloc[row,13]
    b = val_y_pred.iloc[row,14]
    y = val_y_pred.iloc[row,2] 
    pred = val_y_pred.iloc[row,23]
    if pred>=y:
        val_y_pred.iloc[row,25] = b*(pred-y)
    else:
        val_y_pred.iloc[row,25] = a*(y-pred)

val_y_pred = val_y_pred[['item_id','store_code','a','b','y','pred','error','cost']]
for row in range(val_y_pred.shape[0]):
    if val_y_pred.iloc[row,4] == 0.0:
        val_y_pred.iloc[row,6] = -99999

val_y_pred.sort_values(by='cost',axis=0,ascending=False,inplace=True)
val_y_pred.to_csv('16_09_window1_pred_y.csv',index=None)


