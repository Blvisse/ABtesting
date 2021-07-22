"""
This script performs Exploratory Data analysis
"""

import pandas as pd
import numpy as np
import logging
import seaborn as sns
import matplotlib.pyplot as plt



sns.set_style('darkgrid')

logging.basicConfig(filename='../applogs/eda.log', filemode='w', format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',level=logging.DEBUG)


class EDA:

    def __init__(self,data):
        logging.debug("Class initialization")
        self.data=data

    def calculateMissing(self):
        #This function calculates the number of missing values in the dataset

        try:
            logging.debug("Calculating the missing values")

            sumMissing=self.data.isna().sum()
            percentageMissing=sumMissing/len(self.data)*100

            #create a dataframe to present the findings
            logging.info("Creating Dataframe")
            missingValues=pd.DataFrame(data=[sumMissing,percentageMissing])
            missingValues=missingValues.T
            missingValues.columns=['Total Missing','Percentage Missing']

            logging.info("Missing Values calculated")
            print("The report of missing values is as follows")

            return missingValues
        except  Exception as e:
            logging.error("Error message {} ".format(e.__class__))
            print("The following error occured{} ".format(e.__class__))

    def dropDuplicates(self):
        try:
            logging.debug("Launching duplicates search")
            print("Droppping duplicates\n")
            data=self.data.drop_duplicates()
            dupCount=len(self.data)-len(self.data.drop_duplicates())
            print ("There are {} duplicates in the dataset\n".format(dupCount))
            logging.info("Number of duplicates in the datset are {} ".format(dupCount))

            print("Done dropping duplicates! \n")

            return data 

        except Exception as e:
            logging.info("An erro has occured")
            logging.error("The follocing error occured {} ".format(e.__class__))
            print("The following error occured {} ".format(e.__class__))
        

    def valueCounts(self,columns):
        # function to 
        try:
            logging.debug("Value counts of {} column".format(columns))
            count=self.data[columns].value_counts()
            countDF=pd.DataFrame(data=[count])
            count=count.T 

            return count
        except Exception as e:
            logging.info("An erro occured")
            logging.error("The following error occured {} ".format(e.__class__))
            print("The following error occured {} ".format(e.__class__))

    def histVizualisation(self,col, **kwargs):
        #function to create histogram plots
        try:
            
            logging.info("Plotting histogram")
            plt.figure(figsize=(10,9))
            sns.histplot(data=self.data,x=col,**kwargs)
            plt.title("Histogram of {} column".format(col))

        except Exception as e:
            logging.info("An erro has occured")
            logging.error("The following error occured {} ".format(e.__class__))
            print("The following error occured {} ".format(e.__class__))

    def pieChart(self,col, *args, **kwargs):

        try:
            logging.info("Plotting bar graph")
            #Using matplotlib
            cmap=plt.get_cmap(*args) 
            colors = [cmap(i) for i in np.linspace(0, 1, 8)]
            plt.figure(figsize=(10,9))
            plt.pie(x=self.data[col].value_counts(),shadow=True,colors=colors,autopct='%1.1f%%',labels=self.data[col].value_counts().index)
        
            
            plt.title(*args)
            plt.show()

        except Exception as e:
            logging.info("An erro has occured")
            logging.error("The follocing error occured {} ".format(e.__class__))
            print("The following error occured {} ".format(e.__class__))

    
        
           







