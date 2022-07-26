import sys
import mock

sys.modules['src.models.JStap.classification.classifier'] = mock.MagicMock()
from main import application


def test_test_url():
    response = application.test_client().post('/',
                                              data={'text': 'akamai.com',
                                                    'models': 'JStap_Pretrained_model_for_BlackHat_2022', 'api':
                                                        'true'})
    results = response.json


def test_get_model():
    response = application.test_client().get('/models')
    assert "Mock model" in response.json


def test_publicwwww():
    r = application.test_client().get(
        '/metadata/publicwww?domain=akamai.com&name=a88c11dd644107972dca9ff728081ac4decd70b6906485b4c9c3a8c877831465.js&type=inline')
    a = 1
