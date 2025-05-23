import os
import pickle
import click

from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error

import mlflow

def load_pickle(filename: str):
    with open(filename, "rb") as f_in:
        return pickle.load(f_in)


@click.command()
@click.option(
    "--data_path",
    default="./output",
    help="Location where the processed NYC taxi trip data was saved"
)
def run_train(data_path: str):
    # Set or create experiment by name instead of ID
    mlflow.set_experiment("taxi-experiment")
    
    # Enable autologging
    mlflow.autolog()
    
    print(f"MLflow tracking URI: {mlflow.get_tracking_uri()}")
    print(f"Current experiment: {mlflow.get_experiment(mlflow.active_run().info.experiment_id) if mlflow.active_run() else 'None'}")
    
    with mlflow.start_run():
        print("MLflow run started")  # Debug print
        
        X_train, y_train = load_pickle(os.path.join(data_path, "train.pkl"))
        X_val, y_val = load_pickle(os.path.join(data_path, "val.pkl"))

        rf = RandomForestRegressor(max_depth=10, random_state=0)
        rf.fit(X_train, y_train)
        y_pred = rf.predict(X_val)

        mse = mean_squared_error(y_val, y_pred)
        rmse = mse ** 0.5
        mlflow.log_metric("rmse", rmse)
        
        print(f"RMSE: {rmse}")  # Debug print
        print("MLflow run completed")  # Debug print


if __name__ == '__main__':
    run_train()
