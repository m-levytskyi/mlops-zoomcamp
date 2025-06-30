import os
import pandas as pd
from batch import prepare_data, save_data

def dt(hour, minute, second=0):
    from datetime import datetime
    return datetime(2023, 1, 1, hour, minute, second)

def create_test_data():
    data = [
        (None, None, dt(1, 1), dt(1, 10)),
        (1, 1, dt(1, 2), dt(1, 10)),
        (1, None, dt(1, 2, 0), dt(1, 2, 59)),
        (3, 4, dt(1, 2, 0), dt(2, 2, 1)),      
    ]
    columns = ['PULocationID', 'DOLocationID', 'tpep_pickup_datetime', 'tpep_dropoff_datetime']
    df = pd.DataFrame(data, columns=columns)
    categorical = ['PULocationID', 'DOLocationID']
    df_input = prepare_data(df, categorical)
    return df_input

def save_test_data_to_s3(df_input, input_file, options):
    df_input.to_parquet(
        input_file,
        engine='pyarrow',
        compression=None,
        index=False,
        storage_options=options
    )

if __name__ == "__main__":
    # Set up environment variables for test
    year = 2023
    month = 1
    input_file = os.getenv('INPUT_FILE', f's3://nyc-duration/in/{year:04d}-{month:02d}.parquet')
    S3_ENDPOINT_URL = os.getenv('S3_ENDPOINT_URL', 'http://localhost:4566')
    options = {
        'client_kwargs': {
            'endpoint_url': S3_ENDPOINT_URL
        }
    }
    df_input = create_test_data()
    save_test_data_to_s3(df_input, input_file, options)
    print(f"Test data saved to {input_file}")
