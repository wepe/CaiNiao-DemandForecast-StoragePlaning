import pandas as pd



svrlinear1 = pd.read_csv('test/val_56579.6714533.csv')
svrlinear2 = pd.read_csv('test/val_67694.7496993.csv')
svrlinear3 = pd.read_csv('test/val_116090.214836.csv')
svrlinear4 = pd.read_csv('test/val_140788.8249.csv')
svrlinear5 = pd.read_csv('test/val_149083.179453.csv')
svrlinearall = pd.read_csv('test/val_1130762.22469.csv')

pred = pd.concat([svrlinearall,svrlinear1,svrlinear2,svrlinear3,svrlinear4,svrlinear5])


pred[['item_id','store_code','pred']].to_csv('svr_linear_166.csv',index=None,header=None)
