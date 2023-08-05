from __future__ import unicode_literals

from tcell_agent.tcell_logger import get_module_logger

try:
    from flask import __version__
    FLASK_VERSION = tuple([int("".join(i for i in x if i.isnumeric())) for x in __version__.split(".")])
except Exception as e:
    FLASK_VERSION = (0, 0, 0)
    get_module_logger(__name__).error("Could not obtain Flask version: {e}".format(e=e))
