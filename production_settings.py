# pylint: disable=W0401,W0614

from .settings import *

DEBUG = False

XMPP_SERVER = 'xmpp.playwith.xyz'
CONVERSEJS_BOSH_SERVICE_URL = 'http://xmpp.playwith.xyz:7070/http-bind/'
CONVERSEJS_ENABLED = True

ALLOWED_HOSTS.append(XMPP_SERVER)
