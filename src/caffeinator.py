from .db import DBManager

class Caffeinator():

    def __init__(self) -> None:
        self.db = DBManager()
        self.rfid_reader = ...
    
    def onUUID(self, uuid: str) -> None:
        user = self.db.user_from_uuid(uuid)

    