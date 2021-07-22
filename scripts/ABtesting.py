
import pandas as pd
import numpy as np
import logging
from scipy import stats

logging.basicConfig(filename='../applogs/ABtesting.log', filemode='w', format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',level=logging.DEBUG)



class ABTesting:




    def __init__(self,data):
        logging.info("Initializing Class")
        self.data=data


    def splitExperiments(self):
        #this function splits our datasets according to our experiment campaign
        exposed=self.data[self.data['experiment']=='exposed']
        control=self.data[self.data['experiment']=='control']

        return exposed,control 

    def ctrCampaign(self,exposed,control):
        #we caculate the success rate of each campaign
        #we term success as interacting and getting a yes

        #number of interacted users
        #then caclualte the probalility of getting a positive repsonse

        #ctr=number of yes/total number of events

    
        n1=(exposed['yes'].sum()+exposed['no'].sum())
        probExposed=exposed['yes'].sum()/float(n1)

        n2=(control['yes'].sum()+control['no'].sum())
        probControl=control['yes'].sum()/float(n2)

        lift=probExposed-probControl

        return probExposed,probControl,lift,n1,n2

    def tTest(self,exposed,control,n1,n2,d,alpha):

        #lets caclulate the probaility of getting a positive repsonse
        overallProbaility=(exposed['yes'].sum()+control['yes'].sum())/(n1+n2)

        standaradError1=(overallProbaility*(1-overallProbaility))/n1
        standaradError2=(overallProbaility *(1-overallProbaility))/n2

        standardError=np.sqrt(float(standaradError1)+float(standaradError2))

        #we calculate the t-statistic
        tStatistic=(d-0)/ standardError

        #degree of freedom

        dof=(n1+n2-2.0)

        #calulate the t-value

        criticalValue=stats.t.ppf(1.0 -alpha,df=dof )

        #calculate confidence Interval
        confInt=[d-(criticalValue * standardError),d+(criticalValue * standardError)]

        p_value=(1-stats.t.cdf(abs(tStatistic),df=(n1 + n2-2))) *2.0

        return standaradError1,standaradError2,standardError,tStatistic,criticalValue,confInt,p_value
 


    