import pandas as pd




svrall = pd.read_csv('test/val_58564.1619739.csv')
svr1 = pd.read_csv('test/val_71967.6882087.csv')
svr2 = pd.read_csv('test/val_123117.594466.csv')
svr3 = pd.read_csv('test/val_152524.710242.csv')
svr4 = pd.read_csv('test/val_181307.59507.csv')
svr5 = pd.read_csv('test/val_1290468.77376.csv')

pred = pd.concat([svrall,svr1,svr2,svr3,svr4,svr5])


pred[['item_id','store_code','pred']].to_csv('svr_rbf_187.csv',index=None,header=None) 
