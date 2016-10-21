import pandas as pd




gbrt1 = pd.read_csv('gbrt_5/gbrt_5.csv')
gbrt2 = pd.read_csv('gbrt_4/gbrt_4.csv')
gbrt3 = pd.read_csv('gbrt_3/gbrt_3.csv')
gbrt4 = pd.read_csv('gbrt_2/gbrt_2.csv')
gbrt5 = pd.read_csv('gbrt_1/gbrt_1.csv')
gbrtall = pd.read_csv('gbrt_all/gbrt_all.csv')

pred = pd.concat([gbrtall,gbrt1,gbrt2,gbrt3,gbrt4,gbrt5])

print pred
pred[['item_id','store_code','pred']].to_csv('gbrt.csv',index=None,header=None)
