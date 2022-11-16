import mlflow
from mlflow.tracking import MlflowClient
import xgboost as xgb
import pandas as pd

from hyperopt import fmin, tpe, hp, STATUS_OK, Trials
from hyperopt.pyll import scope

from sklearn.metrics import mean_squared_error

from mlflow.entities import ViewType

import pickle


from prefect import task, flow, get_run_logger

@task
def get_data(path_train = "data/train.csv", path_test = "data/test.csv"):
    """Getting train and test data"""
    df_train = pd.read_csv(path_train)
    df_test = pd.read_csv(path_test)

    X_train = df_train[['lon', 'lat']]
    X_test = df_test[['lon', 'lat']]

    y_train = df_train['mean_power']
    y_test = df_test['mean_power']
    
    
    return X_train, y_train, X_test, y_test

@task
def run_opt_xgboost(X_train, y_train, X_test, y_test):
    """Training the model"""
    logger = get_run_logger()
    train = xgb.DMatrix(X_train, label=y_train)
    test = xgb.DMatrix(X_test, label=y_test)

    mlflow.xgboost.autolog()

    def objective(params):
        
        with mlflow.start_run():    
            mlflow.set_tag("model", "xgboost")
            mlflow.log_params(params)
            booster = xgb.train(
                params=params,
                dtrain=train,
                num_boost_round=1000,
                evals=[(test, 'validation')],
                early_stopping_rounds=50
            )
            y_pred = booster.predict(test)
            rmse = mean_squared_error(y_test, y_pred, squared=False)
            mlflow.log_metric("rmse", rmse)
            logger.info(f"The MSE of training is: {rmse}")

        return {'loss': rmse, 'status': STATUS_OK}

    search_space = {
        'max_depth': scope.int(hp.quniform('max_depth', 4, 100, 1)),
        'learning_rate': hp.loguniform('learning_rate', -3, 0),
        'reg_alpha': hp.loguniform('reg_alpha', -5, -1),
        'reg_lambda': hp.loguniform('reg_lambda', -6, -1),
        'min_child_weight': hp.loguniform('min_child_weight', -1, 3),
        'objective': 'reg:linear',
        'seed': 42
    }

    best_result = fmin(
        fn=objective,
        space=search_space,
        algo=tpe.suggest,
        max_evals=3,
        trials=Trials()
    )
    
def save_best_model():
    runs = client.search_runs(
    experiment_ids=exp_id   ,
    #filter_string="metrics.rmse < 7",
    run_view_type=ViewType.ACTIVE_ONLY,
    max_results=5,
    order_by=["metrics.rmse ASC"]
    )

    best_run_id = runs[0].info.run_id


    logged_model = f'runs:/{best_run_id}/model' # Model UUID from the MLflow Artifact page for the run

    xgboost_model = mlflow.xgboost.load_model(logged_model)

    file_name = "xgb_reg.pkl"
    
    # save
    pickle.dump(xgboost_model, open(file_name, "wb"))

@flow
def main():
    X_train, y_train, X_test, y_test = get_data()
    run_opt_xgboost(X_train, y_train, X_test, y_test)
    save_best_model()
    
    

    
if __name__ == '__main__':
    MLFLOW_TRACKING_URI = "sqlite:///mlflow.db"
    EXPERIMENT_NAME = "hpo-xgboost-wind"

    client = MlflowClient(tracking_uri=MLFLOW_TRACKING_URI)
    exisiting_exp = [exp.name for exp in client.search_experiments()]
    
    if EXPERIMENT_NAME not in exisiting_exp:
        client.create_experiment(name=EXPERIMENT_NAME)

    mlflow.set_tracking_uri(MLFLOW_TRACKING_URI)
    mlflow.set_experiment(EXPERIMENT_NAME)

    exp_id = mlflow.set_experiment(EXPERIMENT_NAME).experiment_id

    main()
    
    
    
    
    
