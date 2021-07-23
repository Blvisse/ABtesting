import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score,f1_score,confusion_matrix,precision_score
import mlflow
import mlflow.sklearn

import sys
import os
import pandas as pd


module_path =os.path.abspath(os.path.join('..'))
if module_path not in sys.path:
    sys.path.append(module_path+"\\scripts")

if module_path not in sys.path:
    sys.path.append(module_path+"\\models")

from loadDvc import dvcData

dvcInstance=dvcData()


class LR:

    def __init__(self,data):
        self.data=data

    def cleancolumns(self,cols):
        data=pd.get_dummies(self.data,columns=cols)
        
        data['positive_engagement']=np.where((data['yes']==1)& (data['no']==0),1,0)
        data.drop(labels=['auction_id','yes','no','date'],axis=1,inplace=True)

        return data 



    
    def splitData(self, **kwargs):

        
        X=self.data.drop(labels=['positive_engagement'],axis=1)
        y=self.data['positive_engagement']

        X_train,X_test,y_train,y_test=train_test_split(X,y,test_size=.10,random_state=0)
        X_train,X_val,y_train,y_val=train_test_split(X_train,y_train,test_size=.20,random_state=0)

        return X_train,X_test,y_train,y_test,X_val,y_val

    def trainModel(self):
        X_train,X_test,y_train,y_test,X_val,y_val=self.splitData()
        lr=LogisticRegression()


        with mlflow.start_run():
            lr.fit(X_train,y_train)
            prediction=lr.predict(X_test)
            accuracy=accuracy_score(y_test,prediction)
            f1=f1_score(y_test,prediction)
            precision=precision_score(y_test,prediction)
            # mlflow.log_param("accuracy", accuracy)
            mlflow.log_metric("f1", f1)
            mlflow.log_metric("accuracy",accuracy)
            mlflow.log_metric("precision", precision)
            mlflow.sklearn.log_model(lr, "Logistic_Regressor_Model")
            
            mpath="/trainedModels" % (accuracy,f1)

            mlflow.sklearn.save_model(lr, mpath)
            
            mlflow.log_artifact("LR.png")

            

if __name__ == '__main__':
    dvcInstance=dvcData()
    data=dvcInstance.getData('data/AdSmartABdata.csv','https://github.com/Blvisse/ABtesting','cbf35f6e43a99698ba53718ed8a8c8da8f3da722')
    lrIntsance=LR(data)
    df=lrIntsance.cleancolumns(['experiment','device_make','platform_os'])
    lrIntsance=LR(df)
    lrIntsance.trainModel()
    print (df)


