import pandas as pd




svrall = pd.read_csv('test/test_1.csv')
svr1 = pd.read_csv('test/test_2.csv')
svr2 = pd.read_csv('test/test_3.csv')
svr3 = pd.read_csv('test/test_4.csv')
svr4 = pd.read_csv('test/test_5.csv')
svr5 = pd.read_csv('test/test_all.csv')

pred = pd.concat([svrall,svr1,svr2,svr3,svr4,svr5])


pred[['item_id','store_code','pred']].to_csv('svr_rbf.csv',index=None,header=None) 
