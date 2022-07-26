import os
import conf
from src.models.model import Model


def test_get_type():
    path = os.path.join(conf.TEST_FOLDER, 'models', '../content/akamai.com')
    type_list = Model.get_type(path)
    assert set(type_list) == {"inline", "links"}
