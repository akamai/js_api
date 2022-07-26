import os
import sys
import mock
import pytest
import conf

sys.modules['src.models.JStap.classification.classifier'] = mock.MagicMock()
from src.models.model_jstap import ModelJstap


# THIS MOCK THE MODULE AT THE IMPORT. Patch works only when we execute the function, but in this case, we have an issue with
# argparse in the JSTAP project when run it with Pytest


@pytest.mark.skipif(not os.path.isdir(os.path.join(conf.SRC, 'models', 'JStap')), reason="JSTAP not downloaded")
def test_test_js():
    PDGS = os.path.join(conf.TEST_FOLDER, 'models', 'pdg_examples')
    pdg_list = [os.path.join(os.path.join(conf.TEST_FOLDER, 'models'), x) for x in os.listdir(PDGS)]
    ModelJstap().test_js(pdg_list, th=0.5)


@pytest.mark.skipif(not os.path.isdir(os.path.join(conf.SRC, 'models', 'JStap')), reason="JSTAP not downloaded")
def test_get_process_js():
    path = os.path.join(conf.TEST_FOLDER, 'models', '../content/akamai.com')
    limit = 3
    folder_path = ModelJstap.get_process_js(path, limit, ['inline', 'links'])
    assert folder_path == os.path.join(conf.TEST_FOLDER, 'models', '../content/akamai.com', 'to_process')


@pytest.mark.skipif(not os.path.isdir(os.path.join(conf.SRC, 'models', 'JStap')), reason="JSTAP not downloaded")
def test_create_js_dict():
    path = os.path.join(conf.TEST_FOLDER, 'models', '../content/akamai.com')
    _type_list = ['inline', 'links']
    js_dict = ModelJstap.create_js_dict(path, _type_list)
    assert len(js_dict['inline']) > 2
    assert len(js_dict['links']) > 2

