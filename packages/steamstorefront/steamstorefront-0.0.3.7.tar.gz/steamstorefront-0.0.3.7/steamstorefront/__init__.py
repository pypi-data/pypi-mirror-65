"""Top-level package for Steam Store Front."""

__author__ = """Santosh Panna"""
__email__ = 'santoshpanna.sp@gmail.com'
__version__ = '0.0.3.7'

import builtins

from .steamstorefront import SteamStoreFront
from .errors import InvalidArgument

builtins.InvalidArgument = InvalidArgument
