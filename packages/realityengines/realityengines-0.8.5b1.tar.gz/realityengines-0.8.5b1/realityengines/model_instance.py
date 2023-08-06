

class ModelInstance():
    '''

    '''

    def __init__(self, client, modelInstanceId=None, status=None, modelId=None, trainingStartedAt=None, trainingCompletedAt=None):
        self.client = client
        self.id = modelInstanceId
        self.model_instance_id = modelInstanceId
        self.status = status
        self.model_id = modelId
        self.training_started_at = trainingStartedAt
        self.training_completed_at = trainingCompletedAt

    def __repr__(self):
        return f"ModelInstance(model_instance_id={repr(self.model_instance_id)}, status={repr(self.status)}, model_id={repr(self.model_id)}, training_started_at={repr(self.training_started_at)}, training_completed_at={repr(self.training_completed_at)})"

    def __eq__(self, other):
        return self.__class__ == other.__class__ and self.id == other.id

    def to_dict(self):
        return {'model_instance_id': self.model_instance_id, 'status': self.status, 'model_id': self.model_id, 'training_started_at': self.training_started_at, 'training_completed_at': self.training_completed_at}
