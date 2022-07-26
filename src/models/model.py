import os
import json

from abc import ABC, abstractmethod


class Model(ABC):
    def __init__(self):
        pass

    @abstractmethod
    def test_js(self, *args, **kwargs):
        """return label, prediction"""
        raise NotImplementedError

    @staticmethod
    def get_type(path):
        final_type = []

        _type_list = ['inline', 'links']
        for _type in _type_list:
            if _type in os.listdir(path):
                if os.listdir(os.path.join(path, _type)):
                    final_type.append(_type)
        return final_type

    @staticmethod
    def save_js_dict(_path, _dict):
        with open(_path, 'w') as f:
            json.dump(_dict, f)
