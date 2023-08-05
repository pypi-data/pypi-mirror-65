import os
from datetime import datetime
from cached_property import cached_property

from airflow.configuration import conf
from airflow.utils.log.logging_mixin import LoggingMixin
from airflow.utils.log.gcs_task_handler import GCSTaskHandler
from airflow.contrib.executors.kubernetes_executor import AirflowKubernetesScheduler


class BQTaskHandler(GCSTaskHandler, LoggingMixin):
    """
    BQTaskHandler is a python log handler that handles and reads
    task instance logs. It extends airflow GCSTaskHandler and
    reads from Big Query if the log file is not yet available
    in Google storage.
    """
    def __init__(self, base_log_folder, gcs_log_folder, filename_template,
                 dataset_name, query_limit):
        super(BQTaskHandler, self).__init__(base_log_folder, gcs_log_folder, filename_template)
        self._bq_cursor = None

        self.dataset = dataset_name

        self.parameters = {
            'limit': int(query_limit)
        }

    @cached_property
    def bq_cursor(self):
        remote_conn_id = conf.get('core', 'REMOTE_LOG_CONN_ID')
        try:
            from airflow.contrib.hooks.bigquery_hook import BigQueryHook

            return BigQueryHook(
                bigquery_conn_id = remote_conn_id,
                use_legacy_sql = False
            ).get_conn().cursor()
        except Exception as e:
            self.log.error(
                'Could not create a BigQueryHook with connection id '
                '"%s". %s\n\nPlease make sure that the BigQuery '
                'connection exists.', remote_conn_id, str(e))

    def set_context(self, ti):
        super(BQTaskHandler, self).set_context(ti)
        self._set_parameters(ti)

    def _set_parameters(self, ti, try_number):
        self.parameters['dag_id'] = ti.dag_id
        self.parameters['task_id'] = ti.task_id
        self.parameters['try_number'] = str(try_number if try_number else ti.try_number)
        self.parameters['execution_date'] = AirflowKubernetesScheduler._datetime_to_label_safe_datestring(ti.execution_date)

    def _bq_read(self, metadata=None):
        if not metadata:
            metadata = {'offset': 0}

        if 'offset' not in metadata:
            metadata['offset'] = 0

        try:
            log = self._bq_query(metadata['offset'])
            log_count = len(log)
            log = "".join(log)
        except Exception as e:
            log = '*** Unable to read remote log on BigQuery from {}\n*** {}\n\n'.format(
                self.dataset, str(e))
            self.log.error(log)
            log_count = 0

        metadata['end_of_log'] = (log_count == 0)
        metadata['offset'] += log_count

        return log, metadata

    def _bq_query(self, offset):
        """
        Returns the log found in Big Query.

        :param offset: the query offset
        :type offset: int
        """

        query = """
                SELECT timestamp, textPayload
                FROM `%s.std*`
                """ % self.dataset

        query += """
                WHERE
                    labels.k8s_pod_dag_id = %(dag_id)s AND
                    labels.k8s_pod_task_id = %(task_id)s AND
                    labels.k8s_pod_execution_date = %(execution_date)s AND
                    labels.k8s_pod_try_number = %(try_number)s
                ORDER BY timestamp ASC
                """

        if (self.parameters['limit'] > 0):
            query += """
                    LIMIT %(limit)d
                    OFFSET %(offset)d
                    """

            self.parameters['offset'] = int(offset)

        self.bq_cursor.execute(query, self.parameters)

        return self.format_log(self.bq_cursor.fetchall())

    def _read(self, ti, try_number, metadata=None):
        """
        Read logs of given task instance and try_number from BigQuery
        if the log file is not yet available in Google storage.

        :param ti: task instance object
        :param try_number: task instance try_number to read logs from
        :param metadata: log metadata,
                         can be used for steaming log reading and auto-tailing.
        """

        # Explicitly set query parameters is necessary as the given
        # task instance might be different than task instance passed in
        # in set_context method.
        self._set_parameters(ti, try_number)

        log_relative_path = self._render_filename(ti, try_number)
        remote_loc = os.path.join(self.remote_base, log_relative_path)

        try:
            remote_log = super(BQTaskHandler, self).gcs_read(remote_loc)
            log = '*** Reading remote log from {}.\n{}\n'.format(
                   remote_loc, remote_log)
            return log, {'end_of_log': True}
        except Exception as e:
            error = '*** Unable to read remote log from {}\n*** {}\n\n'.format(
                     remote_loc, str(e))
            self.log.error(error)

            log, metadata = self._bq_read(metadata)

            return (error + log) if metadata['offset'] == 0 else log, metadata

    @staticmethod
    def format_log(log):
        return ['[{}] {}'.format(
            datetime.fromtimestamp(item[0]).strftime("%m/%d/%Y, %H:%M:%S,%f"), item[1]
        ) for item in log]
