import os
import requests
import logging
import urllib.request
import shutil
import socket
import hashlib
import urllib3
import ssl
import tldextract
from urllib.error import HTTPError, URLError
from urllib.parse import urlparse
from bs4 import BeautifulSoup
from collections import defaultdict
from .endrecursive import EndRecursive
import conf

logger = logging.getLogger(conf.LOGGER_NAME)
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
socket.setdefaulttimeout(conf.TIMEOUT_DOWNLOAD)
ssl._create_default_https_context = ssl._create_unverified_context


class Crawler(object):
    """
    This class contains all the methods related to url crawling
    """
    HEADERS = {"Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,/;q=0.8",
               "Accept-Encoding": "gzip, deflate", "Accept-Language": "*", "Connection": "keep-alive",
               "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
                             "Chrome/86.0.42400.198 Safari/537.36"}

    URLS = 'urls'
    opener = urllib.request.build_opener()
    opener.addheaders = [(v, k) for k, v in HEADERS.items()]
    urllib.request.install_opener(opener)

    def __init__(self, _url, lock=None, depth=conf.DEPTH_MAX, inline_only=False, output=conf.DOWNLOAD_FOLDER):
        self.lock = lock
        self.main_domain = self.__get_primary_domain(_url)
        self.main_page = 'http://' + self.main_domain
        self.output = output
        self.main_folder = os.path.join(self.output, self.url_to_file_folder_name(_url))
        self.url = _url
        self.url_list = []
        self.js_list = []
        self.inline_js_hash = set()
        self.domain_redirected = self.main_domain  # By default it's the same value
        self.depth = depth
        self.inline_only = inline_only

    def run(self):
        """
        Main method to run the crawler
        :return:
        """
        url_fixed = self.fix_url(self.url)
        if not self.process_or_not(url_fixed):
            return
        try:
            self.recursive_crawl(url_fixed)
        except EndRecursive:
            pass
        self.__delete_empty_folder()

    def recursive_crawl(self, _url):
        """
        Recursive crawling on a website. It crawls all the urls found.
        :param _url: url to crawl
        :return: void
        """
        if not _url:
            return None
        self.end_recursive_check()
        request = self.__request(_url)
        if not request:  # request = None
            return
        if len(request.content) < 5:
            logger.info(f'We skip {_url}. EMPTY CONTENT')
            return
        soup = BeautifulSoup(request.content, 'html.parser')
        if len(self.url_list) == 0:  # The first one, we always process
            self.__check_for_redirection(request)  # it
            os.makedirs(os.path.join(self.main_folder, conf.LINKS), exist_ok=True)
            os.makedirs(os.path.join(self.main_folder, conf.INLINE), exist_ok=True)
            self.__download_js(_url, soup)
            self.url_list.append(self.__format_for_url(_url))
            self.end_recursive_check()
        self.__parse(_url, soup)

    def __parse(self, _url, soup):
        """
        Parse the soup of URLs
        :param _url: url
        :param soup: bs4 object
        :return: void
        """
        for i in soup.find_all("a"):
            if 'href' not in i.attrs:
                continue

            href = i.attrs['href']
            if len(href) > conf.MAX_LEN_URL:
                logger.info('TOO LONG URL {}'.format(_url))
                continue

            if href.startswith("/"):
                href = self.main_page + href

            if href.startswith("http"):
                if not (self.__get_primary_domain(href).endswith(self.main_domain)) and (
                        not self.__get_primary_domain(href).endswith(self.domain_redirected)):
                    logger.debug('We skip {}'.format(href))
                    continue

                if self.__format_for_url(href) not in self.url_list:
                    self.__download_js(href, soup)
                    self.url_list.append(self.__format_for_url(href))
                    logger.info('Scraping {}'.format(href))
                    self.recursive_crawl(href)

    def __request(self, _url):
        """
        Make the requests and handles different exception
        :param _url: url
        :return: request object
        """
        try:
            request = requests.get(_url, timeout=conf.TIMEOUT_CRAWL, headers=self.HEADERS,
                                   verify=False)  # 10 seconds timeout
        except requests.exceptions.ConnectTimeout as e:
            logger.error("CONNECT TIMEOUT for {}".format(_url))
            return
        except requests.exceptions.ReadTimeout as e:
            logger.error("READ TIMEOUT for {}".format(_url))
            return
        except requests.exceptions.SSLError as e:
            logger.error("SSL Error for {}. Exception {}".format(_url, e))
            return
        except requests.exceptions.ConnectionError as e:
            try:
                if 'nodename nor servname provided, or not known' in e.args[0].reason.args[0]:
                    logger.error(f'{_url} DOWN')
                else:
                    logger.error(f'Connection error for requesting {_url}')
                return
            except Exception as e:
                logger.error(f'Connection error for requesting {_url} {e}')
                return
        except Exception as e:
            logger.error(f'NEW error {e} for requesting {_url}')
            return
        return request

    def __download_js(self, _url, soup):
        """
        Download the js links found in the Beautiful soup object as well as the JS found directly on the page
        :param _url: url
        :param soup: bs4 object
        :return: void
        """
        js_dict = self.extract_js_from_soup(soup)
        if not js_dict:  # so we don't have an empty folder
            return

        base_path = self.get_path_to_download(_url)
        links_to_be_written = []
        # DOWNLOAD LINKS
        if not self.inline_only:
            for _url in js_dict[conf.LINKS]:
                if self.__format_for_url(_url) in self.js_list:
                    continue
                _hash = 'download_failed'
                url_folder_name = self.url_to_file_folder_name(_url)
                path_to_download = os.path.join(self.main_folder, conf.LINKS, url_folder_name)
                _hash = self.download_single_js(_url, path_to_download)
                self.js_list.append(self.__format_for_url(_url))
                links_to_be_written.append(url_folder_name.replace('.js', '') + f'_{_hash}.js')

        # WRITE URL FOLDER

        new_js_inline = {}
        current_js_hash = []  # we can have duplicate maybe
        for i, local_js in enumerate(js_dict[conf.INLINE]):
            local_js_hash = hashlib.sha256(local_js.encode()).hexdigest()
            if local_js_hash not in self.inline_js_hash:
                new_js_inline[local_js_hash] = local_js
                self.inline_js_hash.add(local_js_hash)
                current_js_hash.append(local_js_hash)
            else:
                current_js_hash.append(local_js_hash)
        path_to_save = os.path.join(base_path, conf.INLINE + ".txt")
        if current_js_hash:
            with open(path_to_save, 'w') as f:
                f.write('\n'.join(current_js_hash))
        if new_js_inline:
            for _hash in new_js_inline:
                with open(os.path.join(self.main_folder, conf.INLINE, _hash + ".js"), 'w') as f:
                    f.write(new_js_inline[_hash])

        # WRITE LINKS REFERENCE

        with open(os.path.join(base_path, conf.LINKS + '.txt'), 'w') as f:
            f.write('\n'.join(links_to_be_written))

    @staticmethod
    def download_single_js(_url, dir_to_download):
        """

        :param _url: url
        :param dir_to_download: dir to download the js or path
        :return: hash of the downloaded file
        """
        try:
            request = requests.get(_url, timeout=conf.TIMEOUT_CRAWL, headers=Crawler.HEADERS,
                                   verify=False)
            if not request:
                logger.error(f"Request failed for {_url}")
            if len(request.content) < 3:
                logger.error(f'Empty JS for {_url}')
            _hash = hashlib.sha256(request.content).hexdigest()
            if os.path.isdir(dir_to_download):
                path_to_download = os.path.join(dir_to_download, f"{_hash}.js")
            else:
                path_to_download = dir_to_download.replace('.js',
                                                           '') + f'_{_hash}.js'  # for the links we just append the hash
            with open(path_to_download, 'wb') as f:
                f.write(request.content)
            # urllib.request.urlretrieve(_url, path_to_download) # For now we don't use it because it returns bad request for some JS urls
            logger.info("""{} DOWNLOADED in {}!""".format(_url, path_to_download))
            return _hash
        except HTTPError as e:
            logging.error(f'{e} for {_url}')
        except URLError as e:
            if isinstance(e.reason, socket.timeout):
                logging.error('socket timed out - URL %s', _url)
            else:
                logging.error(f'NEW error {e} for downloading JS : on {_url}')
        except ConnectionResetError as e:
            logger.error(f'{e} for {_url}')
        except UnicodeError as e:
            logger.error(f'{e} for {_url}')
        except Exception as e:
            logger.error(f'NEW ERROR {e} for {_url}')

    def extract_js_from_soup(self, soup):
        """
        Extract all js content from the soup
        :param soup: bs4 object
        :return: dict {"JS_LINKS": [link1, link2], "JS_INLINE": [js1, js2]}
        """
        js_dict = defaultdict(list)
        for script in soup.find_all("script"):
            print(js_dict, '\n\n')  # "text/javascript" is optional !!
            if 'type' in script.attrs:
                if script.attrs['type'] == 'text/javascript':
                    js_dict = self.gather_js(script, js_dict)
            else:  # IF NOTHING IT' JS --
                js_dict = self.gather_js(script, js_dict)
        return js_dict

    @staticmethod
    def __format_for_url(__url):
        """
        Define a unique format for url. So we can check if this url as been processed or not
        :param __url: url
        :return: str
        """
        if __url.endswith('/'):
            __url = __url[:-1]
        return __url

    def gather_js(self, script, js_dict):
        """
        Update the js_dict
        :param script: object from beautiful soup
        :param js_dict: dict
        :return: js_dict updated
        """
        if 'src' in script.attrs:  # it's a link !
            link = script.attrs['src']
            if not link.startswith('http'):
                link = self.main_page + link
            js_dict[conf.LINKS].append(link)
        else:  # inline
            if len(script.text) >= conf.MIN_CHARACTER_LEN_JS:
                js_dict[conf.INLINE].append(script.text)
            else:
                pass  # we don't log since it happens too much
                # logger.warning(f"JS too short we don't keep it")
        return js_dict

    def __check_for_redirection(self, request):
        new_url = request.url
        domain = self.__get_primary_domain(new_url)
        if domain != self.main_domain:
            self.domain_redirected = domain

    def get_path_to_download(self, _url):
        """
        Create a path to download the js files from an url
        :param _url: url
        :return: void
        """
        new_path = os.path.join(self.main_folder, self.URLS, self.url_to_file_folder_name(_url))
        os.makedirs(new_path, exist_ok=True)

        return new_path

    @staticmethod
    def url_to_file_folder_name(_url):
        """
        Convert an url in a correct folder name and create the folder
        :param _url: url
        :return: void
        """
        if "?" in _url:  # we don't want the parameters
            _url = _url[:_url.index("?")]
        _url = _url.replace('http://', '').replace('https://', '').replace(r"/", "_")
        if len(_url) > 200:  # max length for file name 255
            logger.info(f'{_url} too long ! We cut it to create a file name')
            _url = _url[:200] + 'CUT'
        return _url

    def __get_primary_domain(self, _url):
        """
        Get primary domain from an URL
        :param _url: url
        :return: primary domain
        """
        if self.lock:
            self.lock.acquire()
        primary_domain = tldextract.extract(_url).domain + '.' + tldextract.extract(_url).suffix
        if self.lock:
            self.lock.release()
        return primary_domain

    def __delete_empty_folder(self):
        if not os.path.isdir(os.path.join(self.main_folder, self.URLS)):
            try:
                shutil.rmtree(self.main_folder)
                logger.info('We deleted {} because it was empty'.format(self.main_folder))
            except Exception as e:
                pass  # probably was never created or deleted by another logic

    def process_or_not(self, url):
        path = urlparse(url).path
        if '.' not in path:
            return True
        path_splited = path.split('.')
        if path_splited[-1] == 'js':  # We take the last point to check the extension of the URL, we allow only JS
            logger.info(f'JS URL detected {url}. We download it as is')
            path_to_download = os.path.join(self.output, self.url_to_file_folder_name(url), conf.INLINE)
            os.makedirs(path_to_download, exist_ok=True)
            self.download_single_js(url, path_to_download)
            return False
        logger.info(f'We skip {url}. Bad extension URL')
        return False

    def end_recursive_check(self):
        if len(self.url_list) >= self.depth:
            logger.info('Depth max {} reached'.format(self.depth))
            raise EndRecursive()  # Nice way to cut the process

    @staticmethod
    def fix_url(domain):
        if "." not in domain:
            return None
        domain = domain.replace('\n', '')
        if domain.endswith('.'):
            domain = domain[:-1]
        if not domain.startswith("http"):
            domain = f'http://{domain}'
        if domain.endswith('/'):
            domain = domain[:-1]
        return domain
