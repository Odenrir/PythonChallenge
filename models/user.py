class User:
    def __init__(self, username):
        self.username = username

    def to_json(self):
        return {"username": self.username}