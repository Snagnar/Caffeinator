import sqlite3
from datetime import datetime
from pathlib import Path

from .user import User

class DBManager():

    db_file = Path("src/db/users.db")

    def __init__(self) -> None:
        self._connection = None
        self.db_file.parent.mkdir(parents=True, exist_ok=True)
        if not self.db_file.exists():
            self._init_db()
    
    def _init_db(self) -> None:
        self._connect()
        with self._connection:
            cursor = self._connection.cursor()
            cursor.execute("CREATE TABLE Users(id INT PRIMARY KEY, uuid TEXT, balance DECIMAL(4,2), num_coffee INT, last_logged_in TIMESTAMP, registered TIMESTAMP)")

    def _connect(self) -> None:
        self._connection = sqlite3.connect(
            self.db_file, 
            detect_types=sqlite3.PARSE_DECLTYPES | sqlite3.PARSE_COLNAMES
        )

    def user_from_uuid(self, uuid: str) -> User:
        self._connect()
        with self._connection:
            cursor = self._connection.cursor()
            user_entry = cursor.execute(f"SELECT * FROM Users WHERE uuid='{uuid}'")
            current_time = datetime.now()
            if not user_entry:
                cursor.execute(f"INSERT INTO Users(uuid, balance, num_coffee, last_logged_in, registered) VALUES ({uuid}, 0.00, 0, ?, ?)", (current_time, current_time))
                user_entry = (uuid, 0.00, 0, current_time, current_time, current_time)
            else:
                cursor.execute(f"UPDATE Users SET last_logged_in=? WHERE uuid={uuid}", (current_time,))
                user_entry.append(current_time)
            user = User(*user_entry[:3])
        return user

    def update_user(self, user: User) -> None:
        self._connect()
        with self._connection:
            cursor = self._connection.cursor()
            cursor.execute("UPDATE Users SET balance=?, num_coffee=?, last_logged_in=?", (user.balance, user.num_coffee, user.logged_in))
