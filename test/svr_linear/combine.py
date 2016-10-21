import pandas as pd



svrlinear1 = pd.read_csv('test/test_1.csv')
svrlinear2 = pd.read_csv('test/test_2.csv')
svrlinear3 = pd.read_csv('test/test_3.csv')
svrlinear4 = pd.read_csv('test/test_4.csv')
svrlinear5 = pd.read_csv('test/test_5.csv')
svrlinearall = pd.read_csv('test/test_all.csv')

pred = pd.concat([svrlinearall,svrlinear1,svrlinear2,svrlinear3,svrlinear4,svrlinear5])


pred[['item_id','store_code','pred']].to_csv('svr_linear.csv',index=None,header=None)
