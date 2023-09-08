from typing import Tuple, List, Union, Any, Dict, Optional

from MySQLdb import _mysql
from argon2 import PasswordHasher
from dbconfig import DBConfig

class RepoError(Exception):
    pass

class EntityNotFound(RepoError):
    pass

class Repository:
    def __init__(self, config: DBConfig):
        self.__config = config
        self.__db = _mysql.connect(host=config.host, user=config.username, password=config.password, database=config.db, port=config.port)

    def auth_user(self, user_data: Any) -> bool:
        """
        Authenticate a user by checking their username and password in the data store.
        Returns True if authentication is successful, False otherwise.
        """
        try:
            ph = PasswordHasher()
            pwd_hash = ph.hash(user_data.password)
            password = user_data.password
            ph = pwd_hash
            self.__db.query(f"SELECT * FROM users WHERE name = '{user_data.username}' AND passwordHash = '{password}'")
            result = self.__db.store_result()
            row = result.fetch_row()
            if len(row) != 1:
                return False
            return True
        except Exception as e:
            return False

    def create_user(self, user_data: Any) -> Optional[RepoError]:
        """
        Create a new user and add it to the data store.
        Returns None on success or a RepoError if an error occurs.
        """
        try:
            password = user_data.password
            ph = PasswordHasher()
            pwd_hash = ph.hash(user_data.password)
            ph = pwd_hash
            self.__db.query(
                f"INSERT INTO users (name, passwordHash) VALUES ('{user_data.username}', '{password}')"
            )
            return None
        except Exception as e:
            return RepoError(e)

    def get_user_by_username(self, username: str):
        """
        Get a user by username.
        Returns a user dictionary if found, or None if not found.
        """
        try:
            self.__db.query(f"SELECT * FROM users WHERE name = '{username}'")
            result = self.__db.store_result()
            row = result.fetch_row()
            if len(row) != 1:
                return None, EntityNotFound(f"User with username: '{username}' not found")
            user_data = decode_row(row[0])
            user = {
                'id': user_data[0],
                'username': user_data[1]
            }
            return user, None
        except Exception as e:
            return None, RepoError(e)

    def get_users(self) -> Tuple[List[Dict[str, Any]], Optional[RepoError]]:
        try:
            self.__db.query(f'SELECT * FROM users')
            result = self.__db.store_result()
            user_rows = result.fetch_row(maxrows=0)
            users = []
            for row in user_rows:
                decoded_values = decode_row(row)
                users.append({
                    'id': decoded_values[0],
                    'username': decoded_values[1],
                })
            return users, None
        except Exception as e:
            return [], RepoError(e)

    def get_user_by_id(self, id: int) -> Tuple[Optional[Dict[str, Any]], Optional[RepoError]]:
        """
        Get a user by id.
        Returns a user dictionary if found, or None if not found.
        """
        try:
            self.__db.query(f"SELECT * FROM users WHERE id = '{id}'")
            result = self.__db.store_result()
            row = result.fetch_row()
            if len(row) != 1:
                return None, EntityNotFound(f"User with id: '{id}' not found")
            user_data = decode_row(row[0])
            user = {
                'id': user_data[0],
                'username': user_data[1]
            }
            return user, None
        except Exception as e:
            raise RepoError(e)

    def update_user(self, updated_user_data: Any) -> Optional[RepoError]:
        """
        Update an existing user's information in the data store.
        Returns None on success or a RepoError if an error occurs.
        """
        try:
            self.__db.query(
                f"UPDATE users SET name = '{updated_user_data.username}' WHERE id = '{updated_user_data.id}'"
            )
            return None
        except Exception as e:
            return RepoError(e)

    def delete_user(self, id: int) -> Optional[RepoError]:
        """
        Delete an existing user from the data store.
        Returns None on success or a RepoError if an error occurs.
        """
        try:
            self.__db.query(f"DELETE FROM users WHERE id = '{id}'")
            return None
        except Exception as e:
            return RepoError(e)

def decode_row(row: List[bytearray]) -> List[str]:
    return [value.decode('utf-8') for value in row]
