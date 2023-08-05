import os

from airflow.configuration import conf
from airflow.config_templates.airflow_local_settings import DEFAULT_LOGGING_CONFIG as LOGGING_CLASS


if LOGGING_CLASS['handlers']['task']['class'] != 'bigquerylogger.BQTaskHandler':

    remote_logging = conf.getboolean('core', 'remote_logging')
    remote_base_log_folder = conf.get('core', 'REMOTE_BASE_LOG_FOLDER')

    if remote_logging and remote_base_log_folder.startswith('gs://'):

        base_log_folder = conf.get('core', 'BASE_LOG_FOLDER')
        filename_template = conf.get('core', 'LOG_FILENAME_TEMPLATE')
        bigquery_dataset = conf.get('core', 'LOG_BIGQUERY_DATASET')
        bigquery_limit = conf.get('core', 'LOG_BIGQUERY_LIMIT', fallback=0)

        bigquery_remote_handlers = {
            'task': {
                'class': 'bigquerylogger.BQTaskHandler.BQTaskHandler',
                'formatter': 'airflow',
                'base_log_folder': os.path.expanduser(base_log_folder),
                'gcs_log_folder': remote_base_log_folder,
                'filename_template': filename_template,
                'dataset_name': bigquery_dataset,
                'query_limit': bigquery_limit
            }
        }

        LOGGING_CLASS['handlers'].update(bigquery_remote_handlers)

