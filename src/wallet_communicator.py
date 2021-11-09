import requests
import json
from pathlib import Path

from .user import User

class WalletCommunicator():

    config_file = Path("config.json")

    def __init__(self) -> None:
        if not self.config_file.exists():
            raise ValueError(f"config file {str(self.config_file.resolve())} does not exist!")
        
        with self.config_file.open() as config:
            self._config = json.load(config)
        
        self._wallet_host = self._config["wallet_host"]
        self._wallet_port = self._config["wallet_port"]
    
    def user_from_uid(self, uid) -> User:
        ...
    
    def make_purchase(self, user, products) -> float:
        ...
