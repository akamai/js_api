import os
import sys
import conf
import shutil
from collections import defaultdict

from src.models.model import Model

sys.path.append(os.path.join(os.path.dirname(__file__), "JStap", "classification"))
sys.path.append(os.path.join(os.path.dirname(__file__), "JStap", "pdg_generation"))

from src.models.JStap.pdg_generation.node import *
from src.models.JStap.classification.classifier import main_classification
from src.models.JStap.pdg_generation.pdgs_generation import store_pdg_folder

logger = logging.getLogger(conf.LOGGER_NAME)


class ModelJstap(Model):
    """
    To use it run git clone https://github.com/Aurore54F/JStap
    from this repo. You get a folder named "JStap". Also do the modifications specified in the Readme
    """
    NAME = "JStap_Pretrained_model_for_BlackHat_2022"

    def __init__(self, th=None, model_path=os.path.join(conf.MODEL_TRAINED, 'model'),
                 analysis_path=os.path.join(conf.MODEL_TRAINED, 'analysis')):
        super().__init__()
        self.th = self.load_threshold(th)
        self.model_path = model_path
        self.analysis_path = analysis_path

    def get_js_dict(self, limit, _path):
        """
        js_dict = {"inline": {"1.js":{"path" : "mydomain/inline/a.js",
                               "pdg_path": "mydomain/PDGs/a",
                               "prediction": 0.5,
                               "label": "malicious"}}}

        :param limit: int. Number of JS to process
        :param _path: domain folder
        :return:
        """
        _type_list = self.get_type(_path)
        to_process_folder = self.get_process_js(_path, limit, _type_list)
        self.extract_ast(to_process_folder)
        pdg_list = self.get_pdg_list(to_process_folder)
        if len(pdg_list) == 0:
            return None
        js_dict = self.create_js_dict(_path, _type_list)
        if len(js_dict) == 0:
            return None
        predictions = self.test_js(pdg_list, self.th)
        logger.info(f'Got {len(predictions)} results')
        for _type in _type_list:
            for prediction in predictions:
                js_name = os.path.basename(prediction[0]) + ".js"
                if js_name in js_dict[_type]:
                    js_dict[_type][js_name]['label'] = prediction[1]
                    js_dict[_type][js_name]['prediction'] = prediction[2]

        for _type in _type_list:
            for js_name in js_dict[_type]:
                if 'label' not in js_dict[_type][js_name]:
                    js_dict[_type][js_name]['label'] = 'NotTested/Skipped'
                    js_dict[_type][js_name]['prediction'] = 'NotTested/Skipped'

        self.save_js_dict(os.path.join(conf.HISTORY_RESULT, os.path.basename(_path) + ".json"), js_dict)
        logger.info("Results saved")
        logger.info('js_dict', js_dict)
        return js_dict

    def test_js(self, pdg_list, th):
        """
        Run the repo model JStap
        Args:
            pdg_list:
            th:

        Returns:

        """
        logger.info('pdg_list', pdg_list)
        args = dict()
        args['js_files'] = pdg_list
        args['model'] = [self.model_path]
        args['level'] = ['ast']
        args['n'] = 4
        args['features_choice'] = ['ngrams']
        args['threshold'] = [th]
        args['analysis_path'] = self.analysis_path
        result = main_classification(**args)
        return result

    def get_th(self):
        return self.th

    @staticmethod
    def load_threshold(th):
        if th is None:
            with open(os.path.join(conf.MODEL_TRAINED, "threshold.txt")) as f:
                return float(f.read())
        return th

    @staticmethod
    def get_process_js(_path, limit, _type_list):
        """
        Get the list of JS to process
        Args:
            _path: path of the domain folder
            limit: number of samples max to process for each type
            _type_list: list that can contain {"inline", "links"}

        Returns: folder where the JS files to be processed are copied

        """
        to_process = []
        for _type in _type_list:
            to_process += [os.path.join(_path, _type, x) for x in os.listdir(os.path.join(_path, _type))][:limit]
        to_process_folder = os.path.join(_path, conf.TO_PROCESS)
        os.makedirs(to_process_folder, exist_ok=True)
        for file_path in to_process:
            shutil.copy(file_path, os.path.join(to_process_folder, os.path.basename(file_path)))

        return to_process_folder

    @staticmethod
    def extract_ast(path):
        """
        Run AST extract
        Args:
            path: folder with JS to be processed

        Returns: void

        """
        logger.info('We start extracting the AST')
        store_pdg_folder(path)

    @staticmethod
    def get_pdg_list(path):
        """
        Get list of PDG
        Args:
            path: path

        Returns: list

        """
        pdg_folder = os.path.join(path, 'Analysis', 'PDG')
        return [os.path.join(pdg_folder, x) for x in os.listdir(pdg_folder)]

    @staticmethod
    def create_js_dict(_path, _type_list):
        """
        Create the js_dict from a domain folder
        Args:
            _path: domain folder
            _type_list: ist that can contain {"inline", "links"}

        Returns: js_dict

        """
        pdg_folder = os.path.join(_path, conf.TO_PROCESS, 'Analysis', "PDG")
        js_dict = defaultdict(dict)
        for _type in _type_list:
            files = os.listdir(os.path.join(_path, _type))
            for file in files:
                if file.endswith(".js"):
                    tmp_dict = {file: {"path": os.path.join(_path, _type, file)}}
                    if file.replace('.js', '') in os.listdir(pdg_folder):  # pdg generated
                        tmp_dict[file]['pdg_path'] = os.path.join(pdg_folder, file.replace('.js', ''))
                    else:
                        tmp_dict[file]['pdg_path'] = ''
                    js_dict[_type].update(tmp_dict.copy())
        return dict(js_dict)
