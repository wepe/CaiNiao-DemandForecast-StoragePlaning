#coding=utf-8
import pandas as pd
import xgboost as xgb
import numpy as np
from sklearn.cross_validation import train_test_split
import os,cPickle,random

a_b = pd.read_csv('../../../data/config1.csv')


data = pd.read_csv('../../../data/train_test.csv')
hashmap = {1:'1',2:'2',3:'3',4:'4',5:'5',6:'all'}
data.store_code = data.store_code.apply(lambda x:hashmap[x])

data = pd.merge(data,a_b,on=['item_id','store_code'])

data = data[data.store_code=='all']



#
test = data[data.watch==0]
test_a_b = test[['item_id','store_code','a','b']]
test_x = test.drop(['label','watch','item_id','store_code','a','b'],axis=1)







def pipeline():
        val = data[data.watch==1]
        val_a_b = val[['item_id','store_code','a','b']]
        val_y = val.label
        val_x = val.drop(['label','watch','item_id','store_code','a','b'],axis=1)

        train = data[data.watch!=0]
        train_y = train.label

        
        a = list(train.a)
        b = list(train.b)
        train_weight = []
        for i in range(len(a)):
            train_weight.append(min(a[i],b[i]))

        train_x = train.drop(['label','watch','item_id','store_code','a','b'],axis=1)

        print train_x.shape,val_x.shape,test_x.shape


        dtrain = xgb.DMatrix(train_x,label=train_y,weight=train_weight)
        dval = xgb.DMatrix(val_x)
        dtest = xgb.DMatrix(test_x)

	params={
	    	'booster':'gbtree',
	    	'objective': 'reg:linear',
		'eval_metric': 'rmse',
	    	'max_depth':5,
	    	'lambda':1000,
		'subsample':0.85,
		'colsample_bytree':0.85,
		'eta': 0.008,
	    	'seed':1024,
	    	'nthread':8
		}

	#train
	watchlist  = [(dtrain,'train')]
	model = xgb.train(params,dtrain,num_boost_round=400,evals=watchlist)


	#predict test set
	test_a_b['pred'] = model.predict(dtest)
	test_a_b.to_csv('test_all.csv',index=None)

if __name__ == "__main__":
    pipeline()
