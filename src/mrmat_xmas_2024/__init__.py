import importlib.metadata

try:
    __version__ = importlib.metadata.version('mrmat-xmas-2024')
except importlib.metadata.PackageNotFoundError:
    # You have not yet installed this as a package, likely because you're
    # interactively working on it
    __version__ = '0.0.0.dev0'

