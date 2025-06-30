import pytest
import pandas as pd
from datetime import datetime
from batch import prepare_data


def dt(hour, minute, second=0):
    return datetime(2023, 1, 1, hour, minute, second)


def test_prepare_data():
    data = [
        (None, None, dt(1, 1), dt(1, 10)),
        (1, 1, dt(1, 2), dt(1, 10)),
        (1, None, dt(1, 2, 0), dt(1, 2, 59)),
        (3, 4, dt(1, 2, 0), dt(2, 2, 1)),      
    ]

    columns = ['PULocationID', 'DOLocationID', 'tpep_pickup_datetime', 'tpep_dropoff_datetime']
    df = pd.DataFrame(data, columns=columns)
    
    categorical = ['PULocationID', 'DOLocationID']
    result_df = prepare_data(df, categorical)
    
    # Expected values:
    # Row 0: (None, None, dt(1, 1), dt(1, 10)) -> duration = 9 min (valid)
    # Row 1: (1, 1, dt(1, 2), dt(1, 10)) -> duration = 8 min (valid)
    # Row 2: (1, None, dt(1, 2, 0), dt(1, 2, 59)) -> duration = 59/60 = 0.98 min (invalid, < 1)
    # Row 3: (3, 4, dt(1, 2, 0), dt(2, 2, 1)) -> duration = 1440 + 1/60 = 1440.017 min (invalid, > 60)
    
    # Only rows 0 and 1 should remain
    expected_length = 2
    assert len(result_df) == expected_length
    
    # Check that categorical columns are converted to strings
    assert result_df['PULocationID'].dtype == 'object'
    assert result_df['DOLocationID'].dtype == 'object'
    
    # Check that None values are replaced with '-1'
    assert result_df.iloc[0]['PULocationID'] == '-1'
    assert result_df.iloc[0]['DOLocationID'] == '-1'
    
    # Check duration calculations
    assert abs(result_df.iloc[0]['duration'] - 9.0) < 0.01
    assert abs(result_df.iloc[1]['duration'] - 8.0) < 0.01
