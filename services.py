from database import UserModel, ItemModel


class UserService:
    def __init__(self):
        self.model = UserModel()

    # ------------ CREATE ------------
    def create(self, params):
        return self.model.create_user(username=params['username'], email=params['email'])

    # ------------ READ ------------
    def get_all_users(self):
        return self.model.get_all()
    
    def get_by_id(self, userID:int):
        return self.model.get_by_id(userID)
    
    # def get_by_username(self, username:str):
    #     return self.model.get_by_username(username=username)
    
    # def get_by_email(self, email:str):
    #     return self.model.get_by_email(email)
    

    # ------------ UPDATE ------------
    def update_username(self, userID:int, params):
        return self.model.update_username(userID, params['new_username'])
    
    def update_user_items(self, userID:int, itemID:str):
        return self.model.save_user_item(userID, itemID)
    
    # ------------ DELETE ------------
    def delete_user(self, userID:int):
        return self.model.delete_user(userID)
    
    def delete_user_item(self, userID:int, itemID:str):
        return self.model.delete_user_item(userID, itemID)

    def delete_all_user_items(self, userID: int):
        return self.model.delete_all_user_items(userID)
    
    def delete_user_item(self, userID:int, itemID:str):
        return self.model.delete_user_item(userID, itemID)
    
    def delete_all_user_items(self, userID:int):
        return self.model.delete_all_user_items(userID)


class ItemService:
    def __init__(self, table):
        self.model = ItemModel(table_name=table)

    def get_all(self):
        return self.model.get_all()

    def get_by_id(self, id: int):
        return self.model.get_by_id(id)
    
    def get_by_name(self, params):
        return self.model.get_by_name(params['name'])
    
    def filter_by_sell_price(self, params):
        return self.model.filter_by_sell_price(params['op'], params['value'])
