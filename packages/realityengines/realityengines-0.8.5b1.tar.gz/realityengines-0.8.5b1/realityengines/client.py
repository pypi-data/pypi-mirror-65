import inspect
import io
import logging
import requests
import time

from packaging import version

from .api_key import ApiKey
from .batch_prediction import BatchPrediction
from .bucket_verification import BucketVerification
from .schema import Schema
from .dataset import Dataset
from .dataset_instance import DatasetInstance
from .dataset_upload import DatasetUpload
from .deployment import Deployment
from .deployment_auth_token import DeploymentAuthToken
from .model import Model
from .model_instance import ModelInstance
from .project import Project
from .project_dataset import ProjectDataset
from .project_validation import ProjectValidation
from .training_config_options import TrainingConfigOptions
from .use_case import UseCase
from .use_case_requirements import UseCaseRequirements


class ApiException(Exception):
    def __init__(self, message, http_status, exception=None):
        self.message = message
        self.http_status = http_status
        self.exception = exception or 'ApiException'

    def __str__(self):
        return f'{self.exception}({self.http_status}): {self.message}'


class ReClient():
    client_version = '0.8.5'

    def __init__(self, api_key=None, server='https://realityengines.ai'):
        self.api_key = api_key
        self.server = server
        # Connection and version check
        try:
            documentation = self._call_api('documentation', 'GET')
            web_version = documentation['version']
            if version.parse(web_version) > version.parse(self.client_version):
                logging.warning(
                    'A new version of the RealityEngines.AI library is available')
                logging.warning(
                    f'Current Version: {version} -> New Version: {web_version}')
            if api_key is not None:
                self.user = self._call_api('getUser', 'GET')
        except Exception:
            logging.error('Failed to connect to RealityEngines.AI server')
            raise

    def _call_api(
            self, action, method, query_params=None,
            body=None, files=None, parse_type=None):
        headers = {'apiKey': self.api_key,
                   'clientVersion': self.client_version, 'client': 'python'}
        url = self.server + '/api/v0/' + action

        response = self._request(
            url, method, query_params=query_params, headers=headers, body=body, files=files)
        result = None
        success = False
        error_message = None
        error_type = None
        try:
            json_data = response.json()
            success = json_data['success']
            error_message = json_data.get('error')
            error_type = json_data.get('errorType')
            result = json_data.get('result')
            if success and parse_type:
                result = self._build_class(parse_type, result)
        except Exception:
            error_message = response.text
        if not success:
            if response.status_code > 502 and response.status_code not in (501, 503):
                error_message = 'Internal Server Error, please contact dev@realityengines.ai for support'
            raise ApiException(error_message, response.status_code, error_type)
        return result

    def _build_class(self, return_class, values):
        if not values:
            return None
        if isinstance(values, list):
            return [self._build_class(return_class, val) for val in values if val is not None]
        type_inputs = inspect.signature(return_class.__init__).parameters
        return return_class(self, **{key: val for key, val in values.items() if key in type_inputs})

    def _request(self, url, method, query_params=None, headers=None,
                 body=None, files=None):
        if method == 'GET':
            return requests.get(url, params=query_params, headers=headers)
        elif method == 'POST':
            return requests.post(url, params=query_params, json=body, headers=headers, files=files, timeout=90)
        elif method == 'PUT':
            return requests.put(url, params=query_params, data=body, headers=headers, files=files, timeout=90)
        elif method == 'PATCH':
            return requests.patch(url, params=query_params, data=body, headers=headers, timeout=90)
        elif method == 'DELETE':
            return requests.delete(url, params=query_params, data=body, headers=headers)
        else:
            raise ValueError(
                'HTTP method must be `GET`, `POST`, `PATCH`, `PUT` or `DELETE`'
            )

    def _poll(self, obj, wait_states, delay=5, timeout=300):
        start_time = time.time()
        while obj.get_status() in wait_states:
            if timeout and time.time() - start_time > timeout:
                raise TimeoutError(f'Maximum wait time of {timeout}s exceeded')
            time.sleep(delay)
        return obj.describe()

    def describe_use_case_requirements(self, use_case: str):
        '''    '''
        return self._call_api('describeUseCaseRequirements', 'GET', query_params={'useCase': use_case}, parse_type=UseCaseRequirements)

    def list_use_cases(self):
        '''    '''
        return self._call_api('listUseCases', 'GET', query_params={}, parse_type=UseCase)

    def add_user_to_organization(self, email: str):
        '''Send an invite to a specified email.    '''
        return self._call_api('addUserToOrganization', 'POST', body={'email': email})

    def list_organization_users(self):
        '''List all of the users in your organization and the account information associated with each user.    '''
        return self._call_api('listOrganizationUsers', 'GET', query_params={})

    def remove_user_from_organization(self, email: str):
        '''Remove a specified user from the organization.    '''
        return self._call_api('removeUserFromOrganization', 'DELETE', query_params={'email': email})

    def set_user_as_admin(self, email: str):
        '''Set a specified user as an administrator for your organization. You can use the List Organization Users API to see the email for each user in your organization.    '''
        return self._call_api('setUserAsAdmin', 'POST', body={'email': email})

    def delete_api_key(self, api_key_id: str):
        '''Delete a specified API Key.    '''
        return self._call_api('deleteApiKey', 'DELETE', query_params={'apiKeyId': api_key_id})

    def get_user(self):
        '''Get the current User's info    '''
        return self._call_api('getUser', 'GET', query_params={})

    def list_api_keys(self):
        '''List all of the API keys created by the current in the user's Organization    '''
        return self._call_api('listApiKeys', 'GET', query_params={}, parse_type=ApiKey)

    def create_project(self, name: str, use_case: str):
        '''Create a project with your specified project name and use case.    '''
        return self._call_api('createProject', 'GET', query_params={'name': name, 'useCase': use_case}, parse_type=Project)

    def delete_project(self, project_id: str):
        '''Deletes a specified project from your organization.    '''
        return self._call_api('deleteProject', 'DELETE', query_params={'projectId': project_id})

    def describe_project(self, project_id: str):
        '''Retrieves a full description of the specified project.    '''
        return self._call_api('describeProject', 'GET', query_params={'projectId': project_id}, parse_type=Project)

    def get_schema(self, project_id: str, dataset_id: str):
        '''    '''
        return self._call_api('getSchema', 'GET', query_params={'projectId': project_id, 'datasetId': dataset_id}, parse_type=Schema)

    def list_project_datasets(self, project_id: str):
        '''Retrieves all datasets attached to the specified project id.    '''
        return self._call_api('listProjectDatasets', 'GET', query_params={'projectId': project_id}, parse_type=ProjectDataset)

    def list_projects(self):
        '''Retrieves a list of all projects in your organization.    '''
        return self._call_api('listProjects', 'GET', query_params={}, parse_type=Project)

    def remove_column_mapping(self, project_id: str, dataset_id: str, column: str):
        '''Delete a column mapping from a dataset attached to your project.    '''
        return self._call_api('removeColumnMapping', 'DELETE', query_params={'projectId': project_id, 'datasetId': dataset_id, 'column': column}, parse_type=Schema)

    def rename_project(self, project_id: str, name: str):
        '''Rename the project    '''
        return self._call_api('renameProject', 'PATCH', body={'projectId': project_id, 'name': name})

    def set_column_mapping(self, project_id: str, dataset_id: str, column: str, column_mapping: str):
        '''Set a dataset's column mapping    '''
        return self._call_api('setColumnMapping', 'POST', body={'projectId': project_id, 'datasetId': dataset_id, 'column': column, 'columnMapping': column_mapping}, parse_type=Schema)

    def set_column_data_type(self, project_id: str, dataset_id: str, column: str, data_type: str):
        '''Set a project dataset column data type    '''
        return self._call_api('setColumnDataType', 'POST', body={'projectId': project_id, 'datasetId': dataset_id, 'column': column, 'dataType': data_type}, parse_type=Schema)

    def validate_project(self, project_id: str):
        '''    '''
        return self._call_api('validateProject', 'GET', query_params={'projectId': project_id}, parse_type=ProjectValidation)

    def add_aws_role(self, bucket: str, role_arn: str):
        '''    '''
        return self._call_api('addAWSRole', 'POST', body={'bucket': bucket, 'roleArn': role_arn})

    def get_data_connector_verification(self, bucket: str, write_permission: bool = False):
        '''    '''
        return self._call_api('getDataConnectorVerification', 'GET', query_params={'bucket': bucket, 'writePermission': write_permission})

    def list_data_connector_verifications(self):
        '''    '''
        return self._call_api('listDataConnectorVerifications', 'GET', query_params={}, parse_type=BucketVerification)

    def remove_data_connector(self, bucket: str):
        '''    '''
        return self._call_api('removeDataConnector', 'DELETE', query_params={'bucket': bucket})

    def verify_data_connector(self, bucket: str):
        '''    '''
        return self._call_api('verifyDataConnector', 'POST', body={'bucket': bucket})

    def attach_dataset_to_project(self, dataset_id: str, project_id: str, dataset_type: str):
        '''Adds a dataset to an existing project    '''
        return self._call_api('attachDatasetToProject', 'POST', body={'datasetId': dataset_id, 'projectId': project_id, 'datasetType': dataset_type}, parse_type=Schema)

    def delete_dataset(self, dataset_id: str):
        '''    '''
        return self._call_api('deleteDataset', 'DELETE', query_params={'datasetId': dataset_id})

    def describe_dataset(self, dataset_id: str):
        '''    '''
        return self._call_api('describeDataset', 'GET', query_params={'datasetId': dataset_id}, parse_type=Dataset)

    def create_dataset(self, name: str, location: str, file_format: str = None, project_id: str = None, dataset_type: str = None):
        '''    '''
        return self._call_api('createDataset', 'POST', body={'name': name, 'location': location, 'fileFormat': file_format, 'projectId': project_id, 'datasetType': dataset_type}, parse_type=Dataset)

    def create_dataset_instance(self, dataset_id: str, location: str = None, file_format: str = None):
        '''    '''
        return self._call_api('createDatasetInstance', 'POST', body={'datasetId': dataset_id, 'location': location, 'fileFormat': file_format}, parse_type=DatasetInstance)

    def list_datasets(self):
        '''    '''
        return self._call_api('listDatasets', 'GET', query_params={}, parse_type=Dataset)

    def list_dataset_instances(self, dataset_id: str = None):
        '''    '''
        return self._call_api('listDatasetInstances', 'GET', query_params={'datasetId': dataset_id}, parse_type=DatasetInstance)

    def create_dataset_from_local_file(self, name: str, file_format: str = None, project_id: str = None, dataset_type: str = None):
        '''    '''
        return self._call_api('createDatasetFromLocalFile', 'POST', body={'name': name, 'fileFormat': file_format, 'projectId': project_id, 'datasetType': dataset_type}, parse_type=DatasetUpload)

    def create_dataset_instance_from_local_file(self, dataset_id: str, file_format: str = None):
        '''    '''
        return self._call_api('createDatasetInstanceFromLocalFile', 'POST', body={'datasetId': dataset_id, 'fileFormat': file_format}, parse_type=DatasetUpload)

    def remove_dataset_from_project(self, dataset_id: str, project_id: str):
        '''    '''
        return self._call_api('removeDatasetFromProject', 'POST', body={'datasetId': dataset_id, 'projectId': project_id})

    def create_deployment(self, model_id: str, name: str, description: str = None, deployment_config: dict = None):
        '''    '''
        return self._call_api('createDeployment', 'POST', body={'modelId': model_id, 'name': name, 'description': description, 'deploymentConfig': deployment_config}, parse_type=Deployment)

    def create_deployment_token(self, project_id: str):
        '''    '''
        return self._call_api('createDeploymentToken', 'POST', body={'projectId': project_id})

    def delete_deployment(self, deployment_id: str):
        '''    '''
        return self._call_api('deleteDeployment', 'DELETE', query_params={'deploymentId': deployment_id})

    def delete_deployment_token(self, deployment_token: str):
        '''    '''
        return self._call_api('deleteDeploymentToken', 'DELETE', query_params={'deploymentToken': deployment_token})

    def describe_deployment(self, deployment_id: str):
        '''    '''
        return self._call_api('describeDeployment', 'GET', query_params={'deploymentId': deployment_id}, parse_type=Deployment)

    def list_deployments(self, project_id: str):
        '''    '''
        return self._call_api('listDeployments', 'GET', query_params={'projectId': project_id}, parse_type=Deployment)

    def list_deployment_tokens(self, project_id: str):
        '''    '''
        return self._call_api('listDeploymentTokens', 'GET', query_params={'projectId': project_id}, parse_type=DeploymentAuthToken)

    def start_deployment(self, deployment_id: str):
        '''    '''
        return self._call_api('startDeployment', 'GET', query_params={'deploymentId': deployment_id})

    def stop_deployment(self, deployment_id: str):
        '''    '''
        return self._call_api('stopDeployment', 'GET', query_params={'deploymentId': deployment_id})

    def update_deployment(self, deployment_id: str, name: str = None, description: str = None):
        '''    '''
        return self._call_api('updateDeployment', 'PATCH', body={'deploymentId': deployment_id, 'name': name, 'description': description})

    def complete_upload(self, dataset_upload_id: str):
        '''    '''
        return self._call_api('completeUpload', 'POST', body={'datasetUploadId': dataset_upload_id}, parse_type=Dataset)

    def describe_upload(self, dataset_upload_id: str):
        '''    '''
        return self._call_api('describeUpload', 'GET', query_params={'datasetUploadId': dataset_upload_id}, parse_type=DatasetUpload)

    def list_uploads(self):
        '''    '''
        return self._call_api('listUploads', 'GET', query_params={}, parse_type=DatasetUpload)

    def upload_file_part(self, dataset_upload_id: str, part_number: int, part_data: io.TextIOBase):
        '''    Upload a dataset part up to 5GB in size for a total file size of up to 5TB    '''
        return self._call_api('uploadFilePart', 'POST', query_params={'datasetUploadId': dataset_upload_id, 'partNumber': part_number}, files={'partData': part_data})

    def cancel_model_training(self, model_id: str):
        '''    '''
        return self._call_api('cancelModelTraining', 'DELETE', query_params={'modelId': model_id})

    def train_model(self, project_id: str, name: None = None, training_config: dict = {}):
        '''    '''
        return self._call_api('trainModel', 'POST', body={'projectId': project_id, 'name': name, 'trainingConfig': training_config}, parse_type=Model)

    def delete_model(self, model_id: str):
        '''    '''
        return self._call_api('deleteModel', 'DELETE', query_params={'modelId': model_id})

    def describe_model(self, model_id: str):
        '''    '''
        return self._call_api('describeModel', 'GET', query_params={'modelId': model_id}, parse_type=Model)

    def get_model_metrics(self, model_id: str = None, model_instance_id: str = None):
        '''    '''
        return self._call_api('getModelMetrics', 'GET', query_params={'modelId': model_id, 'modelInstanceId': model_instance_id})

    def get_training_config_options(self, project_id: str):
        '''    '''
        return self._call_api('getTrainingConfigOptions', 'GET', query_params={'projectId': project_id}, parse_type=TrainingConfigOptions)

    def list_models(self, project_id: str):
        '''    '''
        return self._call_api('listModels', 'GET', query_params={'projectId': project_id}, parse_type=Model)

    def list_model_instances(self, model_id: str):
        '''    '''
        return self._call_api('listModelInstances', 'GET', query_params={'modelId': model_id}, parse_type=ModelInstance)

    def retrain_model(self, model_id: str):
        '''    '''
        return self._call_api('retrainModel', 'POST', body={'modelId': model_id}, parse_type=Model)

    def predict(self, deployment_token: str, deployment_id: str, query_data: dict = {}, **kwargs):
        '''    '''
        return self._call_api('predict', 'POST', body={'deploymentToken': deployment_token, 'deploymentId': deployment_id, 'queryData': query_data, **kwargs})

    def predict_lead(self, deployment_token: str, deployment_id: str, query_data: dict):
        '''    '''
        return self._call_api('predictLead', 'POST', body={'deploymentToken': deployment_token, 'deploymentId': deployment_id, 'queryData': query_data})

    def predict_churn(self, deployment_token: str, deployment_id: str, query_data: dict):
        '''    '''
        return self._call_api('predictChurn', 'POST', body={'deploymentToken': deployment_token, 'deploymentId': deployment_id, 'queryData': query_data})

    def predict_takeover(self, deployment_token: str, deployment_id: str, query_data: dict):
        '''    '''
        return self._call_api('predictTakeover', 'POST', body={'deploymentToken': deployment_token, 'deploymentId': deployment_id, 'queryData': query_data})

    def predict_fraud(self, deployment_token: str, deployment_id: str, query_data: dict):
        '''    '''
        return self._call_api('predictFraud', 'POST', body={'deploymentToken': deployment_token, 'deploymentId': deployment_id, 'queryData': query_data})

    def get_forecast(self, deployment_token: str, deployment_id: str, query_data: dict, future_data: dict = None):
        '''    '''
        return self._call_api('getForecast', 'POST', body={'deploymentToken': deployment_token, 'deploymentId': deployment_id, 'queryData': query_data, 'futureData': future_data})

    def get_recommendations(self, deployment_token: str, deployment_id: str, query_data: dict, num_items: int = 50, page: int = 1, include_filters: list = [], exclude_filters: list = []):
        '''    '''
        return self._call_api('getRecommendations', 'POST', body={'deploymentToken': deployment_token, 'deploymentId': deployment_id, 'queryData': query_data, 'numItems': num_items, 'page': page, 'includeFilters': include_filters, 'excludeFilters': exclude_filters})

    def get_personalized_ranking(self, deployment_token: str, deployment_id: str, query_data: dict):
        '''    '''
        return self._call_api('getPersonalizedRanking', 'POST', body={'deploymentToken': deployment_token, 'deploymentId': deployment_id, 'queryData': query_data})

    def get_ranked_items(self, deployment_token: str, deployment_id: str, query_data: dict):
        '''    '''
        return self._call_api('getRankedItems', 'POST', body={'deploymentToken': deployment_token, 'deploymentId': deployment_id, 'queryData': query_data})

    def get_related_items(self, deployment_token: str, deployment_id: str, query_data: dict, page: int = 1, include_filters: list = [], exclude_filters: list = []):
        '''    '''
        return self._call_api('getRelatedItems', 'POST', body={'deploymentToken': deployment_token, 'deploymentId': deployment_id, 'queryData': query_data, 'page': page, 'includeFilters': include_filters, 'excludeFilters': exclude_filters})

    def batch_predict(self, deployment_id: str, input_location: str = None, output_location: str = None, name: str = None):
        '''    '''
        return self._call_api('batchPredict', 'POST', body={'deploymentId': deployment_id, 'inputLocation': input_location, 'outputLocation': output_location, 'name': name}, parse_type=BatchPrediction)

    def describe_batch_prediction(self, batch_prediction_id: str):
        '''    '''
        return self._call_api('describeBatchPrediction', 'GET', query_params={'batchPredictionId': batch_prediction_id}, parse_type=BatchPrediction)

    def list_batch_predictions(self, deployment_id: str):
        '''    '''
        return self._call_api('listBatchPredictions', 'GET', query_params={'deploymentId': deployment_id}, parse_type=BatchPrediction)

    def record(self, auth_token: str, deployment_id: str, interactions: list):
        '''    '''
        return self._call_api('record', 'POST', body={'authToken': auth_token, 'deploymentId': deployment_id, 'interactions': interactions})
