from tinydb import TinyDB, Query

class EmailDB:
    def __init__(self):
        self.db = TinyDB("email_db.json")
        self.table = self.db.table("emails")

    def add(self, email):
        self.table.insert({'email': email})

    def is_sent(self, email: str):
        Email = Query()
        return bool(self.table.get(Email.email == email))
