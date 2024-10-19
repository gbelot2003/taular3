from flask_login import UserMixin

# Un modelo de usuario simple que utiliza UserMixin para compatibilidad con Flask-Login
class User(UserMixin):
    users = {
        "1": {"id": "1", "username": "admin", "password": "admin"},
        "2": {"id": "2", "username": "user", "password": "user"}
    }

    def __init__(self, user_id, username):
        self.id = user_id
        self.username = username

    @staticmethod
    def get(user_id):
        user = User.users.get(user_id)
        if user:
            return User(user['id'], user['username'])
        return None

    @staticmethod
    def authenticate(username, password):
        for user in User.users.values():
            if user['username'] == username and user['password'] == password:
                return User(user['id'], username)
        return None
