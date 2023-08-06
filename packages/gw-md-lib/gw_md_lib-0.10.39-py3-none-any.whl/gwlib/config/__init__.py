from . import default, development, production

from gwlib.config import *

config = {
    'development': development.Config,
    'production': production.Config,
    'default': default.Config
}
