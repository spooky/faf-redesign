from PyQt5.QtCore import QSettings

ORGANIZATION_NAME = 'Forged Alliance Forever'
ORGANIZATION_DOMAIN = 'faforever.tk'
APPLICATION_NAME = 'lobby'

# Service URLs
AUTH_SERVICE_URL = 'http://{}:44343/auth'.format(ORGANIZATION_DOMAIN)
FAF_SERVICE_URL = 'http://{}:8080'.format(ORGANIZATION_DOMAIN)

LOGGING = {
    'version': 1,
    'disable_existing_loggers': True,
    'formatters': {
        'simple': {'format': '%(asctime)s - %(name)s - %(levelname)s - %(message)s'}
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'level': 'DEBUG',
            'formatter': 'simple',
            'stream': 'ext://sys.stdout'
        },
        'faf_console': {
            'class': 'utils.logging.QtHandler',
            'level': 'DEBUG',
            'formatter': 'simple'
        }
    },
    'root': {
        'level': 'DEBUG',
        'handlers': ['console', 'faf_console']
    }
}


def init(app):
    # required for settings persistance
    app.setOrganizationName(ORGANIZATION_NAME)
    app.setOrganizationDomain(ORGANIZATION_DOMAIN)
    app.setApplicationName(APPLICATION_NAME)


def get():
    return QSettings(ORGANIZATION_NAME, APPLICATION_NAME)
