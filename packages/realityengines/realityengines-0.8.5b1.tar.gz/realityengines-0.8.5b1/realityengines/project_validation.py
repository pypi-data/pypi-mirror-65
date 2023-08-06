

class ProjectValidation():
    '''

    '''

    def __init__(self, client, valid=None, datasetErrors=None):
        self.client = client
        self.id = valid
        self.valid = valid
        self.dataset_errors = datasetErrors

    def __repr__(self):
        return f"ProjectValidation(valid={repr(self.valid)}, dataset_errors={repr(self.dataset_errors)})"

    def __eq__(self, other):
        return self.__class__ == other.__class__ and self.id == other.id

    def to_dict(self):
        return {'valid': self.valid, 'dataset_errors': self.dataset_errors}
