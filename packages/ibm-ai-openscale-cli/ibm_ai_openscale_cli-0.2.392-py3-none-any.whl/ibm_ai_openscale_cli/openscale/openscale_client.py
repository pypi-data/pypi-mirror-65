# coding=utf-8
from ibm_ai_openscale_cli.utility_classes.fastpath_logger import FastpathLogger
import os
import requests
import time
from datetime import datetime, timedelta
import uuid
from retry import retry
import random
import json
from ibm_ai_openscale_cli.enums import MLEngineType
from ibm_ai_openscale import WatsonMachineLearningInstance4ICP
from ibm_ai_openscale.engines import AzureMachineLearningStudioInstance, AzureMachineLearningStudioAsset
from ibm_ai_openscale.engines import AzureMachineLearningServiceInstance, AzureMachineLearningServiceAsset
from ibm_ai_openscale.engines import CustomMachineLearningInstance, CustomMachineLearningAsset
from ibm_ai_openscale.engines import SageMakerMachineLearningInstance, SageMakerMachineLearningAsset
from ibm_ai_openscale.engines import SPSSMachineLearningInstance, SPSSMachineLearningAsset
from ibm_ai_openscale.engines import WatsonMachineLearningInstance, WatsonMachineLearningAsset
from ibm_ai_openscale.supporting_classes import Feature, InputDataType, ProblemType, FeedbackFormat, PayloadRecord
from ibm_ai_openscale_cli import logging_temp_file, name as cli_name
from ibm_ai_openscale_cli.api_environment import ApiEnvironment
from ibm_ai_openscale_cli.openscale.openscale_reset import OpenScaleReset
from ibm_ai_openscale_cli.utility_classes.utils import get_iam_headers, remove_port_from_url, update_url, get_url_elements

logger = FastpathLogger(__name__)
parent_dir = os.path.dirname(__file__)

