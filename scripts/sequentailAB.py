



import pandas as pd
import numpy as np

class SequentialTest:

    def __init__(self,exposed,control,alpha,beta,odd_ratio):
        self.exposed=exposed
        self.control=control
        self.alpha=alpha
        self.beta=beta
        self.odd_ratio=odd_ratio


    def stoppingRule(self):
        '''
        This function should take current observation and return statistical decision made. 
        Consider truncate rule for longer tests
        '''
        
        criticalUpper,criticalLower=self.computeBoundaries()
        if criticalLower >= S:
            print("Reject the Null hypothesis")

        elif S <= upperLimit:
            print("Accept Null hypothesis")
        



    def computeBoundaries(self):
        '''
        This function shoud compute boundaries 

        

        '''
        criticalUpper=np.log(self.beta/(1-self.alpha))
        criticalLower=np.log((1-self.beta)/self.alpha)

        return criticalUpper,criticalLower

    def plotTest(self,):
        '''
        showing the cumulative statistical test (e.g., log probability ratio) and the uper and lower limits.
        '''

    def plotBoundaries(self,):
        '''cumulative sums of exposed successes, bounded by the critical limits.
        '''

            