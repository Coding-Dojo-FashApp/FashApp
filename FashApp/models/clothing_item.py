from FashApp.config.mysqlconnection import connectToMySQL
from FashApp.models import user
from flask import flash

mydb = 'fashion_inventory'
 
class Clothing_items:
    def __init__( self , data ):
        self.id = data['id'] 
        self.name = data['name']
        self.cost = data['cost']
        self.material = data['material']
        self.style = data['style']
        self.primary_color = data['primary_color']
        self.secondary_color = data['secondary_color']
        self.location_aquired = data['location_aquired']
        self.img_path = data['img_path']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at'] 
        self.user = []
 

    @classmethod  
    def insert_clothing_items(cls,data):
        query = "INSERT INTO clothing_items(name,cost,material,style,primary_color,secondary_color,location_aquired,img_path,created_at,updated_at,clothing_catagory_id,user_id) VALUES (%(name)s,%(cost)s,%(material)s,%(style)s,%(primary_color)s,%(secondary_color)s,%(location_aquired)s,%(img_path)s, NOW(), NOW(), %(clothing_catagory_id)s,%(user_id)s);"
        results = connectToMySQL(mydb).query_db(query,data)
        # print(results)
        return results
    
    @classmethod
    def show_clothing_by_user(cls,data):
        query =  "SELECT * FROM clothing_catagories LEFT JOIN clothing_items ON clothing_items.clothing_catagory_id= clothing_catagories.id left join users on clothing_items.user_id = users.id WHERE clothing_catagories.id = %(id)s and users.id = %(user_id)s" 
        results = connectToMySQL(mydb).query_db(query,data)
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

        return catagories

