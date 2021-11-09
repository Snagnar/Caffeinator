import time
from typing import Any, Callable, List, Union
import logging

from .utils import load_config
from .user import User

class UIManager():
    def __init__(self) -> None:
        self._config = load_config()
        self._user: Union[User, None] = None
        self._on_logout = lambda: logging.info("User logout!")
        self._on_logout_args: List[Any] = []
    
    def ui_loop(self) -> None:
        logging.info("Starting ui loop ...")
        while True:
            time.sleep(1)
            # TODO: put ui loop here
    
    def set_active_user(self, user: User) -> None:
        self._user = user
        # TODO: show new user

    def on_logout(self, function: Callable, args: list = []) -> None:
        self._on_logout = function
        self._on_logout_args = args
    
    def _logout(self) -> None:
        logging.info(f"Logging out user: {self._user}")
        self._on_logout(*self._on_logout_args)
        self._user = None
        # TODO: Call this method, add code for logout
