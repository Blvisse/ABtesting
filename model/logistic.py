import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score,f1_score,confusion_matrix,precision_score
from sklearn.preprocessing import StandardScaler
import mlflow
import mlflow.sklearn
from sklearn.model_selection import RandomizedSearchCV,KFold
from scipy.stats import loguniform
from sklearn.model_selection import cross_val_score

import sys
import os
import pandas as pd
import logging


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

        ss=StandardScaler()

        X_train,X_test,y_train,y_test=train_test_split(X,y,test_size=.10,random_state=0)
        X_train=ss.fit_transform(X_train)
        X_test=ss.transform(X_test)
        X_train,X_val,y_train,y_val=train_test_split(X_train,y_train,test_size=.20,random_state=0)

        return X_train,X_test,y_train,y_test,X_val,y_val

    def trainModel(self):
        mlflow.set_experiment("Base Linear Regressor")
        print("Splitting data..")
        X_train,X_test,y_train,y_test,X_val,y_val=self.splitData()
     

        


        with mlflow.start_run():

            print("Fitting Logistic Regressor to the data")

            lr=LogisticRegression()
            lr.fit(X_train,y_train)
            prediction=lr.predict(X_test)
            accuracy=accuracy_score(y_test,prediction)
            f1=f1_score(y_test,prediction,average='weighted',labels=np.unique(prediction))
            precision=precision_score(y_test,prediction,average='weighted',labels=np.unique(prediction))
  
            mlflow.log_metric("f1", f1)
            mlflow.log_metric("accuracy",accuracy)
            mlflow.log_metric("precision", precision)
            print("Accuray {} ----- precision {},-----f1 score {} ".format(accuracy,precision,f1))
            mlflow.sklearn.log_model(lr, "Base Logistic Regressor")
    
    def KFoldDataSplit(self):

        mlflow.set_experiment("Logistic Regression KFold")


        X=self.data.drop(labels=['positive_engagement'],axis=1)
        y=self.data['positive_engagement']
        ss=StandardScaler()

        logging.debug("Scaling data")
        print ("Scaling data.. \n ")
        X=ss.fit_transform(X)

        logging.debug("Initialize KFold validator with 5 splits \n")
        print("Applying 5 fold cross validation")

        kf= KFold(n_splits=5)
        splits=1

       

        logging.debug("Split training number {}".format(splits))
        lr=LogisticRegression()

       
            
        
        for train_index, test_index in kf.split(X):
    
            print("Train:", train_index, "Validation:",test_index)
            X_train, y_train = X[train_index], y[train_index] 
            X_test, y_test = X[test_index], y[test_index]
            
            with mlflow.start_run():
                
                print("Training and spliting data.. fold number {} \n".format(splits))
               
                lr.fit(X_train,y_train)
               
                prediction=lr.predict(X_test)
                # valaccuracy=accuracy_score(y_val,validationprediction)
                accuracy=accuracy_score(y_test,prediction)
                cm =confusion_matrix(y_test,prediction)
                f1=f1_score(y_test,prediction,average='weighted',labels=np.unique(prediction))
                # valf1=f1_score(y_val,validationprediction,average='weighted',labels=np.unique(validationprediction))

                precision=precision_score(y_test,prediction,average='weighted',labels=np.unique(prediction))
                # valprecision=precision_score(y_val,validationprediction,average='weighted',labels=np.unique(validationprediction))
                
                print("Accuracy for split {} ----,{} ----- precision {},-----f1 score {} \n".format(splits,accuracy,precision,f1))
              
                mlflow.log_param("validation fold",splits)
                # mlflow.log_param("min_sample",min_sample_leaf)
                mlflow.log_metric("f1", f1)
                # mlflow.log_metric("validation f1", valf1)
                # mlflow.log_metric("Confusion Matrix",cm)

                mlflow.log_metric("accuracy",accuracy)
                # mlflow.log_metric(" validation accuracy", valaccuracy)
                mlflow.log_metric("precision", precision)
                # mlflow.log_metric("validation precison",valprecision)
                
                mlflow.sklearn.log_model(lr, "Logistic Regressor")



                splits+=1

            mlflow.end_run()
            

    def hyperParamModel(self):
        mlflow.set_experiment("Hyper-Parameter Regression")
        X_train,X_test,y_train,y_test,X_val,y_val=self.splitData()
        
        lr=LogisticRegression()
        # space = dict()
        solver = ['liblinear']
        penalty= ['l2']
        # space['C'] = loguniform(1e-5, 100)

        
        for pen in penalty:

            with mlflow.start_run():
                lr=LogisticRegression(penalty=pen)
                lr.fit(X_train,y_train)
                prediction=lr.predict(X_test)
                accuracy=accuracy_score(y_test,prediction)
                f1=f1_score(y_test,prediction,average='weighted',labels=np.unique(prediction))
                precision=precision_score(y_test,prediction)
                print("Current Parameters: Penalty {}".format(pen))
                print("Model Metrics: Accuracy   ----,{} ----- precision {},-----f1 score {} \n".format(accuracy,precision,f1))
              
                mlflow.log_param("penalty",pen)
                mlflow.log_metric("f1", f1)
                mlflow.log_metric("accuracy",accuracy)
                mlflow.log_metric("precision", precision)

                mlflow.sklearn.log_model(lr, "Logistic_Regressor_Model")
                    
                    # mpath="/trainedModels" % (accuracy,f1)

                    # mlflow.sklearn.save_model(lr, mpath)
                    
                    # mlflow.log_artifact("LR.png")

            

if __name__ == '__main__':
    dvcInstance=dvcData()
    data=dvcInstance.getData('data/AdSmartABdata.csv','https://github.com/Blvisse/ABtesting','cbf35f6e43a99698ba53718ed8a8c8da8f3da722')
    lrIntsance=LR(data)
    df=lrIntsance.cleancolumns(['experiment','device_make','platform_os'])
    lrIntsance=LR(df)
    lrIntsance.trainModel()
    print (df)


