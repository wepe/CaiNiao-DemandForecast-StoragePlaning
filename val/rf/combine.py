import pandas as pd




rf1 = pd.read_csv('rf_5/val_130800.275439.csv')
rf2 = pd.read_csv('rf_4/val_156574.936926.csv')
rf3 = pd.read_csv('rf_3/val_152693.371671.csv')
rf4 = pd.read_csv('rf_2/val_60469.3043581.csv')
rf5 = pd.read_csv('rf_1/val_63374.1571854.csv')
rfall = pd.read_csv('rf_all/val_1173509.50047.csv')

pred = pd.concat([rfall,rf1,rf2,rf3,rf4,rf5])

print pred
pred[['item_id','store_code','pred']].to_csv('rf_173.csv',index=None,header=None)
