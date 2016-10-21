#coding=utf-8
import pandas as pd
import xgboost as xgb
import numpy as np
from sklearn.cross_validation import train_test_split
from sklearn.ensemble import GradientBoostingRegressor
import os,cPickle,random





a_b = pd.read_csv('../../../data/config1.csv')


data = pd.read_csv('../../../data/train_test.csv')
hashmap = {1:'1',2:'2',3:'3',4:'4',5:'5',6:'all'}
data.store_code = data.store_code.apply(lambda x:hashmap[x])

data = pd.merge(data,a_b,on=['item_id','store_code'])


data = data[data.store_code=='4']






def pipeline():
        val = data[data.watch==0]
        val_a_b = val[['item_id','store_code','a','b']]
        val_x = val.drop(['label','watch','item_id','store_code','a','b'],axis=1)

        train = data[data.watch!=0]
        train_y = train.label

        
        a = list(train.a)
        b = list(train.b)
        train_weight = []
        for i in range(len(a)):
            train_weight.append(min(a[i],b[i]))
        train_weight = np.array(train_weight)

        train_x = train.drop(['label','watch','item_id','store_code','a','b'],axis=1)

        train_x.fillna(train_x.median(),inplace=True)
        val_x.fillna(val_x.median(),inplace=True)
        

        model = GradientBoostingRegressor(loss='lad',learning_rate=0.01,n_estimators=400,subsample=0.75,max_depth=6,random_state=1024, max_features=0.75)

	#train
	model.fit(train_x,train_y, sample_weight=train_weight)


	#predict val set
	val_a_b['pred'] = model.predict(val_x)
        val_a_b.to_csv('gbrt_4.csv',index=None)


if __name__ == "__main__":
    pipeline()
