# MLOps Zoomcamp final project: Renewable potential in South-east France

The goal of this project is to apply everything I learned in this course and build an end-to-end machine learning project.

## Data Science part:

### Problem Statement:

I chose to use the [MeteoNet](https://meteonet.umr-cnrm.fr/) dataset to predict renewable energy potential in south-east of France.
By feeding the GPS coordinates, the model will give us the potential wind energy production of a wind turbine at this location.



I created a dataset for my model, it comes from the wind speed recording of 222 stations across south east France.
The data used for the models can be found [here](https://meteonet.umr-cnrm.fr/dataset/data/SE/ground_stations/).
I post processed the data by computing the average wind speed to the power of 3 to have an estimate of the wind power at the location of all stations.

The model used here is very basic and might not be relevant because the purpose of this project is to use ML-OPS practices and is not focused on the performance and relevancy of a model.

and try to predict whether or not a client is going to churn or not in this quarter based on several parameters on the client themselves, as well as their consumption figures.

To assess the performance of the model, I'll be using an the RMSE which is a classic metric for regression.


### Model Used:

I'll be using an XGBoost Regressor whose hyperparameters I'll get using Hyperoptimization.

## Cleaning Data and uploading it:

I put the postprocessed csv from Meteonet in the `data` folder in the parent directory. The data can be visualized using the notebook `data_viz.ipynb`. It also creates the train and test dataset.

## Training the model with experiment tracking and orchestration:

To train the model, I go through 3 steps:

1. Read the data
2. Run a Hyperoptimzer for XGBoost hyperparameters, store results and models in the `hpo-xgboost-wind` experiment
3. Automatically the best model in the parent directory

Both experiment tracking and model registry are used and the workflow is fully deployed in Prefect.



## Deploying the model:

The model is accessible via an API hosted in AWS thanks to Lambda and API Gateway.
A specific container has been created to be compatible with Lambda function. The lambda function is linked to API gateway and the model can be used using a POST method on the following adress: https://61bmqgucoe.execute-api.eu-west-3.amazonaws.com/postLocation

The json fed into the POST method shall be the GPS coordinates of the location where the available wind power shall be computed:

```
location = {
    "lat": 43.8,
    "lon": 6.1,
}
```

The API will return the wind potential of the location specified and the GPS coordinates such as below:
```
{'wind potential': 87.01605987548828,
 'lat': 43.8,
 'lon': 6.1
 }
```


## Monitoring:

For monitoring, a simple script in the monitoring folder is used.
To run the monitoring for year XXXX, type in the terminal:
```
python run_monitoring XXXX
```
It will ouput the RMSE the deployed model on the test stations and the RMSE of XXXX year on the test stations and the new stations.
If the two values are judged two far from each other, an action will have to be done to retrain the model on larger data or investigate why the model performance changed.

The model monitoring can be long because a 3GB file is converted into a dataset to be fed into the monitoring script.


## Reproducibility:

To reproduce, you shall follow the following steps:

1. Create a virtual envionement and install the dependencies listed in *requirements.txt*

2. Download the data of meteonet by calling the *Makefile*:
    ```
    make download_raw
    ```
    It will download the raw data in the *raw_data_meteonet* folder


3. Generate the dataset by running the python script
    ```
    python generate_dataset.py
    ```

4. Train the models and save the best one by running the python script
    ```
    python train_model.py
    ```

5. Create the lambda containder and pushing it to ECR:
    ```
    make publish_ecr
    ```

## Good practices

1. Unit tests are included in the folder tests/ and can be run by:
    ```
    make test
    ```

2. Pre commit hooks for formatting are used

3. Makefil is used for easier reproducibility
