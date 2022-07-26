import logging
from src.metadata.metadata import Metadata
import pandas as pd
import conf
import urllib3
from pypublicwww import PyPublicWWW

logger = logging.getLogger(conf.LOGGER_NAME)


class MetadataPublicWWW(Metadata):
    NAME = 'PUBLICWWW'

    def __init__(self):
        super().__init__()
        self.key = self.load_key(self.NAME)
        self.publicwww_object = PyPublicWWW(self.key)

    def get_metadata(self, file_path):
        with open(file_path) as f:
            js = f.read()
        js_str = js[:100]  # We send only the first 300 characters
        try:
            result = self.publicwww_object._search_websites(js_str, csv=True, snippets=True)
        except urllib3.exceptions.MaxRetryError:
            logger.error("You probably need to wait a bit before reusing this API")
            return None
        df = self.convert_results_to_df(result)
        if len(df) == 0:
            return None
        return [df]

    @staticmethod
    def convert_results_to_df(result):
        result_splited = [x.split(',') for x in result.split('\n')]
        lines = list()
        for el in result_splited[1:]:
            tmp_list = el[:2]
            tmp_list.append(','.join(el[2:]))
            lines.append(tmp_list.copy())
        df = pd.DataFrame(lines, columns=result_splited[0])
        return df
