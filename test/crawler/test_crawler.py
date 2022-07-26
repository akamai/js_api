import os
import pickle
from bs4 import BeautifulSoup

import conf
from src.crawler.crawler import Crawler


def test_fix_url():
    result = Crawler.fix_url('randomurl.com/')
    assert result == 'http://randomurl.com'


def test_run():
    """
    This test can fail if akamai website remove the majority of its JS.
    Returns:

    """
    output_folder = os.path.join(conf.TEST_FOLDER, 'crawler', 'download')
    url = 'http://akamai.com'
    crawler_object = Crawler(url, depth=1, output=output_folder)
    crawler_object.run()
    assert len(os.listdir(os.path.join(output_folder, 'akamai.com', 'inline'))) > 2
    assert len(os.listdir(os.path.join(output_folder, 'akamai.com', 'links'))) > 2



LINKS = {'https://securepubads.g.doubleclick.net/tag/js/gpt.js', 'http://ynet.co.il/Common/Api/Scripts/paywall.js',
         'http://ynet.co.il/Common/Api/Scripts/jquery-3.4.1.min.js',
         'http://ynet.co.il//totalmedia2.ynet.co.il/new_gpt/ynet/gpt_script_ynet.js',
         'http://ynet.co.il//totalmedia2.ynet.co.il/gpt/gpt_templates.js',
         'https://cdn.taboola.com/libtrc/ynet-ynet-/loader.js',
         'http://ynet.co.il//d1clufhfw8sswh.cloudfront.net/id.js?accountId=7328841',
         'http://ynet.co.il//upapi.net/pb/ex?w=5693168230072320&uponit=true',
         'https://www.ynet.co.il/Common/frontend/site/prod/vendors-widgets.e12044f5e60b5cf7d20c.js',
         'https://www.ynet.co.il/Common/frontend/site/prod/widgets.ebf6a30678f91c28ae35.js',
         'https://www.ynet.co.il/Common/Api/Scripts/YitVideoV2.js?ver=9.81',
         'http://ynet.co.il/Common/Api/Scripts/gdpr/cookieconsent.min.js', 'http://ynet.co.il',
         'https://middycdn-a.akamaihd.net/bootstrap/bootstrap.js',
         'https://images1.ynet.co.il/static/Common/javascript/newsRoomScript2.js?v=4',
         'https://c2.taboola.com/nr/ynet-ynet-/newsroom.js'}


def test_extract_js_from_soup():
    crawler = Crawler(_url='ynet.co.il')
    with open(os.path.join(conf.WORKING_DIR, 'test', 'crawler', 'content', 'soup.pickle'), 'rb') as f:
        html_content = pickle.load(f)
    soup = BeautifulSoup(html_content, 'html.parser')
    js_dict = crawler.extract_js_from_soup(soup)
    assert set(js_dict['links']) == LINKS
    assert len(js_dict['inline']) >= 2  # We check that inline contains something
