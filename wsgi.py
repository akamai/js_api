import multiprocessing
import gunicorn.app.base

import conf
from main import application, init_logger, init_folder

init_folder([conf.LOG_FOLDER, conf.HISTORY_RESULT])

logger = init_logger(debug_mode=True)
application.logger.handlers = logger.handlers


def number_of_workers():
    return (multiprocessing.cpu_count() * 2) + 1


class StandaloneApplication(gunicorn.app.base.BaseApplication):
    """
    Way to run gunicorn within Python. We do it like this there is an issue with running gunicorn from the command line
    with JStap using argparse as well.
    """
    def __init__(self, app, options=None):
        self.options = options or {}
        self.application = app
        super().__init__()

    def load_config(self):
        config = {key: value for key, value in self.options.items()
                  if key in self.cfg.settings and value is not None}
        for key, value in config.items():
            self.cfg.set(key.lower(), value)

    def load(self):
        return self.application


if __name__ == '__main__':
    options = {
        'bind': '%s:%s' % ('0.0.0.0', '8080'),
        'workers': number_of_workers(),
        'timeout': 800
    }
    StandaloneApplication(application, options).run()
