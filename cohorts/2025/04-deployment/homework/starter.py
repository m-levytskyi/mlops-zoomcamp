#!/usr/bin/env python
# coding: utf-8
import pickle
import pandas as pd
import sys


# Parse command line arguments
if len(sys.argv) != 3:
    print('Usage: python starter.py <year> <month>')
    sys.exit(1)

year = int(sys.argv[1])
month = int(sys.argv[2])


# Load the model
with open('model.bin', 'rb') as f_in:
    dv, model = pickle.load(f_in)


categorical = ['PULocationID', 'DOLocationID']

def read_data(filename):
    df = pd.read_parquet(filename)

    df['duration'] = df.tpep_dropoff_datetime - df.tpep_pickup_datetime
    df['duration'] = df.duration.dt.total_seconds() / 60

    df = df[(df.duration >= 1) & (df.duration <= 60)].copy()

    df[categorical] = df[categorical].fillna(-1).astype('int').astype('str')

    return df


# Construct the URL using the provided year and month
url = f'https://d37ci6vzurychx.cloudfront.net/trip-data/yellow_tripdata_{year:04d}-{month:02d}.parquet'
df = read_data(url)


# Make predictions
dicts = df[categorical].to_dict(orient='records')
X_val = dv.transform(dicts)
y_pred = model.predict(X_val)

# Print the mean predicted duration
mean_duration = y_pred.mean()
print(f'Mean predicted duration: {mean_duration:.2f} minutes')


# Create ride IDs and save results
df['ride_id'] = f'{year:04d}/{month:02d}_' + df.index.astype('str')

df_result = pd.DataFrame()
df_result['ride_id'] = df['ride_id']
df_result['prediction'] = y_pred

output_file = f'yellow_tripdata_{year:04d}-{month:02d}_predictions.parquet'

df_result.to_parquet(
    output_file,
    engine='pyarrow',
    compression=None,
    index=False
)

