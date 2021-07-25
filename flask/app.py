"""
Flask app to create an API for our data

"""

import flask 
from flask import request
import pandas as pd

def processData():

    
    exp = request.args.get('experiment')
    hour = request.args.get('hour')
    device = request.args.get('deivce_make')
    platform = request.args.get('platform_os')
    # browser = request.args.get('browser')
    data=pd.DataFrame([[exp,hour,device,platform]],columns=['experiment','hour','device','platform'])

    data=pd.get_dummies(data,columns=['experiment','device','platform'])


    return data

def loadModel():

    pass


app = flask.Flask(__name__)

@app.route("/predict" , methods=['GET','POST'])

def predict():

    data=processData()

    model = loadModel()

    model.predict(data)



app.run(host='0.0.0.0', port=80)


