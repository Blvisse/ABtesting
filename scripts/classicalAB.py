import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import scipy.stats as ss
import logging

logging.basicConfig(filename='../applogs/classical.log', filemode='w', format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',level=logging.DEBUG)



class classicalAB:

    def __init__(self,data):
        self.data=data

    def convertData(self):
        #creating distinctive groups for exposed and control groups
        
        exposed=self.data[self.data['experiment']=='exposed']
        control=self.data[self.data['experiment']=='control']


        print("The number of users in each experiment is as follows \n")
        logging.debug("Calulating distribution of data")
        print("The number of exposed users {} \n".format(len(exposed)))
        print("The number of control users {} \n".format(len(control)))

        

        #calculating positive engagments
        positiveEngagmentExposed=exposed[exposed['yes']==1]
        positiveEngagmentControl=control[control['yes']==1]

        logging.debug("Calculating positive interactions")

        print("Those with a positive interaction with the ad \n ")
        print("From the exposed group {} \n".format(len(positiveEngagmentExposed)))
        print("From the control group {} \n".format(len(positiveEngagmentControl)))

        
        noPositiveExposed=len(positiveEngagmentExposed)
        noPositiveControl=len(positiveEngagmentControl)

        logging.debug("Calculating conversion rate")





        probPosExposed,probPosControl=noPositiveExposed/len(exposed),noPositiveControl/len(control)

        print("The conversion rate is \n")
        print("Exposed {} \n".format(probPosExposed))
        print("Control {} \n ".format(probPosControl))

        print("The lift from the experiment is {} ".format(probPosExposed-probPosControl))



        summary=self.data.pivot_table(values='yes',index='experiment',aggfunc=np.sum)
        return exposed,control,noPositiveExposed,noPositiveControl,probPosExposed,probPosControl,summary

    def compareSamples(self):

        probExposed,probControl=self.convertData()

        exposed=self.data[self.data['experiment']=='exposed']
        control=self.data[self.data['experiment']=='control']

        probControl* len(exposed)

        positiveEngagmentExposed=exposed[exposed['yes']==1]
        positiveEngagmentControl=control[control['yes']==1]

        ss.binomial()

        






    