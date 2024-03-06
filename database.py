import sqlite3
import pandas as pd

class AnimalCrossingDatabase:
    def __init__(self):
        self.DATA_PATH = './animal_crossing_data'
        self.ITEM_TABLE_NAMES = ['fish', 'insect', 'tool']
        self.conn = sqlite3.connect('animal_crossing.db')
        self._create_tables()

    def __del__(self):
        # body of destructor
        self.conn.commit()
        self.conn.close()

    def _create_users_table(self):
        query = '''
        CREATE TABLE IF NOT EXISTS "users" (
        userID INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT NOT NULL UNIQUE,
        email TEXT UNIQUE
        );
        '''
        print('creating users table...')
        self.conn.execute(query)


    def _create_user_items_table(self):
        query = '''
        CREATE TABLE IF NOT EXISTS "useritems" (
        userID INTEGER,
        itemID TEXT
        );
        '''
        print('creating useritems table...')
        self.conn.execute(query)


    def _create_table_from_csv(self, option):
        match option:
            case 'fish':
                print("creating fish table...")
                file_path = f'{self.DATA_PATH}/fish.csv'
                prefix = 'F'
            case 'insect':
                print("creating insect table...")
                file_path = f'{self.DATA_PATH}/insects.csv'
                prefix = 'I'
            case 'tool':
                print("creating tool table...")
                file_path = f'{self.DATA_PATH}/tools.csv'
                prefix = 'T'
            case _:
                raise Exception('[!] Option not supported.')
        
        df = pd.read_csv(file_path) # load data from csv to dataframe
        df['itemID'] = f'{prefix}-' + df.index.astype(str) # create external id
        df.to_sql(name=option, con=self.conn, if_exists='replace', index=True, index_label=f'{option}ID')


    def _create_tables(self):
        # user table
        self._create_users_table()  

        # animal crossing tables
        for tbl in self.ITEM_TABLE_NAMES:
            self._create_table_from_csv(tbl)
    
        # user items table
        self._create_user_items_table()
    



class UserModel:
    TABLE_NAME = 'users'

    def __init__(self):
        self.conn = sqlite3.connect('animal_crossing.db')
        self.conn.row_factory = sqlite3.Row

    def __del__(self):
        # body of destructor
        self.conn.commit()
        self.conn.close()

    def _select_where(self, where_clause: str):
        query = f'SELECT * FROM {self.TABLE_NAME} '

        # append where clause to query if exists
        if where_clause is not None:
            query += where_clause + ';' 
      
        response = self.conn.execute(query).fetchall()
        response = [{column: row[i]
                  for i, column in enumerate(response[0].keys())}
                  for row in response]
      
        return response
    
    def get_by_id(self, id:int):
        where_clause = f'WHERE userID = {id}'
        return self._select_where(where_clause)

    # def get_by_username(self, username:str):
    #     where_clause = f'WHERE LOWER(username) = "{username.lower()}"'
    #     return self._select_where(where_clause)

    # def get_by_email(self, email:str):
    #     where_clause = f'WHERE LOWER(email) = "{email.lower()}"'
    #     return self._select_where(where_clause)

    def get_all(self):
        '''
        Return all users
        '''
        return self._select_where(where_clause=None)

    def create_user(self, username: str, email: str, debug=False):
        '''
        Insert new user into table

        :params Attributes of user to be inserted
        '''
        query = f'INSERT INTO {self.TABLE_NAME} ' \
                f'(username, email) ' \
                f'values ("{username}", "{email}");'
        
        if debug:
            print(query)

        response = self.conn.execute(query)
        return self.get_by_id(response.lastrowid)
    
    def update_username(self, id:int, new_username:str):
        query = f'UPDATE {self.TABLE_NAME} SET username = "{new_username}" WHERE userID = {id}' 
        self.conn.execute(query)
        return self.get_by_id(id)


    def delete_user(self, id: int, debug=False):
        '''
        Delete user by userID
        '''
        # remove all of the users entries in the useritems table
        self.delete_all_user_items(userID=id)

        query = f'DELETE FROM {self.TABLE_NAME} WHERE userID={id};'

        if debug:
            print(query)
        
        self.conn.execute(query)
        return self.get_all()
    

    def save_user_item(self, userID:int, itemID:str, debug=False):
        table_name = 'useritems'
        query = f'INSERT INTO {table_name} ' \
                f'(userID, itemID) ' \
                f'values ({userID},{itemID})'

        if debug:
            print(query)

        return self.conn.execute(query)
    
    def delete_user_item(self, userID: int, itemID: str, debug=False):
        table_name = 'useritems'
        query = f'DELETE FROM {table_name} WHERE userID = {userID} AND itemID = "{itemID}";'

        if debug:
            print(query)

        return self.conn.execute(query)
    
    def delete_all_user_items(self, userID: int, debug=False):
        table_name = 'useritems'
        query = f'DELETE FROM {table_name} WHERE userID = {userID};'

        if debug:
            print(query)

        return self.conn.execute(query)


class ItemModel:
    def __init__(self, table_name):
        self.conn = sqlite3.connect('animal_crossing.db')
        self.conn.row_factory = sqlite3.Row
        self.TABLE_NAME = table_name

    def __del__(self):
        # body of destructor
        self.conn.commit()
        self.conn.close()

    def _select_where(self, where_clause: str):
        query = f'SELECT * FROM {self.TABLE_NAME} '
        
        # append where clause to query if exists
        if where_clause is not None:
            query += where_clause + ';'
        print(query)
        response = self.conn.execute(query).fetchall()
        response = [{column: row[i]
                     for i, column in enumerate(response[0].keys())}
                    for row in response]
     
        return response

    def get_by_id(self, id: int):
        where_clause = f'WHERE {self.TABLE_NAME}ID = {id}'
        return self._select_where(where_clause)
    
    def get_by_name(self, name: str):
        where_clause = f'WHERE Name = "{name}"'
        return self._select_where(where_clause)

    def get_all(self):
        '''
        Return all users
        '''
        return self._select_where(where_clause=None)
    
    def filter_by_sell_price(self, op: str, value: int):
        supported_ops = ['=', '>', '>=', '<', '<=', '<>']

        # default to '='
        if op not in supported_ops:
            op = supported_ops[0]
        
        where_clause = f'WHERE Sell {op} {value}'
        return self._select_where(where_clause)

 

   





    