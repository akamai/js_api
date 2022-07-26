import pytest
import mock
import os
import conf
from src.metadata.metadata_publicwww import MetadataPublicWWW

search_websites_output = """url,ranking,snippets
https://www.mytrip.com/rf/start,23229,"n\',\'Product.SeatMap.Button.Continue\':\'Next\',\'Input.Last...nction(w, d, s, l, i) { w[l] = w[l] || []"
https://www.gotogate.com/,43635,"n\',\'Product.SeatMap.Button.Continue\':\'Next\',\'Input.Last...nction(w, d, s, l, i) { w[l] = w[l] || []"
https://www.student.com/,44040,"_portal.my_requests.button.continue\':\'Next\',\'student_po...95613675-325x165.jpg)\'></span></a><div cl"
https://www.desigual.com/en_GB/,49975,"\':\'CREATE ACCOUNT\',\'button.continue.shopping\':\'Continue...Face !== \'undefined\'){ var font = new Fon"
"""


@mock.patch('src.metadata.metadata_publicwww.PyPublicWWW')
def test_get_metadata(publicwww_mock):
    publicwww_mock_object = mock.Mock()
    publicwww_mock.return_value = publicwww_mock_object
    publicwww_mock_object._search_websites.return_value = search_websites_output
    metadata_publicwww = MetadataPublicWWW()
    path = os.path.join(conf.TEST_FOLDER, 'content/my_script.js')
    df = metadata_publicwww.get_metadata(path)[0]
    assert set(df['url'].to_list()) == {'https://www.mytrip.com/rf/start', 'https://www.gotogate.com/',
                                        'https://www.student.com/', 'https://www.desigual.com/en_GB/', ''}
