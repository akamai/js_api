from src.models.model_jstap import ModelJstap
from src.models.model_mock import ModelMock

MODELS = [ModelJstap, ModelMock]


class UseCaseModel(object):
    """
    Use case for model. Modify this file to add your model
    """
    def __init__(self):
        self.current_model = None

    @staticmethod
    def get_model_list():
        return [model.NAME for model in MODELS]

    @staticmethod
    def get_model(name):
        """
        Plug your model here
        Args:
            name: model name

        Returns: Model object

        """
        if name == ModelJstap.NAME:
            return ModelJstap
        elif name == ModelMock.NAME:
            return ModelMock
        return None

