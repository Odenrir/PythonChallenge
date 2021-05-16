from flask_login import UserMixin


class User(UserMixin):
    def __init__(self, username, password):
        self.username = username
        self.password = password

    def to_json(self):
        return {"username": self.username}

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return self.username
