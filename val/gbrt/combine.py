import pandas as pd




gbrt1 = pd.read_csv('gbrt_5/val_121209.078303.csv')
gbrt2 = pd.read_csv('gbrt_4/val_176515.038384.csv')
gbrt3 = pd.read_csv('gbrt_3/val_153530.211507.csv')
gbrt4 = pd.read_csv('gbrt_2/val_56048.8698256.csv')
gbrt5 = pd.read_csv('gbrt_1/val_71828.1826314.csv')
gbrtall = pd.read_csv('gbrt_all/val_1213120.20938.csv')

pred = pd.concat([gbrtall,gbrt1,gbrt2,gbrt3,gbrt4,gbrt5])

print pred
pred[['item_id','store_code','pred']].to_csv('gbrt_166.csv',index=None,header=None)
