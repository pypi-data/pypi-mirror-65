"""Top-Level imports to be used with main package import."""

import os

if not bool(os.getenv('SHTUKA_SETUP')):
    from shtuka.os import load
    from shtuka.os import save
    from shtuka.wrap import cook
    from shtuka.wrap import gdict
    from shtuka.wrap import gfrozendict
    from shtuka.wrap import gfrozenlist
    from shtuka.wrap import glist
    from shtuka.wrap import raw

__version__ = '0.1.0'
