from beaker.util import parse_cache_config_options
from zope.component import queryUtility
from dolmen.beaker.interfaces import ISessionConfig


def setupCache():
    options = queryUtility(ISessionConfig)
    if options is not None:
        return parse_cache_config_options(options)
