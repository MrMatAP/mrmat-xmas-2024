import importlib.metadata
import fastapi
import fastapi.middleware.cors

import mrmat_xmas_2024.model

try:
    __version__ = importlib.metadata.version('mrmat-xmas-2024')
except importlib.metadata.PackageNotFoundError:
    # You have not yet installed this as a package, likely because you're
    # interactively working on it
    __version__ = '0.0.0.dev0'

__version_header__ = 'X-Version'
