import pickle

import numpy as np

from xgboost import DMatrix
import json

import os


def load_model():
    """ This function loads the model either it is running in a docker container or locally
    Indeed in the two cases, the model is not at the same location"""
    
    env_var = os.environ.get('AM_I_IN_A_DOCKER_CONTAINER', False)
    if env_var:
        print('I am running in a Docker container') 

        with open('./xgb_reg.pkl', 'rb') as f_in:
            model = pickle.load(f_in)
    else:        
         print('I am NOT running in a Docker container')      

         with open('./xgb_reg.pkl', 'rb') as f_in:
            model = pickle.load(f_in)
            
    return model

def predict(model, X):
    X = DMatrix(np.reshape(X, (2,1)))
    preds = model.predict(X)
    return float(preds[0])




def predict_endpoint(coordinates):   

    
    lat = coordinates['lat']
    lon = coordinates['lon']
    
    model = load_model()
    pred = predict(model, [lon, lat])

    result = {
        'wind potential': pred,
        'lat' : lat,
        'lon' : lon
    }

    return result


def handler(event, context):
    print('Lambda invoked')
    decoded_event = json.loads(event['body']) 
    return predict_endpoint(decoded_event)


