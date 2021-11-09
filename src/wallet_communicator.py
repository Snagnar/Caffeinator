import requests

from .user import User
from .utils import load_config

class WalletCommunicator():

    def __init__(self) -> None:
        self._config = load_config()
        
        self._wallet_host = self._config["wallet_host"]
        self._wallet_port = self._config["wallet_port"]
    
    def user_from_uid(self, uid: str) -> User:
        """makes api call to retrieve user information

        Args:
            uid (str): uid string from token

        Returns:
            User: User object with info from api
        """
        ...
    
    def make_purchase(self, user: User, products: dict) -> float:
        ...
