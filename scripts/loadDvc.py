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

    def __init__(self,path,repo):
        logging.debug("Initiaizing class")
        self.path=path
        # self.version=version
        self.repo=repo

    def getData(self):
        try:
            data_url=dvc.api.get_url(path=self.path,repo=self.repo)
            data=pd.read_csv(data_url)
            mlflow.log_param("data_url",data_url)
            mlflow.log_param("data_version",self.version)
            mlflow.log_param("input_rows",self.data.shape[0])
            mlflow.log_param("input_cols",self.data.shape[1])

            return data_url
            

        except Exception as e:

            logging.error("The following error occured {} ".format(e))





# path='data/AdSmartABdata.csv'
# repo=
# version='v1'

if (__name__== '__main__'):
    instance=dvcData('get-started/data.xml','https://github.com/iterative/dataset-registry')
    data=instance.getData()
    print(data)

