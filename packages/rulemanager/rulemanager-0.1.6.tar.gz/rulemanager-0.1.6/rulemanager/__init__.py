from rulemanager._version import __version__ as version
from rulemanager.config import script_config, package_name


__author__ = 'Blake Huber'
__version__ = version
__email__ = "blakeca00@gmail.com"


PACKAGE = package_name('DESCRIPTION.rst')

try:


    from libtools import Colors
    from libtools import logd

    # global logger
    logd.local_config = script_config
    logger = logd.getLogger(__version__)


except Exception:
    pass
