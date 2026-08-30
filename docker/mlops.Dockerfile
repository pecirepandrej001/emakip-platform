FROM python:3.12-slim
RUN pip install --no-cache-dir "mlflow>=3.2,<4" "psycopg2-binary>=2.9,<3"
WORKDIR /mlflow
CMD ["mlflow", "server", "--host", "0.0.0.0", "--port", "5000", "--backend-store-uri", "sqlite:///mlflow.db", "--default-artifact-root", "/mlflow/artifacts"]