class OpenScaleClient(OpenScaleReset):

    def __init__(self, args, credentials, database_credentials, ml_engine_credentials):
        super().__init__(args, credentials, database_credentials, ml_engine_credentials)
        self.is_mrm_challenger = False
        self.is_mrm_preprod = False
        self.is_mrm_prod = False
        self.mrm_preprod_subscription_id = None
        self.mrm_challenger_instance_id = None
        self.mrm_preprod_instance_id = None
        self.mrm_prod_instance_id = None
        self._binding_id = None
        self._binding_id_mrm_preprod = None
        self.metric_check_errors = [['model-name', 'metric', 'status']]
        self.set_iam_headers()

    def set_model(self, model):
        self._model = model
        self._subscription = None
        self._asset_details_dict = None
        self._fairness_run_once = True
        self._explainability_run_once = True
        self._use_bkpi = False
        self._configure_explain = True

    def get_deployment_id(self):
        return self._asset_details_dict['source_entry_metadata_guid']

    def get_asset_id(self):
        return self._asset_details_dict['source_uid']

    def get_binding_id(self):
        if self.is_mrm_challenger or self.is_mrm_preprod:
            return self._binding_id_mrm_preprod
        return self._binding_id

    def get_subscription_id(self):
        return self._subscription.uid

    def is_unstructured_text(self):
        return self._model.is_unstructured_text

    def is_unstructured_image(self):
        return self._model.is_unstructured_image

    def get_datamart_details(self):
        return self._client.data_mart.get_details()

    def set_iam_headers(self):
        token = self._args.iam_token if self._args.iam_token else None
        self.iam_headers = get_iam_headers(self._credentials, self._args.env_dict, token)

    def create_datamart(self):
        '''
        Create datamart schema and datamart
        '''
        logger.log_info('Creating datamart {} ...'.format(self._datamart_name))

        if self._database is None:
            logger.log_info('PostgreSQL instance: internal')
        else:
            self._reliable_create_schema()
        self._reliable_create_datamart()
        logger.log_info('Datamart {} created successfully'.format(self._datamart_name))

    @retry(tries=3, delay=5, backoff=2)
    def _reliable_create_schema(self):
        self._database.create_new_schema(self._datamart_name, self._keep_schema)

    @retry(tries=5, delay=4, backoff=2)
    def _reliable_create_datamart(self):
        start = time.time()
        if self._database is None:
            self._client.data_mart.setup(internal_db=True)
        else:
            self._client.data_mart.setup(db_credentials=self._database_credentials, schema=self._datamart_name)
        elapsed = time.time() - start
        self.timer('data_mart.setup', elapsed)

    @retry(tries=5, delay=4, backoff=2)
    def _reliable_bind_mlinstance(self, binding_name, credentials, ml_engine=None, is_mrm_preprod=False):
        if self._args.ml_engine_type is MLEngineType.WML:
            if self._args.is_icp:
                if 'apikey' in credentials:
                    ml_instance = WatsonMachineLearningInstance(credentials)
                    binding_name = 'IBM Cloud {}'.format(binding_name)
                else:
                    if self._args.wml or self._args.wml_json:
                        ml_instance = WatsonMachineLearningInstance4ICP(credentials)
                        binding_name = 'Remote ICP {}'.format(binding_name)
                    else:
                        credentials = {}
                        ml_instance = WatsonMachineLearningInstance4ICP()
                        binding_name = 'ICP {}'.format(binding_name)
            else:
                ml_instance = WatsonMachineLearningInstance(credentials)
        elif self._args.ml_engine_type is MLEngineType.AZUREMLSTUDIO:
            ml_instance = AzureMachineLearningStudioInstance(credentials)
        elif self._args.ml_engine_type is MLEngineType.AZUREMLSERVICE:
            ml_instance = AzureMachineLearningServiceInstance(credentials)
        elif self._args.ml_engine_type is MLEngineType.SPSS:
            ml_instance = SPSSMachineLearningInstance(credentials)
        elif self._args.ml_engine_type is MLEngineType.CUSTOM:
            ml_instance = CustomMachineLearningInstance(credentials)
        elif self._args.ml_engine_type is MLEngineType.SAGEMAKER:
            ml_instance = SageMakerMachineLearningInstance(credentials)

        if self._args.ml_engine_type is not MLEngineType.WML or not self._args.is_icp: # WML spaces not yet supported in OpenScale public cloud
            start = time.time()
            self._binding_id = self._client.data_mart.bindings.add(binding_name, ml_instance)
            elapsed = time.time() - start
            logger.log_info('Binding {} created successfully'.format(self.get_binding_id()))
        else:
            if is_mrm_preprod:
                self._binding_id_mrm_preprod = '998'
                this_binding_id = self._binding_id_mrm_preprod
                label = 'pre_production'
            else:
                self._binding_id = '999'
                this_binding_id = self._binding_id
                label = 'production'
            payload = {
                "name": "WML {}".format(label),
                "description": "WML Instance designated as {}".format(label),
                "service_type": "watson_machine_learning",
                "instance_id": this_binding_id,
                "credentials": credentials,
                "operational_space_id": label,
                "deployment_space_id": ml_engine._space_id
            }
            bindings_url = "{}/v1/data_marts/{}/service_bindings/{}".format(self._credentials['url'], self._credentials['data_mart_id'], this_binding_id)
            start = time.time()
            response = requests.put(bindings_url, json=payload, headers=self.iam_headers, verify=self._verify)
            elapsed = time.time() - start
            logger.log_info('Binding {} {} created successfully'.format(label, this_binding_id))
        self.timer('data_mart.bindings.add', elapsed)

    def bind_mlinstance(self, credentials, ml_engine_prod=None, ml_engine_preprod=None):
        logger.log_info('Binding {} instance to {} ...'.format(self._args.ml_engine_type.name.lower(), self._args.service_name))
        binding_name = '{} Instance'.format(self._args.ml_engine_type.name)
        self._reliable_bind_mlinstance(binding_name, credentials, ml_engine_prod, is_mrm_preprod=False)
        if self._args.mrm:
            self._reliable_bind_mlinstance(binding_name, credentials, ml_engine_preprod, is_mrm_preprod=True)

    def use_existing_binding(self, asset_details_dict):
        if self._args.is_icp:
            self._binding_id = '999'
        else:
            self._binding_id = asset_details_dict['binding_uid']
        logger.log_info('Use existing binding {}'.format(self.get_binding_id()))

    @retry(tries=5, delay=4, backoff=2)
    def use_existing_subscription(self, asset_details_dict):
        self._asset_details_dict = asset_details_dict
        asset_uid = asset_details_dict['source_uid']
        deployment_uid = asset_details_dict['source_entry_metadata_guid']
        logger.log_info('Get existing subscription for model {} deployment {}...'.format(asset_uid, deployment_uid))
        start = time.time()
        all_subscriptions = self._client.data_mart.subscriptions.get_details()['subscriptions']
        elapsed = time.time() - start
        self.timer('data_mart.subscriptions.get_details(ALL)', elapsed)
        subscription_id = None
        for sub in all_subscriptions:
            if 'entity' in sub and 'asset' in sub['entity'] and 'asset_id' in sub['entity']['asset']:
                if sub['entity']['asset']['asset_id'] == asset_uid and 'deployments' in sub['entity']:
                    for dep in sub['entity']['deployments']:
                        if 'deployment_id' in dep and dep['deployment_id'] == deployment_uid:
                            if 'metadata' in sub and 'guid' in sub['metadata']:
                                subscription_id = sub['metadata']['guid']
        if not subscription_id:
            error_msg = 'ERROR: Could not find an existing subscription for model {} deployment {}'.format(asset_uid, deployment_uid)
            logger.log_error(error_msg)
            raise Exception(error_msg)
        start = time.time()
        self._subscription = self._client.data_mart.subscriptions.get(subscription_uid=subscription_id)
        elapsed = time.time() - start
        self._model.expected_payload_row_count = self._reliable_count_payload_rows('use existing subscription')
        logger.log_info('Subscription {} found successfully'.format(self.get_subscription_id()))
        self.timer('data_mart.subscriptions.get(ONE)', elapsed)
        self._reliable_count_datamart_rows('use existing subscription')

    @retry(tries=5, delay=4, backoff=2)
    def subscribe_to_model_deployment(self, asset_details_dict):
        '''
        Create subscription for the given model
        '''
        logger.log_info('Subscribing ML deployment to {} ...'.format(self._args.service_name))
        self._reliable_count_datamart_rows('create subscription start')
        asset_metadata = self._model.configuration_data['asset_metadata']
        asset_params = {
            'source_uid': asset_details_dict['source_uid'],
            'binding_uid': self.get_binding_id()
        }
        if 'problem_type' in asset_metadata:
            asset_params['problem_type'] = self._get_problem_type_object(asset_metadata['problem_type'])
        if 'input_data_type' in asset_metadata:
            asset_params['input_data_type'] = self._get_input_data_type_object(asset_metadata['input_data_type'])
        if self._model.training_data_reference:
            asset_params['training_data_reference'] = self._model.training_data_reference['cos_storage_reference']
        if 'label_column' in asset_metadata:
            asset_params['label_column'] = asset_metadata['label_column']
        if 'prediction_column' in asset_metadata:
            asset_params['prediction_column'] = asset_metadata['prediction_column']
        if 'class_probability_columns' in asset_metadata:
            asset_params['class_probability_columns'] = asset_metadata['class_probability_columns']
        if 'probability_column' in asset_metadata:
            asset_params['probability_column'] = asset_metadata['probability_column']
        if 'feature_columns' in asset_metadata:
            asset_params['feature_columns'] = asset_metadata['feature_columns']
        if 'categorical_columns' in asset_metadata:
            asset_params['categorical_columns'] = asset_metadata['categorical_columns']
        ml_asset = None
        if self._args.ml_engine_type is MLEngineType.WML:
            ml_asset = WatsonMachineLearningAsset(**asset_params)
        elif self._args.ml_engine_type is MLEngineType.AZUREMLSTUDIO:
            ml_asset = AzureMachineLearningStudioAsset(**asset_params)
        elif self._args.ml_engine_type is MLEngineType.AZUREMLSERVICE:
            ml_asset = AzureMachineLearningServiceAsset(**asset_params)
        elif self._args.ml_engine_type is MLEngineType.SPSS:
            ml_asset = SPSSMachineLearningAsset(**asset_params)
        elif self._args.ml_engine_type is MLEngineType.CUSTOM:
            ml_asset = CustomMachineLearningAsset(**asset_params)
        elif self._args.ml_engine_type is MLEngineType.SAGEMAKER:
            ml_asset = SageMakerMachineLearningAsset(**asset_params)
        deployment_uid = asset_details_dict['source_entry_metadata_guid']
        start = time.time()
        self._subscription = self._client.data_mart.subscriptions.add(ml_asset, deployment_uids=[deployment_uid])
        elapsed = time.time() - start
        self._asset_details_dict = asset_details_dict
        self._model.expected_payload_row_count = self._reliable_count_payload_rows('subscription created')
        logger.log_info('Subscription completed successfully (guid: {})'.format(self.get_subscription_id()))
        self.timer('data_mart.subscriptions.add', elapsed)
        self._reliable_count_datamart_rows('create subscription completed')

    def _get_input_data_type_object(self, data):
        if data == 'STRUCTURED':
            return InputDataType.STRUCTURED
        elif data == 'UNSTRUCTURED_IMAGE':
            return InputDataType.UNSTRUCTURED_IMAGE
        elif data == 'UNSTRUCTURED_TEXT':
            return InputDataType.UNSTRUCTURED_TEXT
        return None

    def _get_problem_type_object(self, data):
        if data == 'BINARY_CLASSIFICATION':
            return ProblemType.BINARY_CLASSIFICATION
        elif data == 'MULTICLASS_CLASSIFICATION':
            return ProblemType.MULTICLASS_CLASSIFICATION
        elif data == 'REGRESSION':
            return ProblemType.REGRESSION
        return None

    # not actually called, because payload logging and performance monitoring are both already enabled by default
    @retry(tries=5, delay=8, backoff=2)
    def configure_subscription(self):
        '''
        Configure payload logging and performance monitoring
        '''
        logger.log_info('Enabling payload logging ...')
        start = time.time()
        self._subscription.payload_logging.enable()
        elapsed = time.time() - start
        self.timer('subscription.payload_logging.enable', elapsed)
        logger.log_info('Payload logging enabled successfully')

        logger.log_info('Enabling performance monitoring ...')
        start = time.time()
        self._subscription.performance_monitoring.enable()
        elapsed = time.time() - start
        self.timer('subscription.performance_monitoring.enable', elapsed)
        logger.log_info('Performance monitoring enabled successfully')

    def configure_subscription_monitors(self):
        def _get_config_params(param_key_name):
            param_name = param_key_name.split('_')[0]
            params = None
            if param_key_name in self._model.configuration_data:
                params = self._model.configuration_data[param_key_name]
                logger.log_info('Configuring {} ...'.format(param_name))
            else:
                logger.log_info('Configuration for {} not provided for this model - skipping'.format(param_name))
            return params

        self.configure_explainability()
        self.configure_fairness(_get_config_params('fairness_configuration'))
        self.configure_quality(_get_config_params('quality_configuration'))
        self.configure_drift(_get_config_params('drift_configuration'))
        if self._args.bkpi:
            self.configure_bkpi(_get_config_params('businesskpi_configuration'))
        if self._args.mrm:
            self.configure_mrm(_get_config_params('mrm_configuration'))

    @retry(tries=5, delay=8, backoff=2)
    def configure_fairness(self, params):
        if params:
            if self._fairness_run_once:  # in case of retry
                feature_list = []
                for elem in params['features']:
                    feature_list.append(Feature(elem['feature'], elem['majority'], elem['minority'], float(elem['threshold'])))
                params['features'] = feature_list
                if not self._model.training_data_reference:
                    if self._model.training_data_statistics:
                        params['training_data_statistics'] = self._model.training_data_statistics
                    else:
                        params['training_data'] = self._model.training_data
                params['deployment_uid'] = self._asset_details_dict['source_entry_metadata_guid']
                self._fairness_run_once = False
            start = time.time()
            self._subscription.fairness_monitoring.enable(**params)
            elapsed = time.time() - start
            self.timer('subscription.fairness_monitoring.enable', elapsed)
            logger.log_info('Fairness configured successfully')

    @retry(tries=5, delay=8, backoff=2)
    def configure_quality(self, params):
        if params:
            start = time.time()
            self._subscription.quality_monitoring.enable(**params)
            elapsed = time.time() - start
            self.timer('subscription.quality_monitoring.enable', elapsed)
            logger.log_info('Quality configured successfully')

    @retry(tries=5, delay=8, backoff=2)
    def configure_explainability(self):
        explain_required_columns_absent = 'class_probability_columns' not in self._model.configuration_data['asset_metadata'] and 'probability_column' not in self._model.configuration_data['asset_metadata']
        is_xgboost_model = 'xgboost' in self._model.name.lower()
        if not is_xgboost_model and explain_required_columns_absent:
            logger.log_info('Explainability not available for this model')
            self._configure_explain = False
            return
        logger.log_info('Configuring explainability ...')
        params = {}
        if self._explainability_run_once: # in case of retry
            if not self._model.training_data_reference:
                if self._model.training_data_statistics:
                    params['training_data_statistics'] = self._model.training_data_statistics
                else:
                    params['training_data'] = self._model.training_data
            self._explainability_run_once = False
        start = time.time()
        self._subscription.explainability.enable(**params)
        elapsed = time.time() - start
        self.timer('subscription.explainability.enable', elapsed)
        logger.log_info('Explainability configured successfully')

    @retry(tries=5, delay=8, backoff=2)
    def configure_drift(self, params):
        if params:
            start = time.time()
            self._subscription.drift_monitoring.enable(**params)
            elapsed = time.time() - start
            self.timer('subscription.drift_monitoring.enable', elapsed)
            logger.log_info('Drift configured successfully')

    @retry(tries=5, delay=8, backoff=2)
    def _reliable_define_bkpi_application(self, params):
        params['name'] = self._model.metadata['model_name'] + '_Application'
        params['subscription_ids'] = [ self.get_subscription_id() ]
        bkpiapp_url = '{}/{}/v2/business_applications'.format(self._credentials['url'], self._credentials['data_mart_id'])
        start = time.time()
        response = requests.post(bkpiapp_url, json=params, headers=self.iam_headers, verify=self._verify)
        elapsed = time.time() - start
        self.timer('define business application', elapsed)
        if response.status_code != 202:
            error_msg = 'ERROR: create bkpi application: {} {}'.format(response.status_code, response.text)
            logger.log_error(error_msg)
            raise Exception(error_msg)
        self._model.metadata['bkpiapp_id'] = response.json()['metadata']['id']

    def configure_bkpi(self, params):
        if params:
            if self.is_mrm_preprod:
                logger.log_info('Skip BKPI configuration for pre-production model')
                return
            self._use_bkpi = True
            if 'business_application' in params:
                self._reliable_define_bkpi_application(params['business_application'])
                self._reliable_update_bkpi_subscription()
            else:
                error_msg = 'ERROR: "business_application" tag missing in bkpi_configuration'
                logger.log_error(error_msg)
                raise Exception(error_msg)
            logger.log_info('Businesskpi configured successfully (guid: {})'.format(self._model.metadata['bkpiapp_id']))

    @retry(tries=5, delay=8, backoff=2)
    def configure_mrm(self, params):
        # save preprod subscription id so it can be used later by prod subscription mrm configuration
        if self.is_mrm_preprod:
            self.mrm_preprod_subscription_id = self.get_subscription_id()

        # enable MRM for this subscription, whether challenger, preprod, or prod
        payload = {
            "data_mart_id": self._credentials['data_mart_id'],
            "monitor_definition_id": "mrm",
            "target": {
                "target_id": self.get_subscription_id(),
                "target_type": "subscription"
                },
            "parameters": { },
            "managed_by": "user"
            }
        mrm_url = '{}/openscale/{}/v2/monitor_instances'.format(self._credentials['url'], self._credentials['data_mart_id'])
        start = time.time()
        response = requests.post(mrm_url, json=payload, headers=self.iam_headers, verify=self._verify)
        elapsed = time.time() - start
        if response.status_code != 200 and response.status_code != 202:
            error_msg = 'ERROR: Failed to enable MRM, rc: {} url: {} payload: {} response: {}'.format(response.status_code, mrm_url, payload, response.text)
            logger.log_error(error_msg)
            raise Exception(error_msg)
        elapsed = time.time() - start
        response_json = response.json()
        if 'metadata' in response_json and 'id' in response_json['metadata']:
            if self.is_mrm_challenger:
                self.mrm_challenger_instance_id = response_json['metadata']['id']
            elif self.is_mrm_preprod:
                self.mrm_preprod_instance_id = response_json['metadata']['id']
            else:
                self.mrm_prod_instance_id = response_json['metadata']['id']
        self.timer('subscription.mrm.enable', elapsed)

        # for the preprod model, mark it as approved for production
        if self.is_mrm_preprod and self.mrm_preprod_instance_id:
            payload = {'state': 'approved'}
            mrm_url = '{}/openscale/{}/v2/subscriptions/{}/risk_evaluation_status'.format(self._credentials['url'], self._credentials['data_mart_id'], self.get_subscription_id())
            start = time.time()
            response = requests.put(mrm_url, json=payload, headers=self.iam_headers, verify=self._verify)
            elapsed = time.time() - start
            if response.status_code != 200:
                error_msg = 'ERROR: Failed to approve pre-prod model, rc: {} url: {} payload: {} response: {}'.format(response.status_code, mrm_url, payload, response.text)
                logger.log_error(error_msg)
                raise Exception(error_msg)
            self.timer('subscription.mrm approve preprod', elapsed)

        # for the prod model, link it back to the preprod model
        if self.is_mrm_prod and self.mrm_preprod_subscription_id:
            payload = [{ "op": "add", "path": "/pre_production_reference_id", "value": self.mrm_preprod_subscription_id }]
            mrm_url = '{}/openscale/{}/v2/subscriptions/{}'.format(self._credentials['url'], self._credentials['data_mart_id'], self.get_subscription_id())
            start = time.time()
            response = requests.patch(mrm_url, json=payload, headers=self.iam_headers, verify=self._verify)
            elapsed = time.time() - start
            if response.status_code != 200:
                error_msg = 'ERROR: Failed to patch subscription with pre-prod reference, rc: {} url: {} payload: {} response: {}'.format(response.status_code, mrm_url, payload, response.text)
                logger.log_error(error_msg)
                raise Exception(error_msg)
            self.timer('subscription.mrm patch prod', elapsed)

        logger.log_info('MRM configured successfully')

    def generate_sample_metrics(self):
        if self._args.history < 1 or (self._args.mrm and self.is_mrm_challenger or self.is_mrm_preprod):
            return False
        self._reliable_count_datamart_rows('generate sample metrics start')
        return True

    def save_subscription_details(self):
        subscription_details = json.dumps(self._client.data_mart.subscriptions.get_details())
        temp_file = logging_temp_file.name.replace('{}.log'.format(cli_name), '{}-{}.json'.format(cli_name, 'subscription-details'))
        logger.log_info('Saving datamart subscription details to: {}'.format(temp_file))
        with open(temp_file, "w+") as f:
            f.write(subscription_details)

    def load_historical_payloads(self):
        self._no_historical_payloads = False
        self._history_load_start_time = datetime.utcnow()
        for day in range(self._args.history_first_day, self._args.history_first_day + self._args.history):
            records = self._model.get_payload_history(day)
            if day == self._args.history_first_day:
                if len(records) == 0:
                    self._no_historical_payloads = True # use later to skip generating drift history
                    logger.log_info('No historical payload records provided - skipping')
                    break
                else:
                    logger.log_info('Loading historical payload records to {} ...'.format(self._args.service_name))
            logger.log_info(' - Loading day {}'.format(day + 1))
            self._reliable_post_payloads(records)
            if (day + 1) == self._args.history:
                logger.log_info('Historical payloads loaded successfully')
                self._model.expected_payload_row_count += self._model.historical_payload_row_count

    def load_historical_performance(self):
        for day in range(self._args.history_first_day, self._args.history_first_day + self._args.history):
            records = self._model.get_performance_history(day)
            if day == self._args.history_first_day:
                if len(records) == 0:
                    logger.log_info('No historical performance metrics provided - skipping')
                    break
                else:
                    logger.log_info('Loading historical performance metrics to {} ...'.format(self._args.service_name))
            logger.log_info(' - Loading day {}'.format(day + 1))
            self._reliable_post_metrics('performance', records)
            if (day + 1) == self._args.history:
                logger.log_info('Historical performance metrics loaded successfully')

    def load_historical_explanations(self):
        records = self._model.get_explain_history()
        if len(records) == 0:
            logger.log_info('No historical explanations provided - skipping')
        else:
            logger.log_info('Loading historical explanations to {} ...'.format(self._args.service_name))
            for record in records:
                self._reliable_store_explanation(record)
            logger.log_info('Historical explanations loaded successfully')
        self._reliable_count_datamart_rows('generate sample metrics completed')

    def load_historical_fairness(self):
        for day in range(self._args.history_first_day, self._args.history_first_day + self._args.history):
            records = self._model.get_fairness_history(day)
            if day == self._args.history_first_day:
                if len(records) == 0:
                    logger.log_info('No historical fairness metrics provided - skipping')
                    break
                else:
                    logger.log_info('Loading historical fairness metrics to {} ...'.format(self._args.service_name))
            logger.log_info(' - Loading day {}'.format(day + 1))
            self._reliable_post_metrics('fairness', records)
            if (day + 1) == self._args.history:
                logger.log_info('Historical fairness metrics loaded successfully')

        for day in range(self._args.history_first_day, self._args.history_first_day + self._args.history):
            records = self._model.get_debias_history(day)
            if day == self._args.history_first_day:
                if len(records) == 0:
                    logger.log_info('No historical debiased fairness metrics provided - skipping')
                    break
                else:
                    logger.log_info('Loading historical debiased fairness metrics to {} ...'.format(self._args.service_name))
            logger.log_info(' - Loading day {}'.format(day + 1))
            self._reliable_post_metrics('debiased_fairness', records)
            if (day + 1) == self._args.history:
                logger.log_info('Historical debiased fairness metrics loaded successfully')

        for day in range(self._args.history_first_day, self._args.history_first_day + self._args.history):
            records = self._model.get_manual_labeling_history(day)
            if day == self._args.history_first_day:
                if len(records) == 0:
                    logger.log_info('No historical manual labeling data provided - skipping')
                    break
                else:
                    logger.log_info('Loading historical manual labeling data to {} ...'.format(self._args.service_name))
            logger.log_info(' - Loading day {}'.format(day + 1))
            self._reliable_post_manual_labeling(records)
            if (day + 1) == self._args.history:
                logger.log_info('Historical manual labeling data loaded successfully')

    def load_historical_quality(self):
        if not self._model.feedback_history:
            logger.log_info('No historical feedback data provided for this model - skipping')
        else:
            logger.log_info('Loading historical feedback data ...')
            self._reliable_upload_feedback(self._model.feedback_history)
            logger.log_info('Historical feedback data loaded successfully')

        for day in range(self._args.history_first_day, self._args.history_first_day + self._args.history):
            records = self._model.get_quality_history(day)
            if day == self._args.history_first_day:
                if len(records) == 0:
                    logger.log_info('No historical quality metrics provided - skipping')
                    break
                else:
                    logger.log_info('Loading historical quality metrics to {} ...'.format(self._args.service_name))
            logger.log_info(' - Loading day {}'.format(day + 1))
            self._reliable_post_metrics('quality', records)
            if (day + 1) == self._args.history:
                logger.log_info('Historical quality metrics loaded successfully')

        for day in range(self._args.history_first_day, self._args.history_first_day + self._args.history):
            records = self._model.get_quality_monitor_history(day)
            if day == self._args.history_first_day:
                if len(records) == 0:
                    logger.log_info('No historical quality monitor metrics provided - skipping')
                    break
                else:
                    logger.log_info('Loading historical quality monitor metrics to {} ...'.format(self._args.service_name))
            logger.log_info(' - Loading day {}'.format(day + 1))
            self._reliable_store_quality_monitor_metrics(records)
            if (day + 1) == self._args.history:
                logger.log_info('Historical quality monitor metrics loaded successfully')

    def load_historical_bkpi(self):
        if self._use_bkpi:
            for day in range(self._args.history_first_day, self._args.history_first_day + self._args.history):
                records = self._model.get_bkpi_metrics_history(day)
                if day == self._args.history_first_day:
                    if len(records) == 0:
                        logger.log_info('No historical business kpi metrics provided - skipping')
                        break
                    else:
                        logger.log_info('Loading historical business kpi metrics to {} ...'.format(self._args.service_name))
                logger.log_info(' - Loading day {}'.format(day + 1))
                self._reliable_store_bkpi_metrics(records)
                self._reliable_store_bkpi_drift_metrics(records)
                if (day + 1) == self._args.history:
                    logger.log_info('Historical business kpi metrics loaded successfully')
            for day in range(self._args.history_first_day, self._args.history_first_day + self._args.history):
                records = self._model.get_bkpi_payload_history(day)
                if day == self._args.history_first_day:
                    if len(records) == 0:
                        logger.log_info('No historical business kpi  provided - skipping')
                        break
                    else:
                        logger.log_info('Loading historical business kpi payloads to {} ...'.format(self._args.service_name))
                logger.log_info(' - Loading day {}'.format(day + 1))
                self._reliable_store_bkpi_data_set(records, 'business_payload')
                if (day + 1) == self._args.history:
                    logger.log_info('Historical business kpi payloads loaded successfully')
            for day in range(self._args.history_first_day, self._args.history_first_day + self._args.history):
                records = self._model.get_bkpi_txn_batches_id_map_history(day)
                if day == self._args.history_first_day:
                    if len(records) == 0:
                        logger.log_info('No historical business kpi transaction batches id maps provided - skipping')
                        break
                    else:
                        logger.log_info('Loading historical business kpi transaction batches id maps to {} ...'.format(self._args.service_name))
                logger.log_info(' - Loading day {}'.format(day + 1))
                self._reliable_store_bkpi_data_set(records, 'transaction_batches')
                if (day + 1) == self._args.history:
                    logger.log_info('Historical business kpi transaction batches id maps loaded successfully')

    def confirm_payload_logging(self):
        self.wait_for_payload_logging(initial_pause=8+int(self._model.historical_payload_row_count/250), context='payload history')
        self._reliable_count_datamart_rows('confirm payload logging')

    def load_historical_debiased_payloads(self):
        for day in range(self._args.history_first_day, self._args.history_first_day + self._args.history):
            records = self._model.get_debiased_payload_history(day)
            if day == self._args.history_first_day:
                if len(records) == 0:
                    logger.log_info('No historical debiased payloads provided - skipping')
                    break
                else:
                    logger.log_info('Loading historical debiased payloads to {} ...'.format(self._args.service_name))
            logger.log_info(' - Loading day {}'.format(day + 1))
            self._reliable_post_debiased_payloads(records)
            if (day + 1) == self._args.history:
                logger.log_info('Historical debiased payloads loaded successfully')

    def load_historical_drift(self):
        if 'drift_configuration' in self._model.configuration_data and self._args.history > 0:
            if self._args.generate_drift_history:
                if self._no_historical_payloads:
                    logger.log_info('No historical payloads provided - skipping drift history generation')
                else:
                    logger.log_info('Generating {} days of historical drift metrics to {} ...'.format(self._args.history, self._args.service_name))
                    end_time = self._history_load_start_time - timedelta(hours=self._args.history_first_day*24)
                    start_time = end_time - timedelta(hours=24*self._args.history)
                    windows = 8 * self._args.history # 3 hour drift windows, so 8 per day
                    self._reliable_generate_drift_metrics(start_time, end_time, windows)
                    logger.log_info('Historical drift metrics generated successfully')
            else:
                for day in range(self._args.history_first_day, self._args.history_first_day + self._args.history):
                    records = self._model.get_drift_metrics_history(day)
                    if day == self._args.history_first_day:
                        if len(records) == 0:
                            logger.log_info('No historical drift metrics provided - skipping')
                            break
                        else:
                            logger.log_info('Loading historical drift metrics to {} ...'.format(self._args.service_name))
                    logger.log_info(' - Loading day {}'.format(day + 1))
                    self._post_drift_metrics(records, day)
                    if (day + 1) == self._args.history:
                        logger.log_info('Historical drift metrics loaded successfully')

    @retry(tries=5, delay=8, backoff=2)
    def _reliable_store_explanation(self, record):
        explain_url = '{0}/v1/data_marts/{1}/explanations'.format(self._credentials['url'], self._credentials['data_mart_id'])
        iam_headers = { 'Authorization': self.iam_headers['Authorization']} # no Content-Type
        record['binding_id'] = self.get_binding_id()
        record['subscription_id'] = self.get_subscription_id()
        record['deployment_id'] = self.get_deployment_id()
        record['request_id'] = uuid.uuid4().hex
        record['explanation']['entity']['asset']['id'] = self.get_subscription_id()
        record['explanation']['entity']['asset']['name'] = self._model.metadata['model_name']
        record['explanation']['entity']['asset']['deployment']['id'] = self.get_deployment_id()
        record['explanation']['entity']['asset']['deployment']['name'] = self._model.metadata['model_name']
        record_file = { "explanation": ("explanation.json", json.dumps(record), "application/json") }
        start = time.time()
        response = requests.post(explain_url, files=record_file, headers=iam_headers, verify=self._verify)
        elapsed = time.time() - start
        if response.status_code != 202:
            error_msg = 'ERROR: Failed to store explanation, rc: {} {}'.format(response.status_code, response.text)
            logger.log_error(error_msg)
            raise Exception(error_msg)
        logger.log_info('Explanation stored for transaction {}'.format(record['scoring_id']))
        self.timer('store explanation', elapsed)

    @retry(tries=5, delay=8, backoff=2)
    def _reliable_upload_feedback(self, feedback_data):
        start = time.time()
        if self._model.is_unstructured_text:
            self._subscription.feedback_logging.store(feedback_data)
        else:
            self._subscription.feedback_logging.store(feedback_data, feedback_format=FeedbackFormat.DICT)
        elapsed = time.time() - start
        self.timer('subscription.feedback_logging.store', elapsed)

    @retry(tries=5, delay=4, backoff=2)
    def _reliable_single_score(self, engine_client, deployment_url, score_input, score_num, values_per_score, totalelapsed, firststart, lastend, tokenizer=None):
        record = None
        start = time.time()
        if self._args.v4:
            deployment_id = self._asset_details_dict['source_entry_metadata_guid']
            if 'fields' in score_input:
                record = engine_client.score(deployment_id, values=score_input['values'], fields=score_input['fields'])
            elif 'fields' not in score_input:
                record = engine_client.score(deployment_id, values=score_input['values'])
        else:
            record = engine_client.deployments.score(deployment_url, score_input)
        end = time.time()
        elapsed = end - start
        totalelapsed += elapsed
        lastend = end
        duration = lastend - firststart
        logger.log_timer('WML deployment.score {} values(s) in {:.3f} seconds, total requests: {}, duration: {:.3f} seconds, elapsed: {:.3f} seconds'.format(values_per_score, elapsed, score_num+1, duration, totalelapsed))
        self.timer('WML deployment.score {} value(s)'.format(values_per_score), elapsed)
        if self._args.generate_payload_history:
            logger.log_info('{},'.format ({"scoring_id": uuid.uuid4().hex, "request": score_input, "response": record, "response_time": int(1000*elapsed)}))
        if self._args.v4:
            record = record['predictions'][0]
        return totalelapsed, duration, lastend, record

    def generate_sample_scoring(self, engine_client, numscores, values_per_score, to_init_payload_logging=False):
        # no feedback or sample scoring for MRM pre-production models
        if not to_init_payload_logging and self._args.mrm and not self.is_mrm_prod:
            return

        # first, generate sample feedback if requested, then move on to scoring
        if not to_init_payload_logging and not self._args.no_new_feedback:
            if not self._model.feedback_data:
                logger.log_info('New feedback data not provided for this model - skipping')
            else:
                logger.log_info('Adding new feedback data ...')
                self._reliable_upload_feedback(self._model.feedback_data)
                logger.log_info('New feedback data added successfully')

        if numscores < 1:
            return
        if to_init_payload_logging:
            logger.log_info('Initialize payload logging by sending one sample scoring request')

        message = 'Generating {} scoring request(s) ...'.format(numscores)
        if values_per_score > 1:
            message = message.replace('...', 'with {} values per request ...'.format(values_per_score))
        logger.log_info(message)
        records_list = []
        if self._args.ml_engine_type is MLEngineType.WML:
            if self._args.v4:
                native_client = engine_client.get_native_client()
                deployment_details = native_client.deployments.get_details(self._asset_details_dict['source_entry_metadata_guid'])
                deployment_url = native_client.deployments.get_scoring_href(deployment_details)
            else:
                engine_client = self._client.data_mart.bindings.get_native_engine_client(binding_uid=self.get_binding_id())
                deployment_details = engine_client.deployments.get_details(self._asset_details_dict['source_entry_metadata_guid'])
                deployment_url = engine_client.deployments.get_scoring_url(deployment_details)

            is_local_icp_wml = False
            is_remote_icp_wml = False
            is_cloud_wml = False
            if self._args.is_icp and self._args.v4:
                api_env = ApiEnvironment()
                if self._args.wml or self._args.wml_json:
                    if 'apikey' in self._ml_engine_credentials:
                        is_cloud_wml = True
                    else:
                        is_remote_icp_wml = True
                else:
                    is_local_icp_wml = True
                if api_env.is_running_on_icp:
                    if is_local_icp_wml:
                        elements = get_url_elements(api_env.icp_gateway_url)
                        deployment_url = update_url(deployment_url, new_hostname=elements.hostname, new_scheme=elements.scheme)
                        deployment_url = remove_port_from_url(deployment_url)
                else:
                    icp4d_port = get_url_elements(self._credentials['url']).port
                    port = get_url_elements(deployment_url).port
                    if not port or port != icp4d_port:
                        deployment_url = update_url(deployment_url, new_hostname=None, new_port=icp4d_port, new_scheme=None)

            pause = self._args.pause_between_scores
            if pause > 0.0:
                logger.log_info('{:.3f} second pause between each scoring request'.format(pause))
            totalelapsed = 0.0
            firststart = time.time()
            lastend = firststart
            self._model.expected_payload_row_count += numscores * values_per_score
            for score_num in range(numscores):
                if pause > 0.0 and score_num > 0:
                    time.sleep(pause)
                fields, values = self._model.get_score_input(values_per_score)
                tokenizer = None
                if self._model.is_unstructured_image:
                    score_input = values
                else:
                    if self._model.is_unstructured_text:
                        tokenizer = self._model.tokenizer
                    score_input = {'fields': fields, 'values': values}
                (totalelapsed, duration, lastend, record) = self._reliable_single_score(engine_client, deployment_url, score_input, score_num, values_per_score, totalelapsed, firststart, lastend, tokenizer=tokenizer)
                # manual payload logging if remote-cloud-wml or remote-icp-wml is used on icp
                if is_cloud_wml or is_remote_icp_wml:
                    pl_record = PayloadRecord(request=score_input, response=record, response_time=int(duration))
                    records_list.append(pl_record)
            logger.log_timer('Total score requests: {}, total scores: {}, duration: {:.3f} seconds'.format(numscores, numscores*values_per_score, duration))
            logger.log_timer('Throughput: {:.3f} score requests per second, {:.3f} scores per second, average score request time: {:.3f} seconds'.format(numscores/duration, numscores*values_per_score/duration, totalelapsed/numscores))

        elif self._args.ml_engine_type is MLEngineType.AZUREMLSTUDIO:
            engine_client.setup_scoring_metadata(self._subscription)
            self._model.expected_payload_row_count += numscores
            for _ in range(numscores):
                fields, values = self._model.get_score_input(1)
                values = values[0]
                value_dict = {}
                for (index, field) in enumerate(fields):
                    value_dict[field] = values[index]
                start = time.time()
                record = engine_client.score({'Inputs': {'input1': [value_dict]}, 'GlobalParameters': {}})
                elapsed = time.time() - start
                self.timer('AzureML score', elapsed)
                records_list.append(record)

        elif self._args.ml_engine_type is MLEngineType.AZUREMLSERVICE:
            engine_client.setup_scoring_metadata(self._subscription)
            self._model.expected_payload_row_count += numscores
            for _ in range(numscores):
                fields, values = self._model.get_score_input(1)
                values = values[0]
                value_dict = {}
                for (index, field) in enumerate(fields):
                    value_dict[field] = values[index]
                start = time.time()
                record = engine_client.score({"input": [value_dict]})
                elapsed = time.time() - start
                self.timer('AzureML score', elapsed)
                records_list.append(record)

        elif self._args.ml_engine_type is MLEngineType.SPSS:
            engine_client.setup_scoring_metadata(self._subscription)
            subscription_details = self._subscription.get_details()
            model_name_id = subscription_details['entity']['asset']['name']
            input_table_id = subscription_details['entity']['asset_properties']['input_data_schema']['id']
            self._model.expected_payload_row_count += numscores
            for _ in range(numscores):
                spss_data = {'requestInputTable':[{'id': input_table_id, 'requestInputRow':[{'input':[]}]}],'id':model_name_id}
                fields, values = self._model.get_score_input(1)
                values = values[0]
                value_dict = {}
                for (index, field) in enumerate(fields):
                    entry_dict = {'name':str(field),'value':str(values[index])}
                    spss_data['requestInputTable'][0]['requestInputRow'][0]['input'].append(entry_dict)
                start = time.time()
                record = engine_client.score(spss_data)
                elapsed = time.time() - start
                self.timer('SPSS score', elapsed)
                records_list.append(record)
        elif self._args.ml_engine_type is MLEngineType.CUSTOM:
            engine_client.setup_scoring_metadata(self._subscription)
            self._model.expected_payload_row_count += numscores
            for _ in range(numscores):
                fields, values = self._model.get_score_input(1)
                score_input = {'fields': fields, 'values': values }
                start = time.time()
                record = engine_client.score(score_input)
                elapsed = time.time() - start
                self.timer('Custom score', elapsed)
                records_list.append(record)
        elif self._args.ml_engine_type is MLEngineType.SAGEMAKER:
            records_list = []
            engine_client.setup_scoring_metadata(self._subscription)
            self._model.expected_payload_row_count += numscores
            for _ in range(numscores):
                fields, values = self._model.get_score_input(1)
                values = values[0]
                start = time.time()
                record = engine_client.score(fields, values)
                elapsed = time.time() - start
                self.timer('Sagemaker score', elapsed)
                records_list.append(record)
        if records_list:
            start = time.time()
            self._subscription.payload_logging.store(records=records_list)
            elapsed = time.time() - start
            self.timer('subscription.payload_logging.store', elapsed)

        logger.log_info('Scoring request(s) generated successfully')
        if to_init_payload_logging:
            context = 'init payload logging'
        else:
            context = 'live scoring'
        self.wait_for_payload_logging(context=context, to_init_payload_logging=to_init_payload_logging)
        self._reliable_count_datamart_rows('generated sample scores and confirmed payload logging')

    @retry(tries=5, delay=4, backoff=2)
    def _reliable_count_payload_rows(self, context=None):
        start = time.time()
        actual_payload_rows = self._subscription.payload_logging.get_records_count()
        elapsed = time.time() - start
        if context:
            context = ', {}'.format(context)
        else:
            context = ''
        logger.log_timer('subscription count payload rows in {:.3f} seconds, rows={}, expected={}{}'.format(elapsed, actual_payload_rows, self._model.expected_payload_row_count, context))
        return actual_payload_rows

    @retry(tries=5, delay=4, backoff=2)
    def _reliable_count_datamart_rows(self, context=None):
        if self._database is None: # internal db
            logger.log_debug('DEBUG: cannot count datamart rows for internal db')
            if self._args.database_counts:
                logger.log_info('Cannot count datamart rows for internal db - skipping')
            return
        start = time.time()
        datamart_rows = self._database.count_datamart_rows(self._datamart_name, context=context)
        elapsed = time.time() - start
        if context:
            context = ', {}'.format(context)
        else:
            context = ''
        logger.log_timer('count datamart rows in {:.3f} seconds{}'.format(elapsed, context))
        logger.log_debug(datamart_rows)
        if self._args.database_counts:
            try:
                from tabulate import tabulate
            except:
                from ibm_ai_openscale_cli.utility_classes.utils import pip_install
                pip_install('tabulate')
            headers = ['table', 'row count']
            logger.log_info('\n{}\n'.format(tabulate(datamart_rows, headers=headers, tablefmt='orgtbl')))

    def wait_for_payload_logging(self, initial_pause=8, context=None, to_init_payload_logging=False):
        logger.log_info('Confirming that all payloads have been stored to the datamart database ...')
        logger.log_info('(start with {} second wait to give payload logging time to complete)'.format(initial_pause))
        time.sleep(initial_pause)
        for pause in [16, 32, 64, 64]:
            actual_payload_rows = self._reliable_count_payload_rows(context)
            if self._model.expected_payload_row_count == actual_payload_rows:
                logger.log_info('Confirmed that the expected {} rows are in the payload table for this model'.format(actual_payload_rows))
                return
            elif self._model.expected_payload_row_count < actual_payload_rows:
                logger.log_warning('Expecting {} rows in the payload table for this model, but {} rows already in table'.format(self._model.expected_payload_row_count, actual_payload_rows))
                break
            else:
                delaymsg = ', pause {} seconds and check again ...'.format(pause)
                logger.log_error('Expecting {} rows in the payload table for this model, {} rows currently in table{}'.format(self._model.expected_payload_row_count, actual_payload_rows, delaymsg))
                time.sleep(pause)
        if to_init_payload_logging and actual_payload_rows < 1:
            error_msg = 'OpenScale did not receive the scoring payload, so setup cannot continue. Please try again.'
            logger.log_error(error_msg)
            raise Exception(error_msg)
        message = 'WARNING: unable to confirm that the expected number of payloads are stored into the datamart database'
        logger.log_warning(message)
        self.metric_check_errors.append([self._model.name, 'payload-logging', 'failed (count-mismatch)'])


    def trigger_monitors(self):
        background_mode = self._args.async_checks
        if self._args.no_checks:
            logger.log_info('Skip monitor checks')
            return
        if self._args.mrm:
            self.trigger_mrm_check((background_mode and not self.is_mrm_prod)) # always do MRM prod model MRM check synchronously (should be fast)
            self._reliable_count_datamart_rows('mrm monitor triggered')
            if not self.is_mrm_prod:
                logger.log_info('Skip other monitor checks')
                return
        self.trigger_bkpi_correlation_monitor(background_mode)
        self._reliable_count_datamart_rows('correlation monitor triggered')
        self._reliable_trigger_fairness_check(background_mode)
        self._reliable_count_datamart_rows('fairness monitor triggered')
        self._reliable_trigger_quality_check(background_mode)
        self._reliable_count_datamart_rows('quality monitor triggered')
        self._reliable_trigger_drift_check(background_mode)
        self._reliable_count_datamart_rows('drift monitor triggered')

    @retry(tries=5, delay=4, backoff=2)
    def _reliable_trigger_fairness_check(self, background_mode):
        if 'fairness_configuration' not in self._model.configuration_data:
            logger.log_info('Skip fairness check since fairness not configured for model')
        else:
            try:
                deployment_uid = self._asset_details_dict['source_entry_metadata_guid']
                logger.log_info('Triggering immediate fairness check ...')
                start = time.time()
                result = self._subscription.fairness_monitoring.run(deployment_uid, background_mode=background_mode)
                elapsed = time.time() - start
                self.timer('subscription.fairness_monitoring.run', elapsed)
                logger.log_info('Fairness check triggered')
                if not background_mode:
                    if not result or (isinstance(result, str) and 'error' in result.lower()) or result['entity']['parameters']['last_run_status'].lower() != 'finished':
                        self.metric_check_errors.append([self._model.name, 'fairness-check', 'failed'])
            except Exception as e:
                message = 'WARNING: Problems occurred while running fairness check: {}'.format(str(e))
                logger.log_warning(message)
                self.metric_check_errors.append([self._model.name, 'fairness-check', 'failed'])

    @retry(tries=5, delay=4, backoff=2)
    def _reliable_trigger_quality_check(self, background_mode):
        if 'quality_configuration' not in self._model.configuration_data:
            logger.log_info('Skip quality check since quality monitoring not configured for model')
        elif (not self._model.feedback_data or self._args.no_new_feedback) and (not self._model.feedback_history or self._args.history < 1):
            logger.log_info('Skip quality check for model since there is no feedback data yet')
        else:
            try:
                logger.log_info('Triggering immediate quality check ...')
                start = time.time()
                result = self._subscription.quality_monitoring.run(background_mode=background_mode)
                elapsed = time.time() - start
                self.timer('subscription.quality_monitoring.run', elapsed)
                logger.log_info('Quality check triggered')
                if not background_mode:
                    if not result or (isinstance(result, str) and 'error' in result.lower()) or result['status'].lower() != 'completed':
                        self.metric_check_errors.append([self._model.name, 'quality-check', 'failed'])
            except Exception as e:
                message = 'WARNING: Problems occurred while running quality check: {}'.format(str(e))
                logger.log_warning(message)
                self.metric_check_errors.append([self._model.name, 'quality-check', 'failed'])

    @retry(tries=5, delay=4, backoff=2)
    def _reliable_trigger_drift_check(self, background_mode):
        if 'drift_configuration' not in self._model.configuration_data:
            logger.log_info('Skip drift check since drift monitoring not configured for model')
        else:
            try:
                logger.log_info('Triggering immediate drift check ...')
                start = time.time()
                result = self._subscription.drift_monitoring.run(background_mode=background_mode)
                elapsed = time.time() - start
                self.timer('subscription.drift_monitoring.run', elapsed)
                logger.log_info('Drift check triggered')
                if not result or (isinstance(result, str) and 'error' in result.lower()):
                    self.metric_check_errors.append([self._model.name, 'drift-check', 'failed'])
            except Exception as e:
                message = 'WARNING: Problems occurred while running drift check: {}'.format(str(e))
                logger.log_warning(message)
                self.metric_check_errors.append([self._model.name, 'drift-check', 'failed'])

    @retry(tries=5, delay=4, backoff=2)
    def _reliable_trigger_mrm_prod_check(self, mrm_instance_id, background_mode):
        mrm_url = '{}/openscale/{}/v2/monitor_instances/{}/runs'.format(self._credentials['url'], self._credentials['data_mart_id'], mrm_instance_id)
        payload = { 'triggered_by': 'user' }

        # trigger the MRM check
        start = time.time()
        response = requests.post(url=mrm_url, json=payload, headers=self.iam_headers, verify=self._verify)
        elapsed = time.time() - start
        self.timer('trigger mrm prod check', elapsed)

        # check to see if the call was successful
        if response.status_code != 201 and response.status_code != 202:
            error_msg = 'ERROR: Failed to trigger MRM check, url: {}, rc: {}, response: {}'.format(mrm_url, response.status_code, response.text)
            logger.log_error(error_msg)
            raise Exception(error_msg)
        mrm_run_id = None
        json_data = response.json()
        if "metadata" in json_data and "id" in json_data["metadata"]:
            mrm_run_id = json_data["metadata"]["id"]
        else:
            error_msg = 'ERROR: Failed to trigger MRM check, url: {}, rc: {}, response: {}'.format(mrm_url, response.status_code, response.text)
            logger.log_error(error_msg)
            raise Exception(error_msg)
        return mrm_run_id

    @retry(tries=5, delay=4, backoff=2)
    def _reliable_trigger_mrm_preprod_check(self, mrm_instance_id, background_mode):
        if self.is_mrm_challenger:
            filename = 'test_data_challenger.csv'
        else:
            filename = 'test_data_preprod.csv'
        mrm_url = '{}/openscale/{}/v2/monitoring_services/mrm/monitor_instances/{}/risk_evaluations?test_data_set_name={}'.format(self._credentials['url'], self._credentials['data_mart_id'], mrm_instance_id, filename)
        payload = self._model._feedback_csv

        # trigger the MRM check
        iam_headers = { 'Authorization': self.iam_headers['Authorization'], 'Content-Type': 'text/csv'} # binary-coded csv payload
        start = time.time()
        response = requests.post(url=mrm_url, data=payload, headers=iam_headers, verify=self._verify)
        elapsed = time.time() - start
        self.timer('trigger mrm preprod check', elapsed)

        # check to see if the call was successful
        if response.status_code != 201 and response.status_code != 202:
            error_msg = 'ERROR: Failed to trigger MRM check, url: {}, rc: {}, response: {}'.format(mrm_url, response.status_code, response.text)
            logger.log_error(error_msg)
            raise Exception(error_msg)

    @retry(tries=5, delay=4, backoff=2)
    def _reliable_get_mrm_check_status(self, mrm_instance_id, mrm_run_id=None):
        # different URLs to check MRM run status between prod and pre-prod (PreProd or Challenger)
        if self.is_mrm_prod:
            results_url = '{}/openscale/{}/v2/monitor_instances/{}/runs/{}'.format(self._credentials['url'], self._credentials['data_mart_id'], mrm_instance_id, mrm_run_id)
        else:
            results_url = '{}/openscale/{}/v2/monitoring_services/mrm/monitor_instances/{}/risk_evaluations'.format(self._credentials['url'], self._credentials['data_mart_id'], mrm_instance_id)
        start = time.time()
        response = requests.get(url=results_url, headers=self.iam_headers, verify=self._verify)
        elapsed = time.time() - start
        if response.status_code != 200:
            error_msg = 'ERROR: Failed to get MRM check status, rc: {} {}'.format(response.status_code, response.text)
            raise Exception(error_msg)
        state = response.json()['entity']['status']['state']
        logger.log_debug('MRM check status: {}'.format(state))
        if state == 'error':
            error_msg = 'ERROR: MRM check failed: {}'.format(response.text)
            raise Exception(error_msg)
        self.timer('get mrm monitoring.run', elapsed)
        return response

    def trigger_mrm_check(self, background_mode):
        if 'mrm_configuration' not in self._model.configuration_data:
            logger.log_info('Skip mrm check since MRM not configured for model')
            return

        logger.log_info('Triggering immediate mrm check ...')
        if self.is_mrm_prod:
            mrm_instance_id = self.mrm_prod_instance_id
            mrm_run_id = self._reliable_trigger_mrm_prod_check(mrm_instance_id, background_mode)
        else:
            if self.is_mrm_challenger:
                mrm_instance_id = self.mrm_challenger_instance_id
            elif self.is_mrm_preprod:
                mrm_instance_id = self.mrm_preprod_instance_id
            self._reliable_trigger_mrm_preprod_check(mrm_instance_id, background_mode)
            mrm_run_id = None

        if background_mode:
            logger.log_info('MRM check triggered')
            return
        logger.log_info('MRM check running ...')

        try:
            check_completed = False
            for i in range(18):
                response = self._reliable_get_mrm_check_status(mrm_instance_id, mrm_run_id)
                state = response.json()['entity']['status']['state'].lower()
                if state != 'running' and state != 'upload_in_progress':
                    check_completed = True
                    break
                logger.log_info('MRM check still running; wait 10 seconds and check again')
                time.sleep(10)
            if check_completed:
                logger.log_info('MRM check completed')
            else:
                logger.log_info('MRM check did not complete in 3 minutes, continuing')
        except Exception as e:
            message = 'WARNING: Problems occurred while running MRM check: {}'.format(str(e))
            logger.log_warning(message)
            self.metric_check_errors.append([self._model.name, 'mrm-check', 'failed'])

    @retry(tries=5, delay=4, backoff=2)
    def _reliable_trigger_bkpi_correlation_monitor(self):
        bkpiapp_id = self._model.metadata['bkpiapp_id']
        monitors_url = '{}/openscale/{}/v2/monitor_instances'.format(self._credentials['url'], self._credentials['data_mart_id'])
        start = time.time()
        response = requests.get(url=monitors_url, headers=self.iam_headers, verify=self._verify)
        elapsed = time.time() - start
        self.timer('list all monitors', elapsed)
        if response.status_code != 200:
            error_msg = 'ERROR: Failed to list monitors, rc: {} {}'.format(response.status_code, response.text)
            logger.log_error(error_msg)
            raise Exception(error_msg)
        instances = response.json()['monitor_instances']
        correlations_instance_id = None
        for instance in instances:
            if instance['entity']['monitor_definition_id'] == 'correlations':
                correlations_instance_id = instance['metadata']['id']
                break
        if correlations_instance_id is None:
            error_msg = 'ERROR: Failed to find a correlation monitor'
            logger.log_error(error_msg)
            raise Exception(error_msg)
        correlations_url = '{}/openscale/{}/v2/monitor_instances/{}/runs'.format(self._credentials['url'], self._credentials['data_mart_id'], correlations_instance_id)
        payload = {
                'triggered_by': 'user',
                'parameters': { 'max_number_of_days': '100' },
                'business_metric_context': { 'business_application_id': bkpiapp_id, 'metric_id': '', 'transaction_data_set_id': '', 'transaction_batch_id': '' }
            }
        start = time.time()
        response = requests.post(url=correlations_url, json=payload, headers=self.iam_headers, verify=self._verify)
        elapsed = time.time() - start
        self.timer('post bkpi_monitoring.run', elapsed)
        if response.status_code != 201:
            error_msg = 'ERROR: Failed to start bkpi monitoring run, rc: {} {}'.format(response.status_code, response.text)
            logger.log_error(error_msg)
            raise Exception(error_msg)
        correlation_run_id = response.json()['metadata']['id']
        return(correlations_instance_id, correlation_run_id)

    @retry(tries=5, delay=4, backoff=2)
    def _reliable_get_correlation_results(self, correlations_instance_id, correlation_run_id):
        results_url = '{}/openscale/{}/v2/monitor_instances/{}/runs/{}'.format(self._credentials['url'], self._credentials['data_mart_id'], correlations_instance_id, correlation_run_id)
        start = time.time()
        response = requests.get(url=results_url, headers=self.iam_headers, verify=self._verify)
        elapsed = time.time() - start
        self.timer('get bkpi_monitoring.run', elapsed)
        return (response)

    def trigger_bkpi_correlation_monitor(self, background_mode):
        if not self._use_bkpi:
            return
        if self._args.history < 7:
            logger.log_info('BKPI correlation monitor requires 7 days history - skipping')
            return
        logger.log_info('Trigger BKPI correlation monitor ...')
        try:
            (correlations_instance_id, correlation_run_id) = self._reliable_trigger_bkpi_correlation_monitor()
            logger.log_debug('BKPI correlation monitor running: instance_id {}, run_id {}'.format(correlations_instance_id, correlation_run_id))
            if background_mode:
                logger.log_info('BKPI correlation monitor triggered')
                return
            logger.log_info('BKPI correlation monitor running ...')
            check_completed = False
            for i in range(18):
                response = self._reliable_get_correlation_results(correlations_instance_id, correlation_run_id)
                if response.status_code != 200:
                    error_msg = 'ERROR: Failed to get bkpi correlation monitor run, rc: {} {}'.format(response.status_code, response.text)
                    raise Exception(error_msg)
                if response.json()['entity']['status']['state'] == 'error':
                    error_msg = 'ERROR: BKPI correlation monitor failed: {}'.format(response.text)
                    raise Exception(error_msg)
                if response.json()['entity']['status']['state'] != 'running':
                    check_completed = True
                    break
                logger.log_info('BKPI correlation monitor still running; wait 10 seconds and check again')
                time.sleep(10)
            if check_completed:
                logger.log_info('BKPI correlation monitor run completed')
            else:
                logger.log_info('BKPI correlation monitor run did not complete in 3 minutes, continuing')
        except Exception as e:
            message = 'WARNING: Problems occurred while running BKPI correlation monitor: {}'.format(str(e))
            logger.log_warning(message)
            self.metric_check_errors.append([self._model.name, 'bkpi-correlation-check', 'failed'])

    @retry(tries=5, delay=4, backoff=2)
    def _reliable_post_payloads(self, records):
        '''
        Retry the loading payloads so that if a specific day fails, just retry that day, rather than retry the whole sequence
        '''
        if not records:
            logger.log_debug('No payload history provided to load - skipping')
            return
        start = time.time()
        self._subscription.payload_logging.store(records=records, deployment_id=self._asset_details_dict['source_entry_metadata_guid'])
        elapsed = time.time() - start
        self.timer('subscription.payload_logging.store', elapsed)

    @retry(tries=5, delay=4, backoff=2)
    def _reliable_post_metrics(self, metric_type, records):
        '''
        Retry the loading metrics so that if a specific day fails, just retry that day, rather than retry the whole sequence
        '''
        if not records:
            logger.log_debug('No {} history provided to load - skipping'.format(metric_type))
            return
        metrics_url = '{0}/v1/data_marts/{1}/metrics'.format(self._credentials['url'], self._credentials['data_mart_id'])
        deployment_guid = self._asset_details_dict['source_entry_metadata_guid']
        record_json = []
        for record in records:
            # update historical manual labeling table reference to be correct
            if metric_type in ['fairness', 'debiased_fairness']:
                if 'manual_labelling_store' in record:
                    record['manual_labelling_store'] = 'Manual_Labeling_' + self._get_subscription_id()
            # new-style quality metrics have a slightly different json input than other metrics
            if metric_type == 'quality monitor':
                metric_label = 'monitor_definition_id'
                metric_type_value = 'quality'
            else:
                metric_label = 'metric_type'
                metric_type_value = metric_type
            record_json.append( {
                'binding_id': self.get_binding_id(),
                metric_label: metric_type_value,
                'timestamp': record['timestamp'],
                'subscription_id': self.get_subscription_id(),
                'value': record['value'],
                'deployment_id': deployment_guid
            })
        start = time.time()
        response = requests.post(metrics_url, json=record_json, headers=self.iam_headers, verify=self._verify)
        elapsed = time.time() - start
        self.timer('post data_mart {} metrics'.format(metric_type), elapsed)
        words = ['error', 'exception']
        if any(word in str(response.json()) for word in words):
            logger.log_warning('WARNING: while posting {} metrics: {}'.format(metric_type, str(response.json())))

    @retry(tries=5, delay=4, backoff=2)
    def _reliable_post_debiased_payloads(self, records):
        '''
        Retry the loading so that if a specific day fails, just retry that day, rather than retry the whole sequence
        '''
        if not records:
            logger.log_debug('No debiased payloads history provided to load - skipping')
            return
        debiased_payloads_url = '{0}/v1/data_marts/{1}/debiased_predictions'.format(self._credentials['url'], self._credentials['data_mart_id'])

        record_json = []
        for record in records:
            # update the record to include required metadata
            record['subscription_id'] = self.get_subscription_id()
            record_json.append(record)
        start = time.time()
        response = requests.post(debiased_payloads_url, json=record_json, headers=self.iam_headers, verify=self._verify)
        elapsed = time.time() - start
        self.timer('post data_mart debiased payloads history', elapsed)
        words = ['error', 'exception']
        if any(word in str(response.json()) for word in words):
            logger.log_warning('WARNING: while posting debiased payloads history: {}'.format(str(response.json())))

    @retry(tries=5, delay=4, backoff=2)
    def _reliable_post_manual_labeling(self, records):
        '''
        Retry the loading so that if a specific day fails, just retry that day, rather than retry the whole sequence
        '''
        if not records:
            logger.log_debug('No manual labeling history provided to load - skipping')
            return
        manual_labeling_url = '{0}/v1/data_marts/{1}/manual_labelings'.format(self._credentials['url'], self._credentials['data_mart_id'])
        deployment_guid = self._asset_details_dict['source_entry_metadata_guid']
        record_json = []
        for record in records:
            # update the record to include required metadata
            record['binding_id'] = self.get_binding_id()
            record['subscription_id'] = self.get_subscription_id()
            if 'asset_revision' in record: # if asset_revision is present, remove it
                del record['asset_revision']
            record['deployment_id'] = deployment_guid
            record_json.append(record)
        start = time.time()
        response = requests.post(manual_labeling_url, json=record_json, headers=self.iam_headers, verify=self._verify)
        elapsed = time.time() - start
        self.timer('post data_mart manual_labeling history', elapsed)
        words = ['error', 'exception']
        if any(word in str(response.json()) for word in words):
            logger.log_warning('WARNING: while posting manual labeling history: {}'.format(str(response.json())))

    @retry(tries=5, delay=4, backoff=2)
    def _reliable_store_bkpi_data_set(self, records, ds_type):
        if ds_type == 'transaction_batches':
            context = 'BKPI transaction batches id map history'
        elif ds_type == 'business_payload':
            context = 'BKPI payloads history'
        else:
            error_msg = 'ERROR: invalid bkpi data_set type: {}'.format(ds_type)
            logger.log_error(error_msg)
            raise Exception(error_msg)
        if not records:
            logger.log_debug('No {} provided to load - skipping'.format(context))
            return
        bkpiapp_id = self._model.metadata['bkpiapp_id']
        bkpi_data_sets_url = '{}/{}/v2/data_sets'.format(self._credentials['url'], self._credentials['data_mart_id'])
        start = time.time()
        response = requests.get(bkpi_data_sets_url, headers=self.iam_headers, verify=self._verify)
        elapsed = time.time() - start
        self.timer('get business data sets', elapsed)
        if response.status_code != 200:
            error_msg = 'ERROR: Failed to get business data sets, rc: {} {}'.format(response.status_code, response.text)
            logger.log_error(error_msg)
            raise Exception(error_msg)
        data_set_id = None
        for ds in response.json()['data_sets']:
            if ds['entity']['type'] == ds_type and ds['entity']['target']['target_type'] == 'business_application':
                if ds['entity']['target']['target_id'] == bkpiapp_id:
                    data_set_id = ds['metadata']['id']
        data_set_records_url = '{}/{}/v2/data_sets/{}/records'.format(self._credentials['url'], self._credentials['data_mart_id'], data_set_id)
        start = time.time()
        response = requests.post(data_set_records_url, json=records, headers=self.iam_headers, verify=self._verify)
        elapsed = time.time() - start
        self.timer('post {} history'.format(context), elapsed)
        if response.status_code != 202:
            error_msg = 'ERROR: Failed to store {}, rc: {} {}'.format(context, response.status_code, response.text)
            logger.log_error(error_msg)
            raise Exception(error_msg)

    @retry(tries=5, delay=4, backoff=2)
    def _reliable_store_bkpi_metrics(self, records):
        if not records:
            logger.log_debug('No business metrics history provided to load - skipping')
            return
        bkpiapp_id = self._model.metadata['bkpiapp_id']
        bkpi_apps_url = '{}/{}/v2/business_applications/{}'.format(self._credentials['url'], self._credentials['data_mart_id'], bkpiapp_id)
        start = time.time()
        response = requests.get(bkpi_apps_url, headers=self.iam_headers, verify=self._verify)
        elapsed = time.time() - start
        self.timer('get business application', elapsed)
        if response.status_code != 200:
            error_msg = 'ERROR: Failed to get business application, rc: {} {}'.format(response.status_code, response.text)
            logger.log_error(error_msg)
            raise Exception(error_msg)
        monitor_instance_id = response.json()['entity']['business_metrics_monitor_instance_id']
        measurements_url = '{}/openscale/{}/v2/monitor_instances/{}/measurements'.format(self._credentials['url'], self._credentials['data_mart_id'], monitor_instance_id)
        start = time.time()
        response = requests.post(measurements_url, json=records[0]['kpi'], headers=self.iam_headers, verify=self._verify)
        elapsed = time.time() - start
        self.timer('post business metrics history', elapsed)
        if response.status_code != 202:
            error_msg = 'ERROR: Failed to store BKPI history metrics, rc: {} {}'.format(response.status_code, response.text)
            logger.log_error(error_msg)
            raise Exception(error_msg)

    @retry(tries=5, delay=4, backoff=2)
    def _reliable_store_bkpi_drift_metrics(self, records):
        if not records:
            return
        bkpiapp_id = self._model.metadata['bkpiapp_id']
        monitors_url = '{}/openscale/{}/v2/monitor_instances'.format(self._credentials['url'], self._credentials['data_mart_id'])
        start = time.time()
        response = requests.get(url=monitors_url, headers=self.iam_headers, verify=self._verify)
        elapsed = time.time() - start
        self.timer('list all monitors', elapsed)
        if response.status_code != 200:
            error_msg = 'ERROR: Failed to list monitors, rc: {} {}'.format(response.status_code, response.text)
            logger.log_error(error_msg)
            raise Exception(error_msg)
        instances = response.json()['monitor_instances']
        drift_instance_id = None
        for instance in instances:
            if instance['entity']['monitor_definition_id'] == 'drift':
                drift_instance_id = instance['metadata']['id']
                break

        drift_records = records[0]['drift']
        for ix in range(len(drift_records)):
            drift_records[ix]['metrics'][0]['business_application_id'] = bkpiapp_id
        measurements_url = '{}/openscale/{}/v2/monitor_instances/{}/measurements'.format(self._credentials['url'], self._credentials['data_mart_id'], drift_instance_id)
        start = time.time()
        response = requests.post(measurements_url, json=drift_records, headers=self.iam_headers, verify=self._verify)
        elapsed = time.time() - start
        self.timer('post business drift metrics history', elapsed)
        if response.status_code != 202:
            error_msg = 'ERROR: Failed to store BKPI history drift metrics, rc: {} {}'.format(response.status_code, response.text)
            logger.log_error(error_msg)
            raise Exception(error_msg)

    @retry(tries=5, delay=4, backoff=2)
    def _reliable_store_quality_monitor_metrics(self, records):
        '''
        Retry the loading metrics so that if a specific day fails, just retry that day, rather than retry the whole sequence
        '''
        if not records:
            logger.log_debug('No quality_monitor history provided to load - skipping')
            return
        start = time.time()
        self._subscription.monitoring.store_measurements(monitor_uid='quality', measurements=records)
        elapsed = time.time() - start
        self.timer('post data_mart quality_monitor metrics', elapsed)

    @retry(tries=5, delay=4, backoff=2)
    def _reliable_generate_drift_metrics(self, start_time, end_time, windows=8): # eight 3-hour drift windows in 24 hours
        date_format = '%Y-%m-%dT%H:%M:%S.%fZ'
        start_time_param = start_time.strftime(date_format)
        end_time_param = end_time.strftime(date_format)

        drift_tasks_url = '{}/v1/data_marts/{}/service_bindings/{}/subscriptions/{}/drift_tasks'.format(self._credentials['url'], self._credentials['data_mart_id'], self.get_binding_id(), self.get_subscription_id())
        drift_tasks_url += '?start_time={}&end_time={}&compute_windows={}'.format(start_time_param, end_time_param, windows)
        # &execute_mode=synch

        start = time.time()
        requests.post(drift_tasks_url, json={}, headers=self.iam_headers, verify=self._verify)
        elapsed = time.time() - start
        self.timer('generate drift metrics', elapsed)

    @retry(tries=5, delay=4, backoff=2)
    def _reliable_post_drift_metrics(self, url, json, context):
        start = time.time()
        response = requests.post(url, json=json, headers=self.iam_headers, verify=self._verify)
        elapsed = time.time() - start
        self.timer('post {}'.format(context), elapsed)
        words = ['error', 'exception']
        if any(word in response.text for word in words):
            logger.log_warning('WARNING: while posting {}: rc={} {}'.format(context, response.status_code, response.text))
        return response

    def _post_drift_metrics(self, records, day):
        drift_measurement = records[0]['drift_measurement']
        drift_annotations = records[0]['drift_annotations']
        for i in range(0,len(drift_measurement)):
            window_start = self._model._get_score_time(day, hour=(i+1)*3).strftime('%Y-%m-%dT%H:%M:%SZ')  # first_payload_record_timestamp_in_window (oldest)
            window_end = self._model._get_score_time(day, hour=i*3).strftime('%Y-%m-%dT%H:%M:%SZ') # last_payload_record_timestamp_in_window (most recent)
            drift_measurement[i][0]['timestamp'] = window_end
            drift_measurement[i][0]['binding_id'] = self.get_binding_id()
            drift_measurement[i][0]['asset_id'] = self.get_asset_id()
            drift_measurement[i][0]['subscription_id'] = self.get_subscription_id()
            drift_measurement[i][0]['deployment_id'] = self.get_deployment_id()
            drift_measurement[i][0]['process'] = 'Drift run for subscription_{}'.format(self.get_subscription_id())
            drift_measurement[i][0]['sources'][0]['data']['start'] = window_start
            drift_measurement[i][0]['sources'][0]['data']['end'] = window_end
        for i in range(0,len(drift_measurement)):
            url = '{}/v1/data_marts/{}/measurements'.format(self._credentials['url'], self._credentials['data_mart_id'])
            response = self._reliable_post_drift_metrics(url, drift_measurement[i], 'drift measurement history')
            measurement_id = response.json()[0]['measurement_id']
            drift_annotations[i]['service_binding_id'] = self.get_binding_id()
            drift_annotations[i]['subscription_id'] = self.get_subscription_id()
            for j in range(0,len(drift_annotations[i]['annotations'])):
                annotation = drift_annotations[i]['annotations'][j]['annotation'].split('_') # [d]drift_<measurement_id>_cluster_<cluster>
                base = annotation[0]
                cluster = annotation[4]
                drift_annotations[i]['annotations'][j]['annotation'] = '{}_{}_cluster_{}'.format(base, measurement_id, cluster)
            url = '{}/v1/data_marts/{}/scoring_payloads_annotations'.format(self._credentials['url'], self._credentials['data_mart_id'])
            response = self._reliable_post_drift_metrics(url, drift_annotations[i], 'drift annotations history')

    @retry(tries=5, delay=4, backoff=2)
    def _reliable_update_bkpi_subscription(self):
        start = time.time()
        subscription_details = self._subscription.get_details()
        elapsed = time.time() - start
        self.timer('get subscription details', elapsed)

        url = '{}/{}/v2/subscriptions/{}'.format(self._credentials['url'], self._credentials['data_mart_id'], self.get_subscription_id())
        asset_properties = subscription_details['entity']['asset_properties']
        asset_properties['transaction_id_field'] = 'transaction_id'
        json=[{'op': 'replace', 'path': '/asset_properties', 'value': asset_properties}]

        start = time.time()
        response = requests.patch(url, json=json, headers=self.iam_headers, verify=self._verify)
        elapsed = time.time() - start
        if response.status_code != 200:
            error_msg = 'ERROR: Failed to patch subscription with BKPI transaction_id_field, rc: {} url: {} payload: {} response: {}'.format(response.status_code, url, json, response.text)
            logger.log_error(error_msg)
            raise Exception(error_msg)
        self.timer('update subscription with bkpi transaction_id', elapsed)

    def get_asset_details(self, name):
        logger.log_info('Retrieving assets ...')
        asset_details = self._client.data_mart.bindings.get_asset_details()
        asset_details_dict = {}
        for detail in asset_details:
            if name == detail['source_entry']['entity']['name']:
                if self._args.ml_engine_type is MLEngineType.SPSS:
                    asset_details_dict['id'] = detail['name']
                asset_details_dict['binding_uid'] = detail['binding_uid']
                asset_details_dict['source_uid'] = detail['source_uid']
                if self._args.ml_engine_type is not MLEngineType.WML: # For WML, the scoring URL is not in the asset
                    asset_details_dict['scoring_url'] = detail['source_entry']['entity']['scoring_endpoint']['url']
                asset_details_dict['source_entry_metadata_guid'] = detail['source_entry']['metadata']['guid']
                break
        if not 'source_uid' in asset_details_dict:
            error_msg = 'ERROR: Could not find a deployment with the name: {}'.format(name)
            logger.log_error(error_msg)
            raise Exception(error_msg)
        return asset_details_dict

    @retry(tries=5, delay=1, backoff=2)
    def _generate_one_explain(self, scoring_id, background_mode):
        cem = not self._args.explain_no_cem
        start = time.time()
        explain = self._subscription.explainability.run(scoring_id, background_mode=background_mode, cem=cem)
        end = time.time()
        return (start, end, explain)

    def _get_available_scores(self, max_explain_candidates):
        try:
            start = time.time()
            payload_table = self._subscription.payload_logging.get_table_content(format='pandas', limit=max_explain_candidates)
            end = time.time()
            scoring_ids = []
            for index, row in payload_table.iterrows():
                scoring_ids.append(row['scoring_id'])
            random.shuffle(scoring_ids)
            return (start, end, scoring_ids)
        except Exception as e:
            logger.log_warning('WARNING: Problems occurred while getting scoring ids for explanation: {}'.format(str(e)))
        return (None, None, None)

    @retry(tries=3, delay=4, backoff=2)
    def generate_explain_requests(self):
        # no explains for an MRM pre-production model
        if self._args.mrm and not self.is_mrm_prod:
            return
        num_explains = self._args.num_explains
        if num_explains < 1:
            return
        if not self._configure_explain:
            logger.log_info('Explainability not available for this model - skipping explain request(s)')
            return
        max_explain_candidates = self._args.max_explain_candidates
        if max_explain_candidates < 1:
            max_explain_candidates = num_explains
        pause = self._args.pause_between_explains
        logger.log_info('Finding up to {} available score(s) to explain...'.format(max_explain_candidates))
        (start, end, scoring_ids) = self._get_available_scores(max_explain_candidates)
        try:
            elapsed = end - start
            logger.log_info('Found {} available score(s) for explain'.format(len(scoring_ids)))
            self.timer('find {} available score(s) for explain'.format(len(scoring_ids)), elapsed)
            if num_explains > len(scoring_ids):
                num_explains = len(scoring_ids)
            if num_explains < 1:
                return

            if self._args.explain_start_sync:
                input('Press ENTER to start generating explain requests')

            if self._args.explain_no_cem:
                explain_mode = 'lime-only'
            else:
                explain_mode = 'lime and cem'
            logger.log_info('Generate {} explain request(s) ({}) ...'.format(num_explains, explain_mode))
            if pause > 0.0:
                logger.log_info('{:.3f} second pause between each explain request'.format(pause))
            background_mode = self._args.async_explains
            for i in range(num_explains):
                if pause > 0.0 and i > 0:
                    time.sleep(pause)
                scoring_id = scoring_ids[i]
                (start, end, explain) = self._generate_one_explain(scoring_id, background_mode)
                elapsed = end - start
                if not background_mode:
                    if not explain or (isinstance(explain, str) and 'errors' in explain.lower()):
                        self.metric_check_errors.append([self._model.name, 'explanation', 'failed'])
                    elif explain:
                        explain_success = explain['entity']['status']['lime_state'].lower() == 'finished'
                        if self._args.explain_no_cem:
                            explain_success = explain_success and explain['entity']['status']['cem_state'].lower() == 'finished'
                        if not explain_success:
                            self.metric_check_errors.append([self._model.name, 'explanation', 'failed'])
                explain_id = ''
                if explain:
                    explain_id = explain['metadata']['id']
                logger.log_timer('Request explain in {:.3f} seconds, scoring_id: {}, explain_id: {}'.format(elapsed, scoring_id, explain_id))
                self.timer('request explain', elapsed)
            logger.log_info('Generated {} explain request(s)'.format(num_explains))
        except Exception as e:
            if 'lime_state' in str(e):  # temporary fix until #13571 is fixed
                pass
            else:
                message = 'WARNING: Problems occurred while running explanation: {}'.format(str(e))
                logger.log_warning(message)
                self.metric_check_errors.append([self._model.name, 'explanation', 'failed'])
        self._reliable_count_datamart_rows('generated explains')
