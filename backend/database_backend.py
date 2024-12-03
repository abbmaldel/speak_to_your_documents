import sqlite3
from time import time
from uuid import uuid4

# Connect to an SQLite database (or create it if it doesn't exist)


class Database:
    def __init__(self, database_location: str) -> None:
        self._conn = sqlite3.connect(database_location)
        self._cursor = self._conn.cursor()
        self._cursor.execute(
            f"""CREATE TABLE IF NOT EXISTS messages
                (epoch real, SSID text, role text, content text, UUID text)"""  # there is a date time type, but I am lazy!
        )
        self._conn.commit()

    def store_message(self, SSID: str, role: str, message: str) -> None:

        # Insert a row of data
        self._cursor.execute(
            f"INSERT INTO messages VALUES(?,?,?,?,?)",
            (str(time()), SSID, role, message, str(uuid4())),
        )
        self._conn.commit()

    def get_messages(self, SSID: str) -> None:
        a = self._cursor.execute(
            "SELECT role, content FROM messages a WHERE a.SSID=? ORDER BY epoch",
            (SSID,),
        )
        return [{"role": i, "content": j} for i, j in a]

    def __drop_table(self):
        self._cursor.executescript(
            "PRAGMA foreign_keys = OFF;DROP TABLE messages;PRAGMA foreign_keys = OFF;"
        )
        """use carefully"""

    # Save (commit) the changes

    # Close the connection
    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self._conn.close()

    def __del__(self):
        self._conn.close()


def main():
    with Database("../databases/messages.db") as test_base:
        test_base.store_message("test", "user", "testing testing!")
        print(test_base.get_messages("test"))


if __name__ == "__main__":
    main()
