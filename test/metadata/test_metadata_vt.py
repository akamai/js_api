import mock
import os

import conf
from src.metadata.metadata_vt import MetadataVT

results = {'Bkav': {'category': 'undetected', 'engine_name': 'Bkav', 'engine_version': '1.3.0.9899', 'result': None,
                    'method': 'blacklist', 'engine_update': '20220711'},
           'Lionic': {'category': 'malicious', 'engine_name': 'Lionic', 'engine_version': '7.5',
                      'result': 'Trojan.JS.Agent.4!c',
                      'method': 'blacklist', 'engine_update': '20220711'},
           'tehtris': {'category': 'type-unsupported', 'engine_name': 'tehtris', 'engine_version': None, 'result': None,
                       'method': 'blacklist', 'engine_update': '20220711'},
           'DrWeb': {'category': 'undetected', 'engine_name': 'DrWeb', 'engine_version': '7.0.56.4040', 'result': None,
                     'method': 'blacklist', 'engine_update': '20220711'},
           'MicroWorld-eScan': {'category': 'malicious', 'engine_name': 'MicroWorld-eScan',
                                'engine_version': '14.0.409.0',
                                'result': 'Trojan.GenericKD.46599608', 'method': 'blacklist',
                                'engine_update': '20220711'}}

stats = {'harmless': 0, 'type-unsupported': 15, 'suspicious': 0, 'confirmed-timeout': 0, 'timeout': 0, 'failure': 0,
         'malicious': 16, 'undetected': 42}


def fake_analyse(self, _id):
    print("Do something I want!")
    return results, stats


@mock.patch.object(MetadataVT, 'analyse', fake_analyse)
@mock.patch('src.metadata.metadata_vt.requests')
@mock.patch('src.metadata.metadata_vt.time')
def test_get_metadata(time_mock, requests_mock):
    requests_post = mock.Mock()
    requests_mock.return_value = requests_post
    requests_post.post.return_value = 'Salut'
    medata_vt_object = MetadataVT()
    file_path = os.path.join(os.path.join(conf.TEST_FOLDER, 'content/my_script.js'))
    df_stats, df_result = medata_vt_object.get_metadata(file_path)
    assert df_stats['malicious'].to_list()[0] == 16
    assert df_result.loc['Lionic', 'category'] == 'malicious'
