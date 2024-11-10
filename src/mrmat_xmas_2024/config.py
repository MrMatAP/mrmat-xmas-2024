import os
import pathlib
import dataclasses
import logging

import yaml
try:
    from yaml import CLoader as Loader, CDumper as Dumper
except ImportError:
    from yaml import Loader, Dumper

from mrmat_xmas_2024 import __default_config_file__
from mrmat_xmas_2024.model import XmasException

@dataclasses.dataclass(init=False)
class Config:
    """
    Configuration handling for mrmat-xmas-2024
    """
    tenant_id: str = dataclasses.field(default=os.getenv('AZURE_TENANT_ID'))
    backend_client_id: str = dataclasses.field(default=os.getenv('AZURE_CLIENT_ID'))
    backend_client_secret: str = dataclasses.field(default=os.getenv('AZURE_CLIENT_SECRET'))
    openapi_client_id: str = dataclasses.field(default=os.getenv('OPENAPI_CLIENT_ID'))
    testclient_client_id: str = dataclasses.field(default=os.getenv('TESTCLIENT_CLIENT_ID'))
    testclient_client_secret: str = os.getenv('TESTCLIENT_CLIENT_SECRET')

    cosmos_url: str = dataclasses.field(default=os.getenv('COSMOS_URL'))
    cosmos_db: str = dataclasses.field(default=os.getenv('COSMOS_DB'))
    cosmos_container: str = dataclasses.field(default=os.getenv('COSMOS_CONTAINER'))
    storage_url: str = dataclasses.field(default=os.getenv('STORAGE_ACCOUNT_URL'))
    storage_container: str = dataclasses.field(default=os.getenv('STORAGE_CONTAINER'))

    def __init__(self, config_file: pathlib.Path | None = None):
        self._logger = logging.getLogger(f"{self.__class__.__module__}.{self.__class__.__name__}")
        if config_file:
            self.load(config_file)

    def load(self, config_file: pathlib.Path):
        """
        Override the defaults from a config file
        Args:
            config_file (pathlib.Path): Path to the config file
        """
        if not config_file.exists():
            self._logger.warning(f"Provided configuration file {config_file} does not exist")
            return
        self._logger.info(f"Loading configuration file from {config_file}")
        configurable = {field.name: field.type for field in dataclasses.fields(self)}
        try:
            with open(config_file, "r", encoding='UTF-8') as c:
                configured = yaml.load(c, Loader=Loader)
                # Set the values for the intersection of what is configurable and actually configured
            for key in list(set(configurable.keys()) & set(configured.keys())):
                value = configured.get(key)
                if configurable.get(key) == pathlib.Path:
                    setattr(self, key, pathlib.Path(value))
                else:
                    setattr(self, key, value)
                self._logger.debug(f"Config file overrides {key} with value {value}")
        except yaml.YAMLError as ye:
            raise XmasException(code=400, msg='Invalid config file') from ye
