from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash


class User(UserMixin):
    def __init__(self, id, username, email, password_hash):
        self.id = id
        self.username = username
        self.email = email
        self.password_hash = password_hash

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


users = {}


def get_user_by_id(user_id):
    return users.get(int(user_id))


def get_user_by_username(username):
    for user in users.values():
        if user.username.lower() == username.lower():
            return user
    return None


def create_user(username, email, password):
    new_id = len(users) + 1
    user = User(new_id, username, email, generate_password_hash(password))
    users[new_id] = user
    return user
