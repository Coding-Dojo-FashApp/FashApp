from FashApp.config.mysqlconnection import connectToMySQL
from FashApp.models import user
from FashApp.models import clothing_category
from flask import flash
from pprint import pprint

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
        self.category = None
        self.user = None


    @staticmethod
    def validate_post(res):
        is_valid = True
        if len(res['name']) < 0:
            flash("clothing name is Required")
            is_valid = False
        elif len(res['name']) < 3:
            flash("clothing name must be at least 3 characters.")
            is_valid = False
        if len(res['material']) < 0:
            is_valid = False
            flash(" material is Required")
        elif len(res['material']) < 3:
            is_valid = False
            flash("material must be at least 3 characters.")
            is_valid = False
        if int(res['cost']) <= 0:
            flash("price is Required")
            is_valid = False
        elif int(res['cost']) <= 3:
            flash("price must must be at least 3 characters.")
            is_valid = False
        if len(res['style']) < 0:
            flash(" style is Required")
            is_valid = False 
        elif len(res['style']) < 3:
            flash("style must be at least 3 characters.")
            is_valid = False
        if len(res['primary_color']) < 0:
            flash("primary_color  is Required")
            is_valid = False
        elif len(res['primary_color']) < 3:
            flash("primary_color must be at least 3 characters.")
            is_valid = False
        if len(res['secondary_color']) < 0:
            is_valid = False
            flash(" secondary_color is Required")
        elif len(res['secondary_color']) < 3:
            is_valid = False
            flash("secondary_color must be at least 3 characters.")
            is_valid = False
        if len(res['location_aquired']) < 0:
            is_valid = False
            flash(" location_aquired is Required")
        elif len(res['location_aquired']) < 3:
            is_valid = False
            flash("location_aquired must be at least 3 characters.")
            is_valid = False
        return is_valid


    @classmethod  
    def insert_clothing_items(cls,data):
        query = "INSERT INTO clothing_items(name,cost,material,style,primary_color,secondary_color,location_aquired,img_path,created_at,updated_at,clothing_catagory_id,user_id) VALUES (%(name)s,%(cost)s,%(material)s,%(style)s,%(primary_color)s,%(secondary_color)s,%(location_aquired)s,%(img_path)s, NOW(), NOW(), %(clothing_catagory_id)s,%(user_id)s);"
        results = connectToMySQL(mydb).query_db(query,data)
        # print(results)
        return results
    
    @classmethod
    def show_clothing_by_user(cls,id):
        data = {
            "id" : id
        }
        query =  "SELECT * FROM clothing_items LEFT JOIN clothing_catagories ON clothing_items.clothing_catagory_id= clothing_catagories.id left join users on clothing_items.user_id = users.id WHERE users.id = %(id)s" 
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
    
    @classmethod
    def get_clothing_by_category(cls,id):
        data={"id" : id}
        query =  """SELECT * FROM clothing_items LEFT JOIN clothing_catagories ON 
        clothing_items.clothing_catagory_id= clothing_catagories.id left join users on 
        clothing_items.user_id = users.id WHERE clothing_catagories.id = %(id)s ORDER BY 
        clothing_items.name ASC ;
        """ 
        results = connectToMySQL(mydb).query_db(query,data)
        catagories = []

        if results:
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
    
    
    @classmethod
    def get_all_clothing(cls):
        query = "SELECT * FROM clothing_items LEFT JOIN clothing_catagories ON clothing_items.clothing_catagory_id = clothing_catagory.id LEFT JOIN users on clothing_items.user_id = user.id ORDER BY clothing_items.name;"
        results = connectToMySQL(mydb).query_db(query)

        all_clothing = []
        for row in results:
            user_data = {
                "id" : row['users.id'],
                "first_name" : row['first_name'],
                "last_name" : row['last_name'],
                "email" : None,
                "password" : None,
                "created_at" : row['users.created_at'],
                "updated_at" : row['users.updated_at'],
                "outfits" : None
            }

            category_data ={
                "id" : row['clothing_catagories.id'],
                "name" : row['clothing_catagories.name'],
                "created_at" : row['clothing_catagories.created_at'],
                "updated_at" : row['clothing_catagories.updated_at'],
                "user_id" : row['clothing_catagories.user_id']
            }
            
            clothing = cls(row)
            clothing.category = clothing_category.Clothing_catagories(category_data)
            clothing.user = user.User(user_data)
            
            all_clothing.append(clothing)
        return all_clothing
    
    @classmethod
    def get_clothing_by_id(cls,id):
        data = {"id" : id}
        query = "SELECT * FROM clothing_items LEFT JOIN clothing_catagories ON clothing_items.clothing_catagory_id = clothing_catagory.id LEFT JOIN users on clothing_items.user_id = user.id ORDER BY clothing_items.name WHERE clothing_items.id = %(id)s;"
        result = connectToMySQL(mydb).query_db(query, data)

        row = result[0]
        
        user_data = {
            "id" : row['users.id'],
            "first_name" : row['first_name'],
            "last_name" : row['last_name'],
            "email" : None,
            "password" : None,
            "created_at" : row['users.created_at'],
            "updated_at" : row['users.updated_at'],
            "outfits" : None
        }

        category_data ={
            "id" : row['clothing_catagories.id'],
            "name" : row['clothing_catagories.name'],
            "created_at" : row['clothing_catagories.created_at'],
            "updated_at" : row['clothing_catagories.updated_at'],
            "user_id" : row['clothing_catagories.user_id']
        }
        
        clothing = cls(row)
        clothing.category = clothing_category.Clothing_catagories(category_data)
        clothing.user = user.User(user_data)
        
        return clothing