

import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split,KFold
import xgboost as xgb

from sklearn.metrics import accuracy_score,f1_score,confusion_matrix,precision_score
from sklearn.preprocessing import StandardScaler
import logging


import matplotlib.pyplot as plt
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

logging.basicConfig(filename='../applogs/xbg.log', filemode='w', format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',level=logging.DEBUG)



class XG:

    def __init__(self,data):
        logging.debug("Initializing Class")
        self.data=data

    def cleancolumns(self,cols):

        try:
            logging.debug("Accessing cleancolumns function")
            logging.info("Acquiring Dataset")
            print("Getting dataset")
            data=pd.get_dummies(self.data,columns=cols)
            
            logging.info("Creating features")
            print("Creating features")
            data['positive_engagement']=np.where((data['yes']==1)& (data['no']==0),1,0)
            data.drop(labels=['auction_id','yes','no','date'],axis=1,inplace=True)

            print("Done..")
        except Exception as e:

            logging.error("Encountered {} error ".format(e))
            print("The program encountred and error..")
            print("Details... {} ".format(e))


        return data 



    
    def splitData(self, **kwargs):

        try:
            logging.debug("Initializing splitData function")
            
            self.data.reset_index()
            logging.info("Spliting data into X and Y")
            X=self.data.drop(labels=['positive_engagement'],axis=1)
            y=self.data['positive_engagement']
            

            
            logging.debug("Initializing Standard Scaler")
            ss=StandardScaler()

            print("Spliting data into train,test samples")
            logging.info("Data spliting")
            X_train,X_test,y_train,y_test=train_test_split(X,y,test_size=.10,random_state=0)
            
            print("Fitting transformer")
            logging.debug("Fitting transformer")
            X_train=ss.fit_transform(X_train)
            X_test=ss.transform(X_test)
            X_train,X_val,y_train,y_val=train_test_split(X_train,y_train,test_size=.20,random_state=0)

            print ("Done..")
        except Exception as e:
            logging.error("Encountered {} error ".format(e))
            print("The program encountred and error..")
            print("Details... {} ".format(e))

        # print (X.train.shape)
        
        return X_train,X_test,y_train,y_test,X_val,y_val

    def KFoldDataSplit(self,max_depth,min_sample_leaf,max_features):
        mlflow.set_experiment("Decision Tree Classifier KFold")
        X=self.data.drop(labels=['positive_engagement'],axis=1)
        y=self.data['positive_engagement']
        logging.debug("Initialize KFold validator with 5 splits")
        print("Applying 5 fold cross validation")
        kf= KFold(n_splits=5)
        splits=1

        print("Training and spliting data.. fold number {} ".format(splits))

        logging.debug("Split training number {}".format(splits))
        dt=xgb.XGBClassifier(n_estimators=100,max_depth=3)

       
            
        
        for train_index, test_index in kf.split(X):
    
            print("Train:", train_index, "Validation:",test_index)
            X_train, y_train = X.loc[train_index], y.loc[train_index] 
            X_test, y_test = X.loc[test_index], y.loc[test_index]
            
            with mlflow.start_run():
                
                print("Training and spliting data.. fold number {} ".format(splits))
               
                dt.fit(X_train,y_train)
                plt.figure(figsize=(10,9))
               
                # validationprediction=dt.predict(X_)
                prediction=dt.predict(X_test)
                # valaccuracy=accuracy_score(y_val,validationprediction)
                accuracy=accuracy_score(y_test,prediction)
                cm =confusion_matrix(y_test,prediction)
                f1=f1_score(y_test,prediction,average='weighted',labels=np.unique(prediction))
                # valf1=f1_score(y_val,validationprediction,average='weighted',labels=np.unique(validationprediction))

                precision=precision_score(y_test,prediction,average='weighted',labels=np.unique(prediction))
                # valprecision=precision_score(y_val,validationprediction,average='weighted',labels=np.unique(validationprediction))
                
                mlflow.log_param("max_depth", max_depth)
                mlflow.log_param("max_features", max_features)
                mlflow.log_param("validation fold",splits)
                # mlflow.log_param("min_sample",min_sample_leaf)
                mlflow.log_metric("f1", f1)
                # mlflow.log_metric("validation f1", valf1)
                # mlflow.log_metric("Confusion Matrix",cm)

                mlflow.log_metric("accuracy",accuracy)
                # mlflow.log_metric(" validation accuracy", valaccuracy)
                mlflow.log_metric("precision", precision)
                # mlflow.log_metric("validation precison",valprecision)
                mlflow.sklearn.log_model(dt, "XGBoost Classifier")


                splits+=1

            mlflow.end_run()

        

    

    def trainModel(self,max_depth,min_sample_leaf,max_features):
        mlflow.set_experiment("Decision Tree Classifier")
        
        logging.debug("Initializing trainModel function")
        
        X_train,X_test,y_train,y_test,X_val,y_val=self.splitData()
        # max_depth=[1,2,3,4]
        # min_sample_leaf=[3,4,5]
        # max_features=[3,4,5]

        #we split data into 5 folds sing kfold cross validation
        logging.debug("Initialize KFold validator with 5 splits")
       

     



        

        logging.debug("Logging into MLFlow")
        print("Training and logging to mlflow")
        with mlflow.start_run():
                

            dt=xgb.XGBClassifier(n_estimators=100,max_depth=3)
            dt.fit(X_train,y_train)
            plt.figure(figsize=(10,9))
            
            validationprediction=dt.predict(X_val)
            prediction=dt.predict(X_test)
            valaccuracy=accuracy_score(y_val,validationprediction)
            accuracy=accuracy_score(y_test,prediction)
            cm =confusion_matrix(y_test,prediction)
            f1=f1_score(y_test,prediction,average='weighted',labels=np.unique(prediction))
            valf1=f1_score(y_val,validationprediction,average='weighted',labels=np.unique(validationprediction))

            precision=precision_score(y_test,prediction,average='weighted',labels=np.unique(prediction))
            valprecision=precision_score(y_val,validationprediction,average='weighted',labels=np.unique(validationprediction))
                
            mlflow.log_param("max_depth", max_depth)
            mlflow.log_param("max_features", max_features)
            
                # mlflow.log_param("min_sample",min_sample_leaf)
            mlflow.log_metric("f1", f1)
            mlflow.log_metric("validation f1", valf1)
                # mlflow.log_metric("Confusion Matrix",cm)

            mlflow.log_metric("accuracy",accuracy)
            mlflow.log_metric(" validation accuracy", valaccuracy)
            mlflow.log_metric("precision", precision)
            mlflow.log_metric("validation precison",valprecision)
            mlflow.sklearn.log_model(dt, "Decision Tree Classifier")


            
                
                
                # mpath="/trainedModelsLR" % (accuracy,f1)

                # mlflow.sklearn.save_model(dt, mpath)
                
                # mlflow.log_artifact("dt.png")

    


if __name__ == '__main__':
    dvcInstance=dvcData()
    data=dvcInstance.getData('data/AdSmartABdata.csv','https://github.com/Blvisse/ABtesting','cbf35f6e43a99698ba53718ed8a8c8da8f3da722')
    lrIntsance=XG(data)
    df=lrIntsance.cleancolumns(['experiment','device_make','platform_os'])
    lrIntsance=XG(df)
    lrIntsance.trainModel(6,3,5)
    print (df)


