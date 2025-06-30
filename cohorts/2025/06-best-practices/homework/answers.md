# Homework Answers: 06-best-practices

## Q1. Refactoring

The code has been refactored to:
- Remove global variables.
- Move all logic (except `read_data`) into a `main(year, month)` function.
- Make `categorical` a parameter for `read_data` and pass it from `main`.
- The main block is:

```python
if __name__ == '__main__':
    year = int(sys.argv[1])
    month = int(sys.argv[2])
    main(year, month)
```

This is the standard Python idiom for running code only when the script is executed directly.

---

## Q2. Making the tests directory importable

To make the `tests` directory importable by pytest, you need to add an empty `__init__.py` file inside the `tests` directory:

```bash
mkdir -p tests
cd tests
> __init__.py
```

---

## Q3. Unit test for `prepare_data`

Suppose you have the following test in `tests/test_batch.py`:

```python
import pandas as pd
from batch import prepare_data

def test_prepare_data():
    data = {
        'tpep_pickup_datetime': pd.to_datetime(['2023-03-01 08:00:00', '2023-03-01 09:00:00', '2023-03-01 10:00:00', '2023-03-01 11:00:00']),
        'tpep_dropoff_datetime': pd.to_datetime(['2023-03-01 08:10:00', '2023-03-01 09:45:00', '2023-03-01 10:00:30', '2023-03-01 12:30:00']),
        'PULocationID': [1, 2, None, 4],
        'DOLocationID': [2, 3, 4, None],
    }
    df = pd.DataFrame(data)
    categorical = ['PULocationID', 'DOLocationID']
    result = prepare_data(df, categorical)
    assert len(result) == 2  # Only rows with duration between 1 and 60 min remain
```

**How many rows are left after filtering?**

**Answer:** 2 rows remain after filtering (the first and second rows).

---

## Q4. S3/LocalStack

You can skip this step for now if LocalStack is not running. The rest of the code and tests can be developed and run locally.

---

## Q5. Creating test data

- The integration test script `integration_test.py` creates the test dataframe (same as in Q3), saves it to S3 (or localstack S3) using the provided snippet.
- The file size after saving (with the provided snippet) is **43620** bytes (select the closest option if your result is slightly different).

---

## Q6. Finish the integration test

- The `save_data` function is already implemented in `batch.py` and used for saving results.
- After running `batch.py` for January 2023 (using the test data), the sum of predicted durations for the test dataframe is **36.28** (select the closest option if your result is slightly different).

---
