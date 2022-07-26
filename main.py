#!/usr/bin/env python
import logging.handlers
import hashlib
import conf
import json
import jsbeautifier
import sys
import os
import flask
from flask import Flask
from flask import render_template
from flask import request
from flask import jsonify
from src.metadata.apinotfound import ApiNotFound
from src.use_cases.use_case_model import UseCaseModel
from src.use_cases.use_case_crawler import UseCaseCrawler
from src.use_cases.use_case_metadata import UseCaseMetadata
from src.crawler.crawler import Crawler

__author__ = "Jordan Garzon"
__email__ = "jgarzon@akamai.com"

application = Flask(__name__, template_folder=conf.TEMPLATE_FOLDER, static_folder=conf.STATIC_FOLDER)
logger = logging.getLogger(conf.LOGGER_NAME)
models = UseCaseModel.get_model_list()


def init_logger(debug_mode=False):
    """
    Init logger file and print the log in stdout in debug_mode
    :param debug_mode: bool
    :return: logger object
    """
    _logger = logging.getLogger(conf.LOGGER_NAME)
    _logger.setLevel(logging.INFO)
    formatter = logging.Formatter('%(asctime)s - %(module)s - %(levelname)s - %(message)s')
    fh = logging.handlers.RotatingFileHandler(
        conf.LOGGER_FILE, maxBytes=conf.LOG_FILE_SIZE, backupCount=conf.LOG_FILE_NUMBER)

    fh.setFormatter(formatter)
    _logger.addHandler(fh)

    if debug_mode:
        stdout_handler = logging.StreamHandler(sys.stdout)
        stdout_handler.setFormatter(formatter)
        _logger.addHandler(stdout_handler)

    return _logger


def init_folder(folders):
    """
    Init folders for the app

    :return: void
    """
    for folder in folders:
        if not os.path.exists(folder):
            os.mkdir(folder)


# ROUTE

@application.route("/", methods=["GET", "POST"])
def home():
    """
    Home page
    :return: template
    """
    api = False
    if flask.request.method == 'GET':
        global models
        return render_template('index.html', models=models)
    elif flask.request.method == 'POST':
        try:
            limit = 5
            new_run = False
            if request.form.get('unlock') == 'on':
                limit = 50
            if request.form.get('new_run') == 'on':
                new_run = True
                logger.info('New run asked !')
            model_name = request.form.get("models")
            _url = request.form['text']
            if request.form.get('api') == 'true':
                api = True
            return url_scan(_url, limit=limit, new_run=new_run, model_name=model_name, api=api)
        except TimeoutError:
            return f"<h3>Took more than {conf.TIMEOUT} minutes. We give up</h3>"


@application.route("/models", methods=["GET"])
def get_model():
    """
    In general used by people using the API.
    :return: List of models loaded
    """
    return jsonify(models)


@application.route("/input", methods=["GET", "POST"])
def home_input():
    """
    One JS sample test
    :return: Template with results
    """

    if flask.request.method == 'GET':
        return render_template('index_input.html', models=models)
    elif flask.request.method == 'POST':
        try:
            logger.info(f'Input test run from {request.remote_addr}')

            model = request.form.get("models")

            js_text = request.form['text']
            _hash = hashlib.sha256(js_text.encode()).hexdigest()
            _path = os.path.join(conf.DOWNLOAD_FOLDER, _hash, 'inline')
            file_path = os.path.join(_path, _hash + '.js')
            if not os.path.exists(file_path):
                os.makedirs(_path)
                with open(file_path, 'w') as f:
                    f.write(js_text)

            return test_and_render_results(os.path.dirname(_path), model=model, url='your custom JS code', limit=5,
                                           api=None)

        except TimeoutError:
            return f"<h3>Took more than {conf.TIMEOUT} minutes. We give up</h3>"


@application.route("/js", methods=["GET"])
def get_js():
    """
    Example
    /js?domain=ynet.co.il&name=0a21c9c3986ebd084181b150efab0d589120b70f32fd93aa9554ce8d73400e1e.js&type=inline
    :return:
    """
    beautify = 'false'
    domain = request.args.get('domain')
    name = request.args.get('name')
    _type = request.args.get('type')
    try:
        with open(os.path.join(os.path.join(conf.DOWNLOAD_FOLDER, domain, _type, name))) as f:
            js_code = f.read()
    except Exception as e:
        return f"<h3>JS not found in the server</h3>"
    js_code = jsbeautifier.beautify(js_code)
    if beautify:
        if beautify.lower() == 'true':
            js_code = js_code.replace('\n', '<br>')
    return render_template('js_template.html', js_code=js_code, domain_name=domain, js=name, _type=_type)


