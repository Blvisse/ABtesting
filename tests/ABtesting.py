import unittest
import pandas as pd
import sys,os

module_path =os.path.abspath(os.path.join('..'))
if module_path not in sys.path:
    sys.path.append(module_path+"\\scripts")

if module_path not in sys.path:
    sys.path.append(module_path+"\\models")

from loadDvc import getData


class Tests(unittest.TestCase):

    def __init__ (self):
        pass
        
    
    def checkforPlatform(self):
        #check to see if the data versions have the same data 
        #platform version shouldn't contain browser column
        #while browser shouldn't contain platform column
        pdata=getData('data/AdSmartABdata.csv','https://github.com/Blvisse/ABtesting','cbf35f6e43a99698ba53718ed8a8c8da8f3da722')
        counter=0
        if 'browser' in pdata.columns:
            counter = 1
            return counter
        
        else:
            counter = 2

            return counter

        self.assertEqual(counter , 2)
    def fullDataset(self):

        pdata=getData('data/AdSmartABdata.csv','https://github.com/Blvisse/ABtesting','cbf35f6e43a99698ba53718ed8a8c8da8f3da722')
        #check to confirm 8 columns
        self.assertEqual(pdata.shape[1],8)
    def checkforBrowser(self):
                #check to see if the data versions have the same data 
        #platform version shouldn't contain browser column
        #while browser shouldn't contain platform column
        bdata=getData('data/AdSmartABdata.csv','https://github.com/Blvisse/ABtesting','f2ee815f7d230722139cdb43b3817f44a1ce9064')
        counter=0
        if 'platform_os' in bdata.columns:
            counter = 1
            return counter
        
        else:
            counter = 2

            return counter

        self.assertEqual(counter , 2)
    def checkNulls(self):

        #select column and check for nulls
        bdata=getData('data/AdSmartABdata.csv','https://github.com/Blvisse/ABtesting','f2ee815f7d230722139cdb43b3817f44a1ce9064')
        

        self.assertEqual(bdata['broswer'].isnull().sum(),0)



if __name__ == '__main__':
	unittest.main()      





