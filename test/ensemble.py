#coding=utf-8
import pandas as pd


#单模型预测结果 合并
xgb = pd.read_csv('xgb/xgb.csv',header=None)
xgb.columns = ['item_id','store_code','xgb']

svr_rbf = pd.read_csv('svr_rbf/svr_rbf.csv',header=None)
svr_rbf.columns = ['item_id','store_code','svr_rbf']

svr_linear = pd.read_csv('svr_linear/svr_linear.csv',header=None)
svr_linear.columns = ['item_id','store_code','svr_linear']

rule = pd.read_csv('rule/2weekrule.csv',header=None)
rule.columns = ['item_id','store_code','rule']

rf = pd.read_csv('rf/rf.csv',header=None)
rf.columns = ['item_id','store_code','rf']

gbrt = pd.read_csv('gbrt/gbrt.csv',header=None)
gbrt.columns = ['item_id','store_code','gbrt']


t = pd.merge(xgb,rf,on=['item_id','store_code'],how='outer')
t = pd.merge(t,svr_rbf,on=['item_id','store_code'],how='outer')
t = pd.merge(t,svr_linear,on=['item_id','store_code'],how='outer')
t = pd.merge(t,rule,on=['item_id','store_code'],how='outer')
t = pd.merge(t,gbrt,on=['item_id','store_code'],how='outer')
t.fillna(0.0,inplace=True)


#模型预测值可能为负数，用0替换
t.xgb = t.xgb.apply(lambda x:max(x,0.0))
t.rf = t.rf.apply(lambda x:max(x,0.0))
t.rule = t.rule.apply(lambda x:max(x,0.0))
t.svr_rbf = t.svr_rbf.apply(lambda x:max(x,0.0))
t.svr_linear = t.svr_linear.apply(lambda x:max(x,0.0))
t.gbrt = t.gbrt.apply(lambda x:max(x,0.0))



#每个item的补少、补多成本
a_b = pd.read_csv('../data/config1.csv')
t = pd.merge(t,a_b,on=['item_id','store_code'])

col_num = t.shape[1]


#取单模型预测值的最大、次大、最小、次小值
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



#根据补多、补少成本对模型结果融合
t = pd.read_csv('all_pred.csv')
col_num = t.shape[1]

t['pred'] = 0
for row in range(t.shape[0]):
    a = t.iloc[row,8]
    b = t.iloc[row,9]
    
    min_pred_norule = t.iloc[row,10]
    min2_pred_norule = t.iloc[row,11]
    max_pred_norule = t.iloc[row,12]
    max2_pred_norule = t.iloc[row,13]
    this_store_code = t.iloc[row,1]

    if a>b:
        t.iloc[row,col_num] = max_pred_norule*1.1
    else:
        t.iloc[row,col_num] = min_pred_norule*0.9


#模型与规则再加权融合
t.pred = 0.75*t.pred + 0.25*t.rule


def func(x):
    if x<0.01:
        return 0.0
    else:
        return x

t.pred = t.pred.apply(func)
t = t[['item_id','store_code','pred']]
t.pred = t.pred.apply(lambda x:round(x))

t.to_csv('ensemble_1109_7525.csv',index=None,header=None)


#对验证集上代价比较大的各个分仓的top k 个item，用前两周的销量结合补少补多成本进行预测
#如果补多>补少，预测少一点，用前两周的销量*0.8
#如果补少>补多，预测多一点，用前两周的销量*1.2
val_cost = pd.read_csv('../val/16_09_window1_pred_y.csv')
val_cost_1 = val_cost[val_cost.store_code=='1'].iloc[0:2,:][['item_id','store_code','y']]
val_cost_2 = val_cost[val_cost.store_code=='2'].iloc[0:2,:][['item_id','store_code','y']]
val_cost_3 = val_cost[val_cost.store_code=='3'].iloc[0:3,:][['item_id','store_code','y']]
val_cost_4 = val_cost[val_cost.store_code=='4'].iloc[0:4,:][['item_id','store_code','y']]
val_cost_5 = val_cost[val_cost.store_code=='5'].iloc[0:1,:][['item_id','store_code','y']]
val_cost_all = val_cost[val_cost.store_code=='all'].iloc[0:17,:][['item_id','store_code','y']]
replace_item = pd.concat([val_cost_all,val_cost_5,val_cost_4,val_cost_3,val_cost_2,val_cost_1])
replace_item.iloc[[1,5,6,7,8,12,16,17,19,22,27],2] *= 1.2 
replace_item.iloc[[4,10,11,13,15,21,24],2] *= 0.8


#合并模型与规则的预测
t = pd.merge(t,replace_item,on=['item_id','store_code'],how='left')
t.fillna(-999,inplace=True)
t_1 = t[t.y==-999][['item_id','store_code','pred']]
t_2 = t[t.y!=-999][['item_id','store_code','y']]
t_2.rename(columns={'y':'pred'},inplace=True)

t = pd.concat([t_1,t_2])
t.pred = t.pred.apply(lambda x:round(x))  #取整

t[['item_id','store_code','pred']].to_csv('ensemble_1109_7525_final.csv',index=None,header=None)  #最终提交文件

