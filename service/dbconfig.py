import os


class DBConfig:
    def __init__(self):
        self.host = os.getenv('HOST')
        self.port = os.getenv('PORT')
        self.username = os.getenv('DB_USER')
        self.password = os.getenv('DB_PASSWORD')
        self.db = os.getenv('DB_NAME')
        self.__validate()

    def __validate(self):
        if self.host is None:
            self.host = 'localhost'
        if self.port is None:
            self.port = 3306
        if self.username is None:
            self.username = 'user'
        if self.password is None:
            self.password = 'password'
        if self.db is None:
            self.db = 'usersDB'

    def __str__(self):
        return f"DB Configuration:" \
               f"\nHost: {self.host}" \
               f"\nPort: {self.port}" \
               f"\nUsername: {self.username}" \
               f"\nPassword: {'*' * len(self.password)}" \
               f"\nDatabase: {self.db}"
