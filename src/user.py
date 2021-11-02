from decimal import Decimal
from dataclasses import dataclass

@dataclass
class User:
    """Class for storing current logged in user information"""
    uuid: str
    balance: Decimal # for fixed  decimal precision to avoid float unaccuracy
    num_coffee: int
    registered: str
    last_logged_in: str
    logged_in: str

