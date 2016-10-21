import pandas as pd


def cal_cost(y,pred,a,b):
    cost = 0
    nb_sample = len(y)
    for i in range(nb_sample):
        if pred[i]>y[i]:
            cost += b[i]*(pred[i]-y[i])
        else:
            cost += a[i]*(y[i]-pred[i])
    return nb_sample,cost


a_b = pd.read_csv('../data/config1.csv')
val_pred = pd.read_csv('val.csv')
val_pred.pred = val_pred.pred.apply(lambda x:max(x,0.0))
val_y = pd.read_csv('val_y.csv')

pred_y = pd.merge(val_pred,val_y,on=['item_id','store_code'],how='left')
pred_y = pd.merge(pred_y,a_b,on=['item_id','store_code'],how='left')
print cal_cost(pred_y.qty_alipay_njhs,pred_y.pred,pred_y.a,pred_y.b)
