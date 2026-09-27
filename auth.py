class AuthManager:

    def __init__(self):

        self.users = {
            "admin": {
                "password": "1234",
                "role": "admin"
            },

            "staff": {
                "password": "1234",
                "role": "staff"
            },

            "customer": {
                "password": "1234",
                "role": "customer"
            }
        }

    def login(self, username, password):

        user = self.users.get(username)

        if user is not None and user["password"] == password:

            return {
                "username": username,
                "role": user["role"]
            }

        return None

    def show_users(self):

        for username, user in self.users.items():

            print(f"{username} - {user['role']}")