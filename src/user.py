from decimal import Decimal
from dataclasses import dataclass

@dataclass
class User:
    """Class for storing current logged in user information"""
    uuid: str
    balance: Decimal # for fixed  decimal precision to avoid float inaccuracy
