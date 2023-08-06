from .version import __version__
from .executor import create_app

# if somebody does "from flint import *", this is what they will
# be able to access:
__all__ = [
    'create_app',
]