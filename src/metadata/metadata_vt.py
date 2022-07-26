import logging
import os
import pandas as pd
import requests
import time

from src.metadata.metadata import Metadata
import conf

logger = logging.getLogger(conf.LOGGER_NAME)


class MetadataVT(Metadata):
    """
    Metadata VT object. For now get_metadata uploads the file and waits for the results.
    Don't forget to store your key in credentials.json.
    """
    NAME = 'VT'
    VT_URL = "https://www.virustotal.com/api/v3/"

    def __init__(self):
        super().__init__()
        self.key = self.load_key(self.NAME)
        self.headers = {
            "Accept": "application/json",
            "x-apikey": self.key}

    def get_metadata(self, file_path):
        """
        Take a file, upload it to VT and return stats and df on engine results
        Args:
            file_path: file to analyze

        Returns: df_stats, df_engines

        """
        url = os.path.join(self.VT_URL, "files")
        files = {"file": open(file_path, "rb")}
        response = requests.post(url, files=files, headers=self.headers)
        _id = response.json()['data']['id']
        results = self.wait_and_analyze(_id)
        if not results:
            return None
        df_engines = pd.DataFrame.from_dict(results[0]).T
        df_engines = df_engines.drop(['engine_name'], axis=1)
        df_stats = pd.DataFrame([results[1]])
        return [df_stats, df_engines]

    def analyse(self, file_id):
        """
        Analyze a file based on its VT id
        Args:
            file_id: file id

        Returns: results, stats

        """
        analysis_url = os.path.join(self.VT_URL, "analyses", file_id)
        res = requests.get(analysis_url, headers=self.headers)
        if res.status_code == 200:
            result = res.json()
            status = result.get("data").get("attributes").get("status")
            if status == "completed":
                stats = result.get("data").get("attributes").get("stats")
                results = result.get("data").get("attributes").get("results")
                return results, stats

    def wait_and_analyze(self, file_id, max_time_to_wait=conf.VT_UPLOAD_MAX_TIME):
        times = max_time_to_wait // conf.SLEEP_STEP
        rest = max_time_to_wait % conf.SLEEP_STEP
        sleep_array = [conf.SLEEP_STEP for x in range(times)] + [rest]
        logger.info(f'Sleep array {sleep_array}')
        response = None
        for sleep in sleep_array:
            logger.info(f'Waiting {sleep} seconds')
            time.sleep(sleep)
            response = self.analyse(file_id)
            if response is not None:
                return response
        logger.info('We still get null answer...')
        return response
