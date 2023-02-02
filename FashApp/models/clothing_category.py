from FashApp.config.mysqlconnection import connectToMySQL
from FashApp.models import user
from FashApp.models import clothing_item




class Clothing_categories:
    DB = "fashion_inventory"
    
    def __init__(self, data):
        self.id = data['id']
        self.name = data['name']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.user_id = data['user_id']
        self.user = []
        self.num_of = None


    @classmethod
    def get_all(cls):
        # print("\n __categories get all method___")
        query = "SELECT * FROM clothing_categories LEFT JOIN users ON clothing_categories.user_id = users.id"
        results = connectToMySQL(cls.DB).query_db(query)

        categories = []
        
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
            category.num_of = len(clothing_item.Clothing_items.get_clothing_by_category(category.id))
            categories.append(category)
            # print(categories)
        return categories
    
    @classmethod 
    def get_category_by_id(cls,id):
        # print("\n __categories get by id method___")
        data = {"id" : id}
        query = "SELECT * FROM clothing_categories LEFT JOIN users ON clothing_categories.user_id = users.id WHERE clothing_categories.id = %(id)s"
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
        category.num_of = len(clothing_item.Clothing_items.get_clothing_by_category(category.id))
        print(category)
        return category
    
    
    @classmethod
    def save(cls, data):
        print("\n __clothing_categories Save Method__")
        query = "INSERT INTO clothing_categories ( name, created_at, updated_at, user_id) VALUES ( %(name)s, NOW(), NOW(), %(user_id)s );"
        return connectToMySQL(cls.DB).query_db( query, data )