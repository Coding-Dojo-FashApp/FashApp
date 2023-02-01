from FashApp.config.mysqlconnection import connectToMySQL
from FashApp.models import user



class Clothing_catagories:
    DB = "fashion_inventory"
    
    def __init__(self, data):
        self.id = data['id']
        self.name = data['name']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.user_id = data['user_id']
        self.user = []


    @classmethod
    def get_all(cls):
        # print("\n __catagories get all method___")
        query = "SELECT * FROM clothing_catagories LEFT JOIN users ON clothing_catagories.user_id = users.id"
        results = connectToMySQL(cls.DB).query_db(query)

        catagories = []
        
        for row in results:
            category = cls(row)
            # print(category) 
            user_data = {
                "id" : row["users.id"],
                "first_name" : row["first_name"],
                "last_name" : row["last_name"],
                "email" : row["email"],
                "password" : row["password"],
                "created_at" : row["users.created_at"],
                "updated_at" : row["users.updated_at"]

            }
            
            category.user = user.User(user_data)
            catagories.append(category)
            # print(catagories)
        return catagories
    
    @classmethod 
    def get_category_by_id(cls,id):
        # print("\n __catagories get by id method___")
        data = {"id" : id}
        query = "SELECT * FROM clothing_catagories LEFT JOIN users ON clothing_catagories.user_id = users.id WHERE clothing_catagories.id = %(id)s"
        results = connectToMySQL(cls.DB).query_db(query, data)
        row = results[0]
        category = cls(row)
        user_data = {
            "id" : row["users.id"],
            "first_name" : row["first_name"],
            "last_name" : row["last_name"],
            "email" : row["email"],
            "password" : row["password"],
            "created_at" : row["users.created_at"],
            "updated_at" : row["users.updated_at"]
        }
        category.user = user.User(user_data)
        print(category)
        return category
    
    
    @classmethod
    def save(cls, data):
        print("\n __clothing_categories Save Method__")
        query = "INSERT INTO clothing_catagories ( name, created_at, updated_at, user_id) VALUES ( %(name)s, NOW(), NOW(), %(user_id)s );"
        return connectToMySQL(cls.DB).query_db( query, data )