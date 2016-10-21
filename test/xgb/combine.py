import pandas as pd



xgb1 = pd.read_csv('xgb_1/test_1.csv')
xgb2 = pd.read_csv('xgb_2/test_2.csv')
xgb3 = pd.read_csv('xgb_3/test_3.csv')
xgb4 = pd.read_csv('xgb_4/test_4.csv')
xgb5 = pd.read_csv('xgb_5/test_5.csv')
xgball = pd.read_csv('xgb_all/test_all.csv')

pred = pd.concat([xgball,xgb1,xgb2,xgb3,xgb4,xgb5])


pred[['item_id','store_code','pred']].to_csv('xgb.csv',index=None,header=None)

