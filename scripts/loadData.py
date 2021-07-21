"""
This script module reads and loads data

"""

import pandas as pd
import logging

logging.basicConfig(filename='../applogs/loaddata.log', filemode='w', format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',level=logging.DEBUG)

class READ:

    def __init__(self,path):
        logging.debug("Initializing Class")
        self.path=path
        logging.info("Successfuly initialized class ")


    def readData(self):

        #read csv into pandas data frame
        try:
            logging.debug("Reading CSV File")
            print("Reading csv file..\n")
            data=pd.read_csv(self.path)
            print("File read successfully\n")
            logging.info("Successfully Read File")

            return data
        except Exception as e:
            logging.error("Run into Error{}".format(e.__class__))
            print("Wooops the followng error occured {}".format(e.__class__.__name__))

    

if (__name__ == "__main__"):

    classInstance=READ('../data/AdSmartABdata.csv')
    data=classInstance.readData()
    