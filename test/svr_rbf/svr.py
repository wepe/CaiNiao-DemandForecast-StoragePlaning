#coding=utf-8
import pandas as pd
import xgboost as xgb
import numpy as np
from sklearn.cross_validation import train_test_split
from sklearn.preprocessing import MinMaxScaler
from sklearn.svm import SVR
import os,cPickle,random





a_b = pd.read_csv('../../data/config1.csv')


data = pd.read_csv('../../../data/train_test.csv')
hashmap = {1:'1',2:'2',3:'3',4:'4',5:'5',6:'all'}
data.store_code = data.store_code.apply(lambda x:hashmap[x])

data = pd.merge(data,a_b,on=['item_id','store_code'])

#
data = data[data.store_code=='all']

def pipeline():

        #
        test = data[data.watch==0]
        test_a_b = test[['item_id','store_code','a','b']]
        test_x = test.drop(['label','watch','item_id','store_code','a','b'],axis=1)
        test_x.fillna(test_x.median(),inplace=True)

       
        train = data[data.watch!=0]
        
        train_y = train.label

        
        a = list(train.a)
        b = list(train.b)
        train_weight = []
        for i in range(len(a)):
            #train_weight.append(min(a[i],b[i]))
            train_weight.append(a[i]+b[i])
        train_weight = np.array(train_weight)

        train_x = train.drop(['label','watch','item_id','store_code','a','b'],axis=1)

        train_x.fillna(train_x.median(),inplace=True)

        scaler = MinMaxScaler()
        scaler.fit(train_x)
        train_x = scaler.transform(train_x)
        test_x = scaler.transform(test_x)
        
        #model = SVR(kernel='rbf',cache_size=2000,gamma=0.01,C=3.5)#1
        #model = SVR(kernel='rbf',cache_size=2000,gamma=0.01,C=3.5)#2
        #model = SVR(kernel='rbf',cache_size=2000,gamma=0.01,C=3.5)#3
        model = SVR(kernel='rbf',cache_size=2000,gamma=0.01,C=3.5)

	#train
	model.fit(train_x,train_y, sample_weight=train_weight)

	#predict test set
        test_a_b['pred'] = model.predict(test_x)
        test_a_b.to_csv('test/test_all.csv',index=None)
        


if __name__ == "__main__":
        pipeline()
