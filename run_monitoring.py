import pickle
import pandas as pd
import sys


from sklearn.metrics import mean_squared_error

from generate_dataset import  process_data
from train_model import get_data

import xgboost as xgb




def load_model():
    
    with open('./xgb_reg.pkl', 'rb') as f_in:
            model = pickle.load(f_in)
            
    return model
    

    


if __name__ == "__main__":
    year = sys.argv[1]
 
 
    PATH_TRAIN = "data/train.csv"
    
    FILENAME = f"raw_data_meteonet/SE{year}.csv"    
    CHUNKSIZE = 10 ** 6
    
    df_moni = pd.DataFrame()
    
    for chunk in pd.read_csv(FILENAME, chunksize=CHUNKSIZE):
        df_moni = process_data(df_moni, chunk)
     

    
    model = load_model()
    X_train, y_train, X_test, y_test = get_data.fn()
    
    test = xgb.DMatrix(X_test, label=y_test)
    y_pred = model.predict(test)
    rmse_test = mean_squared_error(y_test, y_pred, squared=False)
        

    
    ### We selec only the coordinates that are not the same than in the train dataset
    df_train = pd.read_csv(PATH_TRAIN)
    
    df_moni = df_moni.drop(df_train["number_sta"])
    
    df_moni.dropna(inplace = True)
    
    ## we keep the values of windpower below 500 to avoid extreme data
    
    df_moni = df_moni[df_moni['mean_power']<500]
    
    X_moni = df_moni[['lon', 'lat']]
    y_moni = df_moni['mean_power']
    
    moni = xgb.DMatrix(X_moni, label=y_moni)
    y_pred_moni = model.predict(moni)
    rmse_moni = mean_squared_error(y_moni, y_pred_moni, squared=False)
        
    
    print("On the initial test period, the RMSE was: ", rmse_test)
    print("On the monitored period, the RMSE is: ", rmse_moni)
   
    
