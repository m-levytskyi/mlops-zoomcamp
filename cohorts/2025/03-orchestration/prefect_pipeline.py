import pandas as pd
import mlflow
import mlflow.sklearn

from prefect import flow, task

from sklearn.feature_extraction import DictVectorizer
from sklearn.linear_model import LinearRegression
from sklearn.metrics import root_mean_squared_error
import pickle


@task
def read_dataframe(filename):
    df = pd.read_parquet(filename)

    df['duration'] = df.tpep_dropoff_datetime - df.tpep_pickup_datetime
    df.duration = df.duration.dt.total_seconds() / 60

    df = df[(df.duration >= 1) & (df.duration <= 60)]

    categorical = ['PULocationID', 'DOLocationID']
    df[categorical] = df[categorical].astype(str)

    print(f"Read {len(df)} rows from {filename}")
    return df


@task
def preprocess(df):
    categorical = ['PULocationID', 'DOLocationID']
    train_dicts = df[categorical].to_dict(orient='records')

    dv = DictVectorizer()
    X = dv.fit_transform(train_dicts)
    y = df['duration'].values

    return X, y, dv


@task
def train_model(X, y):
    lr = LinearRegression()
    lr.fit(X, y)
    print(f"Trained Linear Regression model with {X.shape[0]} samples")
    print(f"Model intercept: {lr.intercept_:.2f}")
    return lr


@task
def evaluate_and_log(X, y, dv, model):
    y_pred = model.predict(X)
    rmse = root_mean_squared_error(y, y_pred)

    mlflow.set_tracking_uri("file:./mlruns")
    mlflow.set_experiment("prefect-nyc-taxi")

    with mlflow.start_run():
        mlflow.log_metric("rmse", rmse)
        mlflow.sklearn.log_model(model, "model")
        # Save DictVectorizer too
        with open("dv.pkl", "wb") as f_out:
            pickle.dump(dv, f_out)
        mlflow.log_artifact("dv.pkl")

    print(f"RMSE: {rmse:.2f}")
    return rmse


@flow(name="NYC Taxi Linear Regression Pipeline")
def main(filename: str):
    df = read_dataframe(filename)
    X, y, dv = preprocess(df)
    model = train_model(X, y)
    rmse = evaluate_and_log(X, y, dv, model)


if __name__ == "__main__":
    # Replace with your actual file path
    main("yellow_tripdata_2023-03.parquet")
