import re
from MySQLdb import _mysql

from dbconfig import DBConfig


class RepoError(Exception):
    pass


class Repository:
    def __init__(self, config: DBConfig):
        print(config)
        _db = _mysql.connect(host=config.host, user=config.username, password=config.password, database=config.db,
                         port=config.port)

        # Initialize the repository with some sample user data
        self.data = {
            'USERS': [
                {'id': 1, 'username': 'admin', 'password': 'admin'},
                {'id': 2, 'username': 'user', 'password': 'user'},
            ]
        }
        self.next_index = 2

    # Method for executing a query on the repository
    def query(self, q):
        # Define regular expressions to match parts of the query
        select_pattern = r'^\s*SELECT\s+(.+?)\s+FROM\s+(.+?)\s+WHERE\s+(.+?);?$'

        # Try to match the SELECT statement
        select_match = re.match(select_pattern, q, re.IGNORECASE)

        if not select_match:
            return None, RepoError('invalid SQL query')

        columns = select_match.group(1)
        table = select_match.group(2)
        where_clause = select_match.group(3)

        # Print the parsed information
        print("Columns:", columns)
        print("Table:", table)

        pattern = r'(\S+\s*=\s*\S+)(?=\s(AND|OR)|$)'

        # Use regular expressions to find matches in the input query
        matches = re.findall(pattern, q, re.IGNORECASE)

        # Check if any matches were found in the query
        if not matches:
            return [], RepoError('no result matches query')

        # Initialize a dictionary to organize matches into 'AND' and 'OR' groups
        sorted_matches = {'AND': [matches[0][0]], 'OR': []}

        # Iterate through the matches and group them based on 'AND' or 'OR'
        for i in range(1, len(matches)):
            key = matches[i - 1][1]  # Extract the logical operator ('AND' or 'OR')
            val = sorted_matches[key]  # Get the existing list of matches for the operator
            sorted_matches[key] = val + [matches[i][0]]  # Add the current match to the list

        # Extract and process conditions from the 'OR' group
        conditions = [match.strip() for match in sorted_matches['OR']]
        for cond in conditions:
            key, val = cond.split('=')  # Split the condition into key and value
            key = key.strip()  # Remove leading/trailing whitespace from the key
            val = val.strip()  # Remove leading/trailing whitespace from the value

            try:
                # Evaluate the condition using Python's 'eval' function
                res = eval(f'{key} == {val}')
                if res is True:
                    return [self.data[table]], None  # Return a result if the condition is met
            except Exception as e:
                pass  # Handle exceptions, if any

            out = []
            # Check the condition against the data in the repository
            for row in self.data[table]:
                if row[key] == val:
                    out.append(row)
                return out, None  # Return a result if the condition is met

        # Extract and process conditions from the 'AND' group
        conditions = [match.strip() for match in sorted_matches['AND']]
        for cond in conditions:
            key, val = cond.split('=')  # Split the condition into key and value
            key = key.strip()  # Remove leading/trailing whitespace from the key
            val = val.strip()  # Remove leading/trailing whitespace from the value

            # Check the condition against the data in the repository
            if self.data[table][0][key] != val:
                return [], None  # Return an empty result if the condition is not met

        return [self.data[table][0]], None  # Return a result if all conditions are met

    def auth_user(self, user_data):
        """
                Authenticate a user by checking their username and password in the data store.
                """
        out, err = self.query(
            f'SELECT * FROM USERS WHERE username = {user_data.username} AND password = {user_data.password}')
        if err is not None or len(out) != 1:
            return False
        return True

    def create_user(self, user_data):
        """
        Create a new user and add it to the data store.
        """
        user_data['id'] = self.next_index
        self.next_index += 1
        self.data['USERS'].append(user_data)

    def get_user_by_username(self, username):
        user = self.query(f'SELECT * FROM USERS WHERE username = {username}')
        return user

    def get_user_by_id(self, id):
        print('get_user_by_id')
        user, err = self.query(f'SELECT * FROM USERS WHERE id = {id}')
        print(user, err)
        if err is not None or len(user) != 1:
            return user, RepoError('failed to get user by id', err)
        return user, None

    def update_user(self, updated_user_data):
        """
        Update an existing user's information in the data store.
        """
        for user in self.data['USERS']:
            if user['username'] == updated_user_data['username']:
                user.update(updated_user_data)
                return

    def delete_user(self, username):
        """
        Delete an existing user from the data store.
        """
        users = self.data['USERS']
        for user in users:
            if user['username'] == username:
                users.remove(user)
                return
