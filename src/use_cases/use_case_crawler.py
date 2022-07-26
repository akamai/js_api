from src.crawler.crawler import Crawler


class UseCaseCrawler(object):
    """
    Use case for running the crawler
    """
    def __init__(self, _url, depth, output):
        self._url = _url
        self.depth = depth
        self.output = output

    def run(self):
        crawler_object = Crawler(_url=self._url, depth=self.depth, output=self.output)
        crawler_object.run()
