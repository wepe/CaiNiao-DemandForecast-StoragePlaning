#coding=utf-8
import pandas as pd


#合并各个分仓的预测值
xgb1 = pd.read_csv('xgb_1/val_pred_70050.2551423.csv')
xgb2 = pd.read_csv('xgb_2/val_pred_57397.6172493.csv')
xgb3 = pd.read_csv('xgb_3/val_pred_149219.413656.csv')
xgb4 = pd.read_csv('xgb_4/val_pred_170979.811645.csv')
xgb5 = pd.read_csv('xgb_5/val_pred_121922.035419.csv')
xgball = pd.read_csv('xgb_all/val_pred_1245843.34623.csv')

pred = pd.concat([xgball,xgb1,xgb2,xgb3,xgb4,xgb5])


pred[['item_id','store_code','pred']].to_csv('xgb_181.csv',index=None,header=None)

