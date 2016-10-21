import pandas as pd




rf1 = pd.read_csv('rf_5/test_5.csv')
rf2 = pd.read_csv('rf_4/test_4.csv')
rf3 = pd.read_csv('rf_3/test_3.csv')
rf4 = pd.read_csv('rf_2/test_2.csv')
rf5 = pd.read_csv('rf_1/test_1.csv')
rfall = pd.read_csv('rf_all/test_all.csv')

pred = pd.concat([rfall,rf1,rf2,rf3,rf4,rf5])

print pred
pred[['item_id','store_code','pred']].to_csv('rf.csv',index=None,header=None)
