import sys
import json
import logging
import logging.config
from widgets import Application
from quamash import QEventLoop

try:
    import signal
    signal.signal(signal.SIGINT, signal.SIG_DFL)
except ImportError:
    pass


def configureLogging():
    try:
        with open('logging.json') as config:
            logging.config.dictConfig(json.load(config))
    except:
        from utils.logging import QtHandler
        logging.basicConfig(level=logging.WARNING, handlers=[QtHandler()])


if __name__ == '__main__':
    app = Application(sys.argv)

    configureLogging()
    log = logging.getLogger(__name__)
    log.info('starting app')

    app.start()

    loop = QEventLoop(app)

    with loop:
        sys.exit(loop.run_forever())
