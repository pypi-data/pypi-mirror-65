from .model_instance import ModelInstance


class Model():
    '''

    '''

    def __init__(self, client, name=None, modelId=None, modelConfig=None, createdAt=None, projectId=None, latestModelInstance={}):
        self.client = client
        self.id = modelId
        self.name = name
        self.model_id = modelId
        self.model_config = modelConfig
        self.created_at = createdAt
        self.project_id = projectId
        self.latest_model_instance = client._build_class(
            ModelInstance, latestModelInstance)

    def __repr__(self):
        return f"Model(name={repr(self.name)}, model_id={repr(self.model_id)}, model_config={repr(self.model_config)}, created_at={repr(self.created_at)}, project_id={repr(self.project_id)}, latest_model_instance={repr(self.latest_model_instance)})"

    def __eq__(self, other):
        return self.__class__ == other.__class__ and self.id == other.id

    def to_dict(self):
        return {'name': self.name, 'model_id': self.model_id, 'model_config': self.model_config, 'created_at': self.created_at, 'project_id': self.project_id, 'latest_model_instance': self.latest_model_instance.to_dict() if self.latest_model_instance else None}

    def create_deployment(self, name, description=None, deployment_config=None):
        return self.client.create_deployment(self.model_id, name, description, deployment_config)

    def cancel_training(self):
        return self.client.cancel_model_training(self.model_id)

    def delete(self):
        return self.client.delete_model(self.model_id)

    def refresh(self):
        self = self.describe()
        return self

    def describe(self):
        return self.client.describe_model(self.model_id)

    def get_metrics(self, model_instance_id=None):
        return self.client.get_model_metrics(self.model_id, model_instance_id)

    def list_instances(self):
        return self.client.list_model_instances(self.model_id)

    def retrain(self):
        return self.client.retrain_model(self.model_id)

    def wait_for_training(self, timeout=None):
        return self.client._poll(self, {'PENDING', 'TRAINING'}, delay=30, timeout=timeout)

    def wait_for_evaluation(self, timeout=None):
        return self.client._poll(self, {'PENDING', 'TRAINING', 'EVALUATING'}, delay=30, timeout=timeout)

    def get_status(self):
        return self.describe().latest_model_instance.status
