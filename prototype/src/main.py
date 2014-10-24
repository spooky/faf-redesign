import sys
import json
import logging, logging.config
from ui import Application


def configureLogging():
    try:
        with open('logging.json') as config:
            logging.config.dictConfig(json.load(config))
    except:
        import utils
        logging.basicConfig(level=logging.WARNING, handlers=[utils.QtHandler()])

if __name__ == '__main__':
    app = Application(sys.argv)

    configureLogging()
    log = logging.getLogger(__name__)
    log.info('starting app')

    app.start()

    from samples import run_background_task_samples
    run_background_task_samples()

    sys.exit(app.exec_())
