# BigQuery logger handler for Airflow

## Installation

`pip install airflow-bigquerylogger`

## Configuration

```bash
AIRFLOW__CORE__REMOTE_LOGGING='true'
AIRFLOW__CORE__REMOTE_BASE_LOG_FOLDER='gs://bucket/path'
AIRFLOW__CORE__REMOTE_LOG_CONN_ID='gcs_log'
AIRFLOW__CORE__LOGGING_CONFIG_CLASS='bigquerylogger.config.LOGGING_CLASS'
AIRFLOW__CORE__LOG_BIGQUERY_DATASET='dataset.table'
AIRFLOW__CORE__LOG_BIGQUERY_LIMIT=50
```

## Credits

Thanks to https://medium.com/bluecore-engineering/kubernetes-pod-logging-in-the-airflow-ui-ed9ca6f37e9d


Unable to delete logs from BigQuery {} because:\n\n
                         *** Rows that were written to a table recently via streaming
                         (using the tabledata.insertall method) cannot be modified using
                         UPDATE, DELETE, or MERGE statements.
                         I recommend setting up a table retention!