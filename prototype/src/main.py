import sys
import logging
import logging.config
import asyncio
import settings
from widgets import Application
from quamash import QEventLoop

try:
    import signal
    signal.signal(signal.SIGINT, signal.SIG_DFL)
except ImportError:
    pass


def configureLogging():
    try:
        logging.config.dictConfig(settings.LOGGING)
    except:
        from utils.logging import QtHandler
        logging.basicConfig(level=logging.WARNING, handlers=[QtHandler()])


if __name__ == '__main__':
    app = Application(sys.argv)
    settings.init(app)

    configureLogging()
    log = logging.getLogger(__name__)
    log.info('starting app')

    loop = QEventLoop(app)
    asyncio.set_event_loop(loop)

    app.start()
    sys.exit(loop.run_forever())
