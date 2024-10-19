from flask_login import UserMixin

# Un modelo de usuario simple que utiliza UserMixin para compatibilidad con Flask-Login
class User(UserMixin):
    users = {
        "1": {"id": "1", "username": "admin", "email": "admin@example.com", "password": "admin"},
        "2": {"id": "2", "username": "user", "email": "user@example.com", "password": "user"}
    }

    def __init__(self, user_id, username, email):
        self.id = user_id
        self.username = username
        self.email = email

    @staticmethod
    def get(user_id):
        user = User.users.get(user_id)
        if user:
            return User(user['id'], user['username'], user['email'])
        return None

    @staticmethod
    def authenticate(email, password):
        for user in User.users.values():
            if user['email'] == email and user['password'] == password:
                return User(user['id'], user['username'], user['email'])
        return None
