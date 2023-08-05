# coding=utf-8

from ibm_ai_openscale_cli.utility_classes.fastpath_logger import FastpathLogger
from ibm_ai_openscale_cli.utility_classes.utils import get_immediate_subdirectories, get_path
from ibm_ai_openscale_cli.credentials import Credentials
from ibm_ai_openscale_cli.enums import MLEngineType
from ibm_ai_openscale_cli.ml_engines.azure_machine_learning import AzureMachineLearningStudioEngine, AzureMachineLearningServiceEngine
from ibm_ai_openscale_cli.ml_engines.custom_machine_learning import CustomMachineLearningEngine
from ibm_ai_openscale_cli.ml_engines.sagemaker_machine_learning import SageMakerMachineLearningEngine
from ibm_ai_openscale_cli.ml_engines.spss_machine_learning import SPSSMachineLearningEngine
from ibm_ai_openscale_cli.ml_engines.watson_machine_learning import WatsonMachineLearningEngine
from ibm_ai_openscale_cli.models.model import Model
import os

logger = FastpathLogger(__name__)


class Ops:

    def __init__(self, args):
        self._args = args
        self._credentials = Credentials(args)
        self._ml_engine = None
        self._ml_engine_mrm = None

    def get_modeldata_instance(self, modelname, model_instance_num):
        model = Model(modelname, self._args, model_instance_num)
        return model

    def get_models_list(self):
        cwd = os.path.dirname(__file__)
        all_models_dir = get_path(cwd, [cwd, 'models'])
        modelnames_list = get_immediate_subdirectories(all_models_dir)
        if self._args.ml_engine_type is not MLEngineType.WML:
            for modelname in get_immediate_subdirectories(all_models_dir):
                model_dir = get_path(all_models_dir, [all_models_dir, modelname])
                all_engine_dirs = get_immediate_subdirectories(model_dir)
                if not self._args.ml_engine_type.name.lower() in all_engine_dirs:
                    modelnames_list.remove(modelname)
        else:
            for modelname in get_immediate_subdirectories(all_models_dir):
                wml_dir = get_path(all_models_dir, [all_models_dir, modelname, 'wml'])
                version_dirs = get_immediate_subdirectories(wml_dir)
                if self._args.v4 and ('v4' not in version_dirs):
                    modelnames_list.remove(modelname)
                elif (not self._args.v4) and ('v3' not in version_dirs):
                    modelnames_list.remove(modelname)
        modelnames_list.sort(key=str.lower)
        return modelnames_list

    def get_ml_engine_instance(self, openscale_client, is_mrm = False):
        logger.log_info('Using {}'.format(self._args.ml_engine_type.value))
        if is_mrm:
            if not self._ml_engine_mrm:
                ml_engine_credentials = self._credentials.get_ml_engine_credentials()
                self._ml_engine_mrm = WatsonMachineLearningEngine(ml_engine_credentials, openscale_client, self._args.v4, is_mrm)
            return self._ml_engine_mrm
        if not self._ml_engine:
            ml_engine_credentials = self._credentials.get_ml_engine_credentials()
            if self._args.ml_engine_type is MLEngineType.WML:
                self._ml_engine = WatsonMachineLearningEngine(ml_engine_credentials, openscale_client, self._args.v4)
            elif self._args.ml_engine_type is MLEngineType.AZUREMLSTUDIO:
                self._ml_engine = AzureMachineLearningStudioEngine()
            elif self._args.ml_engine_type is MLEngineType.AZUREMLSERVICE:
                self._ml_engine = AzureMachineLearningServiceEngine()
            elif self._args.ml_engine_type is MLEngineType.SPSS:
                self._ml_engine = SPSSMachineLearningEngine(ml_engine_credentials)
            elif self._args.ml_engine_type is MLEngineType.CUSTOM:
                self._ml_engine = CustomMachineLearningEngine(ml_engine_credentials)
            elif self._args.ml_engine_type is MLEngineType.SAGEMAKER:
                self._ml_engine = SageMakerMachineLearningEngine(ml_engine_credentials)
        return self._ml_engine