@application.route("/metadata/<metadata>")
def get_metadata(metadata):
    """
    Route for metadata
    :param metadata: Can be any metadata ( VT, publicwww...)
    :return: template with metadata results
    """
    try:
        metadata_object = UseCaseMetadata.get_metadata(metadata)()
    except ApiNotFound:
        return f"<h2>{metadata} API key not found. You should add it in credentials.json</h2>"
    domain = request.args.get('domain')
    name = request.args.get('name')
    _type = request.args.get('type')
    file_path = os.path.join(os.path.join(conf.DOWNLOAD_FOLDER, domain, _type, name))

    result = metadata_object.get_metadata(file_path=file_path)
    if not result:
        return f"<h2>No results for {name} in {metadata}. You probably need to wait a bit if you are using a free plan</h2>"

    if len(result) == 1:  # it is PublicWWW
        return render_template(f'js_{metadata.lower()}.html',
                               results=[result[0].to_html(classes='table table-striped', justify='start')], path=name,
                               titles_results=result[0].columns)

    if len(result) == 2:  # it is VT
        return render_template(f'js_{metadata.lower()}.html',
                               results=[result[1].to_html(classes='table table-striped', justify='start')],
                               stats=[result[0].to_html(classes='table table-striped', justify='start')], path=name)


def url_scan(_url, limit, new_run, model_name, api):
    url = Crawler.fix_url(_url)
    if url.endswith('+'):  # There is a plus at the end of the url sometimes
        url = url[:-1]
    folder_name = Crawler.url_to_file_folder_name(url)
    _path = os.path.join(conf.DOWNLOAD_FOLDER, folder_name)

    if not os.path.exists(_path):
        new_run = True
    if not new_run:
        try:
            th = UseCaseModel.get_model(model_name)().get_th()

            js_dict = load_old_js_dict(folder_name)
            if api:
                return jsonify(js_dict)  # if there is a bug and the results have not been saved.
            return render_template('results.html', js_dict=js_dict, url=url, model=model_name, th=th,
                                   domain_name=folder_name)
        except Exception as e:
            logger.error(e)

    UseCaseCrawler(_url=url, depth=1, output=conf.DOWNLOAD_FOLDER).run()
    if not os.path.exists(_path):
        return "<h3>Sorry no JS found</h3></br> "
    return test_and_render_results(_path, model_name, url, limit, api=api)


def load_old_js_dict(domain_name):
    with open(os.path.join(conf.HISTORY_RESULT, domain_name + ".json")) as f:
        return json.load(f)


def test_and_render_results(_path, model, url, limit, api):
    model_object = UseCaseModel.get_model(model)()
    th = model_object.get_th()
    js_dict = model_object.get_js_dict(limit, _path)
    if not js_dict:  # TODO: Sometimes, testing an URL does not work but manually yes...
        urls_splitted = '\n'.join(return_paths_downloaded(_path))
        return f"Error in testing {url}. You can maybe test each sample manually. Below the URLs that you can query<br/>" \
               f"{urls_splitted}"

    domain_name = os.path.basename(_path)
    if api:
        return jsonify(js_dict)
    return render_template('results.html', js_dict=js_dict, url=url, model=model, th=th,
                           domain_name=domain_name)


def return_paths_downloaded(_path):
    js_urls = []
    url = os.path.basename(_path)
    for root, dirs, files in os.walk(_path, topdown=False):
        if ('inline' in root) or ('links' in root):
            for name in files:
                _type = os.path.basename(root)
                href = f"{flask.request.url}js?domain={url}&name={name}&type={_type}"
                js_urls.append(f"<a href ={href}>{name} - {_type}</a>")

    return js_urls


if __name__ == '__main__':
    """
    For better performance run the file wsgi.py 
    """
    init_folder([conf.LOG_FOLDER, conf.HISTORY_RESULT])
    logger = init_logger(debug_mode=True)
    application.run(host="0.0.0.0", port=4005, use_reloader=False, debug=False)
