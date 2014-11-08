from PyQt5.QtCore import QSettings

ORGANIZATION_NAME = 'Forged Alliance Forever'
ORGANIZATION_DOMAIN = 'faforever.com'
APPLICATION_NAME = 'lobby'


def init(app):
    # required for settings persistance
    app.setOrganizationName(ORGANIZATION_NAME)
    app.setOrganizationDomain(ORGANIZATION_DOMAIN)
    app.setApplicationName(APPLICATION_NAME)


def get():
    return QSettings(ORGANIZATION_NAME, APPLICATION_NAME)
