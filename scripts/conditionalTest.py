

import pandas as pd
import numpy as np

class ConditionalSPRT:

    def __init__(self,exposed,control,odd_ratio,alpha=0.05,beta=0.10,stop=None):
        self.exposed=exposed
        self.control=control
        self.odd_ratio=odd_ratio
        self.alpha=alpha
        self.beta=beta
        self.stop=stop

    def ConditionalSPRT(self,x,y,t1):
        