import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import scipy.stats as ss
import logging
import math

logging.basicConfig(filename='../applogs/classicalAB.log', filemode='w', format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',level=logging.DEBUG)



class classicalABTesting:

    def __init__(self,data):
        self.data=data

    def convertData(self):
        #creating distinctive groups for exposed and control groups
        
        self.data['hour+day']=self.data['date'].apply(lambda x: pd.Timestamp(x,tz=None).strftime('%Y-%m-%d:%H'))

       
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

    def ConditionalSPRT(self,t1,alpha=0.05,beta=0.10,stop=None):
        x=self.convertData()[0]
        y=self.convertData()[1]


        if t1<=1:
            logging.warning('warning',"Odd ratio should exceed 1.")
        if (alpha >0.5) | (beta >0.5):
            logging.warning('warning',"Unrealistic values of alpha or beta were passed."
                     +" You should have good reason to use large alpha & beta values")
        if stop!=None:
            stop=math.floor(n0)

        def comb(n, k):
            return math.factorial(n) // math.factorial(k) // math.factorial(n - k)
        
        def lchoose(b, j):
            a=[]
            if (type(j) is list) | (isinstance(j,np.ndarray)==True):
                if len(j)<2:
                    j=j[0]
            if (type(j) is list) | (isinstance(j,np.ndarray)==True):
                for k in j:
                    n=b
                    if (0 <= k) & (k<= n):
                        a.append(math.log(comb(n,k)))
                    else:
                        a.append(0)
            else:
                n=b
                k=j
                if (0 <= k) & (k<= n):
                    a.append(math.log(comb(n,k)))
                else:
                    a.append(0)

            return np.array(a)

        def g(x,r,n,t1,t0=1):

         
            return -math.log(h(x,r,n,t1))+math.log(h(x,r,n,t0))

        def h(x,r,n,t=1):
         
            return f(r,n,t,offset=ftermlog(x,r,n,t))

        def f(r,n,t,offset=0):
      
            upper=max(0,r-n)
            lower=min(n,r)
            rng=list(range(upper,lower+1))
            return np.sum(fterm(rng,r,n,t,offset))

        def fterm(j,r,n,t,offset=0):
            ftlog=ftermlog(j,r,n,t,offset)
            return np.array([math.exp(ex) for ex in ftlog])

        def ftermlog(j,r,n,t,offset=0):
  
            xx=r-j
            lch=lchoose(n,j)
            lchdiff=lchoose(n,xx)
            lg=np.array(j)*math.log(t)
            lgsum=lch+lchdiff
            lgsum2=lgsum+lg
            lgdiff=lgsum2-offset

            return lgdiff

        def logf(r,n,t,offset=0):
            z=f(r,n,t,offset)
            if z>0:
                return math.log(z)
            else:
                return np.nan

        def clowerUpper(r,n,t1c,t0=1,alpha=0.05,beta=0.10):
       
            offset=ftermlog(math.ceil(r/2),r,n,t1c)
            z=logf(r,n,t1c,logf(r,n,t0,offset)+offset)
            a=-math.log(alpha/(1-beta))
            b=math.log(beta/(1-alpha))
            lower=b
            upper=1+a
            return (np.array([lower,upper])+z)/math.log(t1c/t0)

        l=math.log(beta/(1-alpha))
        u=-math.log(alpha/(1-beta))
        sample_size=min(len(x),len(y))
        n=np.array(range(1,sample_size+1))

        if stop!=None:
            n=np.array([z for z in n if z<=stop])
        x1=np.cumsum(x[n-1])
        r=x1+np.cumsum(y[n-1])
        stats=np.array(list(map(g,x1, r, n, [t1]*len(x1)))) #recurcively calls g
         #
          # Perform the test by finding the first index, if any, at which `stats`
          # falls outside the open interval (l, u).
          #
        clu=list(map(clowerUpper,r,n,[t1]*len(r),[1]*len(r),[alpha]*len(r), [beta]*len(r)))
        limits=[]
        for v in clu:
            inArray=[]
            for vin in v:
                inArray.append(math.floor(vin))
            limits.append(np.array(inArray))
        limits=np.array(limits)

        k=np.where((stats>=u) | (stats<=l))
        cvalues=stats[k]
        if cvalues.shape[0]<1:
            k= np.nan
            outcome='Unable to conclude.Needs more sample.'
        else:
            k=np.min(k)
            if stats[k]>=u:
                outcome=f'Exposed group produced a statistically significant increase.'
            else:
                outcome='Their is no statistically significant difference between two test groups'
        if (stop!=None) & (k==np.nan):
          #
          # Truncate at trial stop, using Meeker's H0-conservative formula (2.2).
          # Leave k=NA to indicate the decision was made due to truncation.
          #
            c1=clowerUpper(r,stop,t1,alpha,beta)
            c1=math.floor(np.mean(c1)-0.5)
            if x1[n0]<=c1:
                truncate_decision='h0'
                outcome='Maximum Limit Decision. The aproximate decision point shows their is no statistically significant difference between two test groups'
            else:
                truncate_decision='h1'
                outcome=f'Maximum Limit Decision. The aproximate decision point shows exposed group produced a statistically significant increase.'
            truncated=stop
        else:
            truncate_decision='Non'
            truncated=np.nan
        return (outcome,n, k,l,u,truncated,truncate_decision,x1,r,stats,limits)

        






    