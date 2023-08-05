# coding=utf-8
from ibm_ai_openscale_cli.utility_classes.fastpath_logger import FastpathLogger
from retry import retry
import time
from ibm_ai_openscale_cli.utility_classes.utils import jsonFileToDict
from watson_machine_learning_client import WatsonMachineLearningAPIClient

logger = FastpathLogger(__name__)


class WatsonMachineLearningEngine:

    def __init__(self, credentials, openscale_client, is_v4=False, is_mrm=False):
        start = time.time()
        self._client = WatsonMachineLearningAPIClient(dict(credentials))
        self._openscale_client = openscale_client
        self._is_v4 = is_v4
        self._space_id = None
        if is_v4:
            self._set_or_create_space_id(is_mrm)
        elapsed = time.time() - start
        self._openscale_client.timer('WML connect to WatsonMachineLearningAPIClient',elapsed)
        logger.log_info('Using Watson Machine Learning Python Client version: {}'.format(self._client.version))

    def get_native_client(self):
        return self._client

    def set_model(self, model):
        self._model_metadata = model.metadata

    @retry(tries=5, delay=4, backoff=2)
    def _reliable_create_space(self, space_name):
        logger.log_debug('Creating space {} ...'.format(space_name))
        space_props = {
            self._client.spaces.ConfigurationMetaNames.NAME: space_name
        }
        space = self._client.spaces.store(meta_props=space_props)
        start = time.time()
        space_id = self._client.spaces.get_uid(space)
        elapsed = time.time() - start
        self._openscale_client.timer('WML create space completed', elapsed)
        logger.log_debug('Succesfully created space {} (id: {})'.format(space_name, space_id))
        return space_id

    @retry(tries=5, delay=4, backoff=2)
    def _reliable_set_space(self, space_id, space_name):
        start = time.time()
        rc = self._client.set.default_space(space_id)
        elapsed = time.time() - start
        if not rc == 'SUCCESS':
            error_msg = 'ERROR: WML set.default_space failed for space {} (id: {}) {}'.format(space_name, space_id, rc)
            logger.log_error(error_msg)
            raise Exception(error_msg)
        self._space_id = space_id
        logger.log_info('Succesfully set space to {} (id: {})'.format(space_name, space_id))
        self._openscale_client.timer('WML set space completed', elapsed)

    def _set_or_create_space_id(self, is_mrm=False):
        space_name = 'openscale-fast-path'
        if is_mrm:
            space_name += '-preprod'
        logger.log_info('Checking for existing space "{}" ...'.format(space_name))
        spaces = self._client.spaces.get_details()
        space_id = None
        for space in spaces['resources']:
            if space_name == space['entity']['name']:
                space_id = space['metadata']['guid']
                break
        if not space_id:
            space_id = self._reliable_create_space(space_name=space_name)
        self._reliable_set_space(space_id, space_name)

    def _create_pipeline(self, model_name, pipeline_metadata_file):
        logger.log_info('Creating pipeline for model {} ...'.format(self._model_metadata['model_name']))
        pipeline_metadata = jsonFileToDict(pipeline_metadata_file)
        pipeline_props = {
            self._client.repository.DefinitionMetaNames.AUTHOR_NAME: pipeline_metadata['author']['name'],
            self._client.repository.DefinitionMetaNames.NAME: pipeline_metadata['name'],
            self._client.repository.DefinitionMetaNames.FRAMEWORK_NAME: pipeline_metadata['framework']['name'],
            self._client.repository.DefinitionMetaNames.FRAMEWORK_VERSION: pipeline_metadata['framework']['version'],
            self._client.repository.DefinitionMetaNames.RUNTIME_NAME: pipeline_metadata['framework']['runtimes'][0]['name'],
            self._client.repository.DefinitionMetaNames.RUNTIME_VERSION: pipeline_metadata['framework']['runtimes'][0]['version'],
            self._client.repository.DefinitionMetaNames.DESCRIPTION: pipeline_metadata['description'],
            self._client.repository.DefinitionMetaNames.TRAINING_DATA_REFERENCES: pipeline_metadata['training_data_reference']
        }
        start = time.time()
        self._client.repository.store_definition(self._model_metadata['pipeline_file'], meta_props=pipeline_props)
        elapsed = time.time() - start
        self._openscale_client.timer('WML repository.store_definition(pipeline)',elapsed)
        logger.log_info('Pipeline created successfully')

    def _delete_models(self, model_name):
        models = self._client.repository.get_model_details()
        found_model = False
        for model in models['resources']:
            model_guid = model['metadata']['guid']
            if model_name == model['entity']['name']:
                try:
                    found_model = True
                    # delete the model's deployments (if any) before the model
                    deployments = self._client.deployments.get_details()
                    for deployment in deployments['resources']:
                        deployment_guid = deployment['metadata']['guid']
                        deployment_name = deployment['entity']['name']
                        if self._is_v4:
                            deployment_asset_id = deployment['entity']['asset']['href'].split('/v4/models/')[1].split('?space_id')[0]
                        else:
                            deployment_asset_id = deployment['entity']['deployable_asset']['guid']
                        if deployment_asset_id == model_guid:
                            logger.log_info('Deleting deployment {} for model {} ...'.format(deployment_name, model_name))
                            self._reliable_delete_deployment(deployment_guid)
                            logger.log_info('Deployment deleted successfully'.format())

                    # delete the model
                    logger.log_info('Deleting model {} ...'.format(model_name))
                    self._reliable_delete_model(model_guid)
                    logger.log_info('Model deleted successfully')
                except Exception as e:
                    logger.log_warning('Error deleting WML deployment "{}": {}'.format(model_guid, str(e)))
        if not found_model:
            logger.log_info('No existing model found with name: {}'.format(model_name))

    @retry(tries=5, delay=4, backoff=2)
    def _reliable_delete_model(self, model_guid):
        all_models = self._client.repository.get_model_details()
        for model in all_models['resources']:
            if model_guid == model['metadata']['guid']:
                start = time.time()
                rc = self._client.repository.delete(model_guid)
                if not rc == 'SUCCESS':
                    error_msg = 'ERROR: WML repository.delete(model) delete failed (id: {}) {}'.format(model_guid, rc)
                    logger.log_error(error_msg)
                    raise Exception(error_msg)
                elapsed = time.time() - start
                self._openscale_client.timer('WML repository.delete(model)',elapsed)
                return
        logger.log_debug('Model {} not found, nothing to delete'.format(model_guid))

    def _create_model(self, model_name, model_metadata_file):
        logger.log_info('Creating new model {} ...'.format(model_name))
        metadata = jsonFileToDict(model_metadata_file)
        model_props = {
            self._client.repository.ModelMetaNames.NAME: model_name
        }
        if self._is_v4:
            model_props[self._client.repository.ModelMetaNames.TYPE] = metadata['type']
            model_props[self._client.repository.ModelMetaNames.RUNTIME_UID] = metadata['runtime_uid']
            if 'training_data_references' in metadata:
                model_props[self._client.repository.ModelMetaNames.TRAINING_DATA_REFERENCES] = metadata['training_data_references']
            if 'input_data_schema' in metadata:
                model_props[self._client.repository.ModelMetaNames.INPUT_DATA_SCHEMA] = metadata['input_data_schema']
            if 'output_data_schema' in metadata:
                model_props[self._client.repository.ModelMetaNames.OUTPUT_DATA_SCHEMA] = metadata['output_data_schema']
        else:
            model_props[self._client.repository.ModelMetaNames.FRAMEWORK_NAME] = metadata['framework']['name']
            model_props[self._client.repository.ModelMetaNames.FRAMEWORK_VERSION] = metadata['framework']['version']
            if 'runtimes' in metadata['framework']:
                model_props[self._client.repository.ModelMetaNames.RUNTIME_NAME] = metadata['framework']['runtimes'][0]['name']
                model_props[self._client.repository.ModelMetaNames.RUNTIME_VERSION] = metadata['framework']['runtimes'][0]['version']
            if 'training_data_schema' in metadata:
                model_props[self._client.repository.ModelMetaNames.TRAINING_DATA_SCHEMA] = metadata['training_data_schema']
            if 'evaluation' in metadata:
                model_props[self._client.repository.ModelMetaNames.EVALUATION_METHOD] = metadata['evaluation']['method']
                model_props[self._client.repository.ModelMetaNames.EVALUATION_METRICS] = metadata['evaluation']['metrics']
            if 'training_data_reference' in metadata:
                model_props[self._client.repository.ModelMetaNames.TRAINING_DATA_REFERENCE] = metadata['training_data_reference'][0]
            if 'libraries' in metadata['framework']:
                model_props[self._client.repository.ModelMetaNames.FRAMEWORK_LIBRARIES] = metadata['framework']['libraries']
            if 'label_column' in metadata:
                model_props[self._client.repository.ModelMetaNames.LABEL_FIELD] = metadata['label_column']
            if 'input_data_schema' in metadata:
                model_props[self._client.repository.ModelMetaNames.INPUT_DATA_SCHEMA] = metadata['input_data_schema']
        if 'output_data_schema' in metadata:
            model_props[self._client.repository.ModelMetaNames.OUTPUT_DATA_SCHEMA] = metadata['output_data_schema']
        model_details = self._reliable_create_model(self._model_metadata['model_file'], model_props)
        model_guid = self._client.repository.get_model_uid(model_details)
        logger.log_info('Created new model {} successfully (guid: {})'.format(model_name, model_guid))
        return metadata, model_guid

    @retry(tries=5, delay=4, backoff=2)
    def _reliable_create_model(self, model_file, model_props):
        start = time.time()
        model_details = self._client.repository.store_model(model_file, model_props)
        elapsed = time.time() - start
        self._openscale_client.timer('WML repository.store_model', elapsed)
        return model_details

    def _list_all_models(self):
        logger.log_info('Listing all models ...')
        start = time.time()
        self._client.repository.list_models()
        elapsed = time.time() - start
        self._openscale_client.timer('WML repository.list_models', elapsed)
        logger.log_info('Models listed successfully')

    def _deploy_model(self, model_guid, deployment_name, deployment_description):
        logger.log_info('Creating new deployment {} ...'.format(deployment_name))
        elapsed_time, deployment_details = self._reliable_deploy_model(model_guid, deployment_name, deployment_description)
        deployment_guid = deployment_details['metadata']['guid']
        logger.log_info('Created new deployment {} (guid: {}) successfully in {} seconds'.format(deployment_name, deployment_guid, round(elapsed_time, 2)))
        return deployment_guid

    @retry(tries=5, delay=4, backoff=2)
    def _reliable_deploy_model(self, model_guid, deployment_name, deployment_description):
        start = time.time()
        deployment_details = None
        if self._is_v4:
            meta_props = {
                self._client.deployments.ConfigurationMetaNames.NAME: deployment_name,
                self._client.deployments.ConfigurationMetaNames.DESCRIPTION: deployment_description,
                self._client.deployments.ConfigurationMetaNames.ONLINE: {},
            }
            deployment_details = self._client.deployments.create(artifact_uid=model_guid, meta_props=meta_props)
        else:
            deployment_details = self._client.deployments.create(artifact_uid=model_guid, name=deployment_name, description=deployment_description)
        elapsed = time.time() - start
        self._openscale_client.timer('WML deployments.create', elapsed)
        return elapsed, deployment_details

    @retry(tries=5, delay=4, backoff=2)
    def _reliable_delete_deployment(self, deployment_guid):
        all_deployments = self._client.deployments.get_details()
        for deployment in all_deployments['resources']:
            if deployment_guid == deployment['metadata']['guid']:
                start = time.time()
                rc = self._client.deployments.delete(deployment_guid)
                if not rc == 'SUCCESS':
                    error_msg = 'ERROR: WML deployments.delete failed (id: {}) {}'.format(deployment_guid, rc)
                    logger.log_error(error_msg)
                    raise Exception(error_msg)
                elapsed = time.time() - start
                self._openscale_client.timer('WML deployments.delete',elapsed)
                return
        logger.log_debug('Deployment {} not found, nothing to delete'.format(deployment_guid))

    def _list_all_deployments(self):
        start = time.time()
        deployment_details = self._client.deployments.get_details()
        elapsed = time.time() - start
        self._openscale_client.timer('WML deployments.get_details',elapsed)
        for details in deployment_details['resources']:
            logger.log_info('Name: {}, GUID: {}'.format(details['entity']['name'], details['metadata']['guid']))

    def create_model_and_deploy(self):
        model_name = self._model_metadata['model_name']
        deployment_name = self._model_metadata['deployment_name']

        # delete existing model and its deployments
        logger.log_info('Checking for models with the name {}'.format(model_name))
        self._delete_models(model_name)

        # create new model and deployment
        # self._create_pipeline(model_name, self._model_metadata['pipeline_metadata_file'])
        model_metadata_dict, model_guid = self._create_model(model_name, self._model_metadata['model_metadata_file'])
        deployment_guid = self._deploy_model(model_guid, deployment_name, self._model_metadata['deployment_description'])

        model_deployment_dict = {
            'model_name': model_name,
            'source_uid': model_guid,
            'model_metadata_dict': model_metadata_dict,
            'deployment_name': deployment_name,
            'source_entry_metadata_guid': deployment_guid,
            'binding_uid': self._client.service_instance.get_instance_id()
        }

        return model_deployment_dict

    def model_cleanup(self):
        model_name = self._model_metadata['model_name']
        self._delete_models(model_name)

    # returns info for first-found deployment with the specified name, if there are multiple
    def get_existing_deployment(self, deployment_name):
        model_name = self._model_metadata['model_name']
        model_guid = None
        deployment_guid = None
        model_metadata_dict = None
        logger.log_info('Use existing model named: {}'.format(model_name))
        models = self._client.repository.get_model_details()
        for this_model in models['resources']:
            this_model_name = this_model['entity']['name']
            guid = this_model['metadata']['guid']
            mata_data = this_model['metadata']
            if model_name == this_model_name:
                model_guid = guid
                model_metadata_dict = mata_data
                break
        depl_details = self._client.deployments.get_details()
        for details in depl_details['resources']:
            dep_guid = details['metadata']['guid']
            dep_name = details['entity']['name']
            if dep_name == deployment_name:
                deployment_guid = dep_guid
                break

        logger.log_info('Model Name: {}  Model GUID: {}'.format(model_name, model_guid))
        logger.log_info('Deployment Name: {}  Deployment GUID: {}'.format(deployment_name, deployment_guid))

        model_deployment_dict = {
            'model_metadata_dict': model_metadata_dict,
            'source_uid': model_guid,
            'source_entry_metadata_guid': deployment_guid,
            'binding_uid': self._client.service_instance.get_instance_id()
        }

        return model_deployment_dict

    def score(self, deployment_uid, values, fields=None):
        if fields:
            scoring_input = {
                "fields": fields,
                "values": values
            }
        else:
            scoring_input = {
                "values": values
            }
        payload = {
            self._client.deployments.ScoringMetaNames.INPUT_DATA: [scoring_input]
        }
        record = self._client.deployments.score(deployment_uid, payload)
        return record
