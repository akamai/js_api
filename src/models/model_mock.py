from .model import Model
from .mock_model.my_model import MyModel


class ModelMock(Model):
    NAME = 'Mock model'

    def __init__(self):
        super().__init__()

    @staticmethod
    def get_th():
        return 0.5

    def test_js(self, js_code):
        return MyModel.test_js()
