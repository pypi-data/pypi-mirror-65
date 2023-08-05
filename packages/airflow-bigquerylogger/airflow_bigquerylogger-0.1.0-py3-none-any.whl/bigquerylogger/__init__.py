import os

from airflow.configuration import conf
from airflow.utils.module_loading import import_string


def get_default_logging_config():
    logging_class_path = 'airflow.config_templates.' \
                         'airflow_local_settings.DEFAULT_LOGGING_CONFIG'
    return import_string(logging_class_path)


def set_bigquery_handler(default_logging_config):
    remote_logging = conf.getboolean('core', 'remote_logging')
    remote_base_log_folder = conf.get('core', 'REMOTE_BASE_LOG_FOLDER')

    if not (
        remote_logging and remote_base_log_folder.startswith('gs://')
    ): return default_logging_config

    base_log_folder = conf.get('core', 'BASE_LOG_FOLDER')
    filename_template = conf.get('core', 'LOG_FILENAME_TEMPLATE')
    bigquery_dataset = conf.get('core', 'LOG_BIGQUERY_DATASET')
    bigquery_limit = conf.get('core', 'LOG_BIGQUERY_LIMIT', fallback=0)

    bigquery_remote_handlers = {
        'task': {
            'class': 'bigquerylogger.BQTaskHandler',
            'formatter': 'airflow',
            'base_log_folder': os.path.expanduser(base_log_folder),
            'gcs_log_folder': remote_base_log_folder,
            'filename_template': filename_template,
            'dataset_name': bigquery_dataset,
            'query_limit': bigquery_limit
        }
    }

    default_logging_config['handlers'].update(bigquery_remote_handlers)

    return default_logging_config


default_logging_config = get_default_logging_config()

CONFIG_CLASS=set_bigquery_handler(default_logging_config)
