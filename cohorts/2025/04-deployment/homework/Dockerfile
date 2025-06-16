FROM agrigorev/zoomcamp-model:mlops-2024-3.10.13-slim

RUN pip install -U pip

RUN pip install scikit-learn==1.6.1 pandas pyarrow

COPY starter.py .

ENTRYPOINT ["python", "starter.py"]