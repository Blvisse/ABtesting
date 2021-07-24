"""
This scripts imports data from our dvc directory
"""

import dvc.api
import pandas as pd
import logging 
import mlflow


logging.basicConfig(filename='../applogs/DVC.log', filemode='w', format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',level=logging.DEBUG)
mlflow.set_experiment("data")

class dvcData:

    def __init__(self):
        logging.debug("Initiaizing class")
        # self.path=path
        # self.version=version
        # self.repo=repo

    def getData(self,patht,repot,version):

        logging.debug("Initializing getData function")
        
        data_url=dvc.api.get_url(path=patht,repo=repot,rev=version)
        data=pd.read_csv(data_url)
        mlflow.log_param("data_url",data_url)
        mlflow.log_param("data_version",version)
        mlflow.log_param("input_rows",data.shape[0])
        mlflow.log_param("input_cols",data.shape[1])

        mlflow.end_run()

        return data 
            

        # except Exception as e:

        #     logging.error("The following error occured {} ".format(e))

    





if (__name__== '__main__'):
    instance=dvcData()
    data=instance.getData('data/AdSmartABdata.csv','https://github.com/Blvisse/ABtesting','cbf35f6e43a99698ba53718ed8a8c8da8f3da722')
    print(data)

