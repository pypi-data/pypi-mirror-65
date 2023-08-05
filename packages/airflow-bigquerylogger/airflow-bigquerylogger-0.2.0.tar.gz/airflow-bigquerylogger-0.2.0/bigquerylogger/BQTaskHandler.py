import os
from datetime import datetime
from cached_property import cached_property

from airflow.configuration import conf
from airflow.utils.log.logging_mixin import LoggingMixin
from airflow.utils.log.gcs_task_handler import GCSTaskHandler


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

        self.dataset_name = dataset_name
        self.query_limit = query_limit

        self.where_statement = ""

        self.closed = False

    @cached_property
    def bq_cursor(self):
        remote_conn_id = conf.get('core', 'REMOTE_LOG_CONN_ID')
        try:
            from airflow.contrib.hooks.bigquery_hook import BigQueryHook

            return BigQueryHook(
                bigquery_conn_id = remote_conn_id,
                use_legacy_sql = False).get_conn().cursor()
        except Exception as e:
            self.log.error(
                'Could not create a BigQueryHook with connection id '
                '"%s". %s\n\nPlease make sure that the BigQuery '
                'connection exists.', remote_conn_id, str(e))

    def set_context(self, ti):
        super(BQTaskHandler, self).set_context(ti)

        self.where_statement = """
            labels.k8s_pod_dag_id = '%s' AND
            labels.k8s_pod_task_id = '%s' AND
            labels.k8s_pod_execution_date = '%s' AND
            labels.k8s_pod_try_number = '%d'
            """ % (ti.dag_id, ti.task_id, ti.execution_date.isoformat(), ti.try_number)

    def close(self):
        if self.closed:
            return

        super(BQTaskHandler, self).close()

        self.log.info("""*** Unable to delete logs from BigQuery {} because:\n\n
                         *** Rows that were written to a table recently via streaming
                         (using the tabledata.insertall method) cannot be modified using
                         UPDATE, DELETE, or MERGE statements.
                         I recommend setting up a table retention!\n""".format(self.dataset_name))

        self.closed = True

    def _bq_read(self, metadata=None):
        if not metadata:
            metadata = {'offset': 0}

        if 'offset' not in metadata:
            metadata['offset'] = 0

        log = self._bq_query(metadata['offset'])
        log_count = len(log)

        metadata['end_of_log'] = (log_count == 0)
        metadata['offset'] += log_count

        return "".join(log), metadata

    def _bq_query(self, offset):
        """
        Returns the log found in Big Query.

        :param offset: the query offset
        :type offset: int
        """
        query = """
                SELECT timestamp, textPayload
                FROM `%s.std*`
                WHERE %s
                ORDER BY timestamp ASC
                OFFSET %d
                """

        if (self.query_limit > 0):
            query += 'LIMIT %d' % self.query_limit

        self.bq_cursor.execute(query, (self.dataset_name,
                                       self.where_statement,
                                       offset))

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
