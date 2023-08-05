# coding=utf-8
import os
from ibm_ai_openscale_cli.utility_classes.fastpath_logger import FastpathLogger
import time
import logging
from retry import retry
from ibm_ai_openscale_cli.enums import ResetType
from ibm_ai_openscale_cli.openscale.openscale import OpenScale

logger = FastpathLogger(__name__)
parent_dir = os.path.dirname(__file__)

DATAMART_MAX_DELETION_ATTEMPTS = 10


class NonExistingDatamartDeleteErrorFilter(logging.Filter):
    def filter(self, record):
        return not record.getMessage().startswith('Failure during delete of data mart')


class OpenScaleReset(OpenScale):

    def __init__(self, args, credentials, database_credentials, ml_engine_credentials):
        super().__init__(args, credentials, database_credentials, ml_engine_credentials)

    def reset(self, reset_type):
        if reset_type is ResetType.METRICS:
            self.reset_metrics()
        elif reset_type is ResetType.MONITORS:
            self.reset_metrics()
            self.reset_monitors()
        # "factory reset" the system
        elif reset_type is ResetType.DATAMART:
            self.delete_datamart()
            self.clean_database()

    @retry(tries=5, delay=4, backoff=2)
    def reset_metrics(self):
        '''
        Clean up the payload logging table, monitoring history tables etc, so that it restores the system
        to a fresh state with datamart configured, model deployments added, all monitors configured,
        but no actual metrics in the system yet. The system is ready to go.
        '''
        if self._database is None:
            logger.log_info('Internal database metrics cannot be reset - skipping')
        else:
            logger.log_info('Deleting datamart metrics ...')
            self._database.reset_metrics_tables(self._datamart_name)
            logger.log_info('Datamart metrics deleted successfully')

    @retry(tries=5, delay=4, backoff=2)
    def reset_monitors(self):
        '''
        Remove all configured monitors and corresponding metrics and history, but leave the actual model deployments
        (if any) in the datamart. User can proceed to configure the monitors via user interface, API, or fastpath.
        '''
        logger.log_info('Deleting datamart monitors ...')
        subscription_uids = self._client.data_mart.subscriptions.get_uids()
        for subscription_uid in subscription_uids:
            try:
                start = time.time()
                subscription = self._client.data_mart.subscriptions.get(subscription_uid)
                elapsed = time.time() - start
                logger.log_timer('data_mart.subscriptions.get in {:.3f} seconds'.format(elapsed))
                start = time.time()
                subscription.explainability.disable()
                elapsed = time.time() - start
                logger.log_timer('subscription.explainability.disable in {:.3f} seconds'.format(elapsed))
                start = time.time()
                subscription.fairness_monitoring.disable()
                elapsed = time.time() - start
                logger.log_timer('subscription.fairness_monitoring.disable in {:.3f} seconds'.format(elapsed))
                start = time.time()
                subscription.performance_monitoring.disable()
                elapsed = time.time() - start
                logger.log_timer('subscription.performance_monitoring.disable in {:.3f} seconds'.format(elapsed))
                start = time.time()
                subscription.payload_logging.disable()
                elapsed = time.time() - start
                logger.log_timer('subscription.payload_logging.disable in {:.3f} seconds'.format(elapsed))
                start = time.time()
                subscription.quality_monitoring.disable()
                elapsed = time.time() - start
                logger.log_timer('subscription.quality_monitoring.disable in {:.3f} seconds'.format(elapsed))
                logger.log_info('Datamart monitors deleted successfully')
            except Exception as e:
                logger.log_warning('Problem during monitor reset: {}'.format(str(e)))
        logger.log_info('Datamart monitors deleted successfully')

        # finally, drop the monitor-related tables
        if self._database is None:
            logger.log_info('Internal database monitor-related tables cannot be deleted - skipping')
        else:
            logger.log_info('Deleting datamart monitor-related tables ...')
            self._database.drop_metrics_tables(self._datamart_name)
            logger.log_info('Datamart monitor-related tables deleted successfully')

    @retry(tries=5, delay=4, backoff=2)
    def delete_datamart(self):
        logger.log_info('Deleting datamart ...')
        attempt = 0
        added_filter = False
        try:
            start = time.time()
            while attempt < DATAMART_MAX_DELETION_ATTEMPTS:  # Wait until exception is thrown to confirm datamart is completely deleted
                if attempt == 1:
                    logger.log_info('Confirming datamart deletion ...')
                elif attempt > 1:
                    logger.log_info('Confirming datamart deletion (attempt {}) ...'.format(attempt))
                self._client.data_mart.delete()
                time.sleep(3)  # wait a few seconds to give time for datamart cleanup
                attempt = attempt + 1
            elapsed = time.time() - start
            logger.log_timer('data_mart.delete in {:.3f} seconds'.format(elapsed))
            logger.log_info('Datamart deleted successfully')
        except Exception as e:
            ignore_exceptions = ['AIQCS0005W', 'AIQC50005W', 'AISCS0005W']  # datamart does not exist, so cannot delete
            if any(word in str(e) for word in ignore_exceptions):
                added_filter = True
                logger.logger.addFilter(NonExistingDatamartDeleteErrorFilter())
                if attempt == 0:
                    logger.log_exception(str(e))
                    logger.log_info('Datamart not present, nothing to delete')
                else:
                    logger.log_info('Confirmed datamart deletion')
            else:
                raise e
        if added_filter:
            logger.logger.removeFilter(NonExistingDatamartDeleteErrorFilter())

    @retry(tries=5, delay=4, backoff=2)
    def clean_database(self):
        if self._database is None:
            logger.log_info('Internal database instance cannot be deleted - skipping')
        else:
            logger.log_info('Cleaning database ...')
            self._database.drop_existing_schema(self._datamart_name, self._keep_schema)
            logger.log_info('Database cleaned successfully')
