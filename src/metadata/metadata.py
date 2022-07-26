import json
import logging
from abc import ABC, abstractmethod

import conf
from src.metadata.apinotfound import ApiNotFound

logger = logging.getLogger(conf.LOGGER_NAME)


class Metadata(ABC):

    @abstractmethod
    def get_metadata(self, js):
        raise NotImplementedError

    @staticmethod
    def load_key(key):
        try:
            with open(conf.API_CREDENTIALS) as f:
                data = json.load(f)
            return data[key]

        except Exception as e:
            logger.error('You need store your API key in the file credentials.json before continuing.')
            raise ApiNotFound
