import importlib.metadata
import pathlib
import logging.config

import rich.logging

import mrmat_xmas_2024.model

try:
    __version__ = importlib.metadata.version('mrmat-xmas-2024')
except importlib.metadata.PackageNotFoundError:
    # You have not yet installed this as a package, likely because you're
    # interactively working on it
    __version__ = '0.0.0.dev0'

__default_config_file__ = pathlib.Path('~/etc/mrmat-xmas-2024.yml').expanduser()
__version_header__ = 'X-Version'

__log_config__ = {
    "version": 1,
    "formatters": {
        "server": {"format": "[%(name)s] %(message)s"},
    },
    "handlers": {
        "server": {
            "()": "rich.logging.RichHandler",
            "show_time": False,
            "show_path": False,
            "formatter": "server",
        },
    },
    "loggers": {
        "": {"level": "INFO", "handlers": ["server"], "propagate": False},
        "mrmat_xmas_2024": {"level": "INFO", "handlers": ["server"], "propagate": False},
        "httpx": {"level": "WARNING", "handlers": ["server"]},
        "httpcore": {"level": "WARNING", "handlers": ["server"]},
        "uvicorn": {"level": "INFO", "handlers": ["server"], "propagate": False},
    },
}
logging.config.dictConfig(__log_config__)