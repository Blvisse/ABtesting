import unittest
import pandas as pd
import sys,os

module_path =os.path.abspath(os.path.join('..'))
if module_path not in sys.path:
    sys.path.append(module_path+"\\scripts")

if module_path not in sys.path:
    sys.path.append(module_path+"\\model")

from loadDvc import dvcData
dvcInstance=dvcData()


class TestsAB(unittest.TestCase):

    
    
    def test_checkforPlatform(self):
        #check to see if the data versions have the same data 
        #platform version shouldn't contain browser column
        #while browser shouldn't contain platform column
        pdata=dvcInstance.getData('data/AdSmartABdata.csv','https://github.com/Blvisse/ABtesting','cbf35f6e43a99698ba53718ed8a8c8da8f3da722')
        counter=0
        if 'browser' in pdata.columns:
            counter = 1
            return counter
        
        else:
            counter = 2

            return counter

        self.assertEqual(counter , 2)
    def test_fullDataset(self):

        pdata=dvcInstance.getData('data/AdSmartABdata.csv','https://github.com/Blvisse/ABtesting','cbf35f6e43a99698ba53718ed8a8c8da8f3da722')
        #check to confirm 8 columns
        self.assertEqual(pdata.shape[1],8)
    def test_checkforBrowser(self):
                #check to see if the data versions have the same data 
        #platform version shouldn't contain browser column
        #while browser shouldn't contain platform column
        bdata=dvcInstance.getData('data/AdSmartABdata.csv','https://github.com/Blvisse/ABtesting','f2ee815f7d230722139cdb43b3817f44a1ce9064')
        counter=0
        if 'platform_os' in bdata.columns:
            counter = 1
            return counter
        
        else:
            counter = 2

            return counter

        self.assertEqual(counter , 2)
    def test_checkNulls(self):

        #select column and check for nulls
        #we select the experiment column to ensure everyone recorded was allocated 
        bdata=dvcInstance.getData('data/AdSmartABdata.csv','https://github.com/Blvisse/ABtesting','f2ee815f7d230722139cdb43b3817f44a1ce9064')
        

        self.assertEqual(bdata['experiment'].isnull().sum(),0)


   

if __name__ == '__main__':
    unittest.main()


