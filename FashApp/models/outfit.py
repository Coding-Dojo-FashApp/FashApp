from FashApp.config.mysqlconnection import connectToMySQL
from FashApp.models import user
from FashApp.models import clothing_item
from flask import flash
import json


class Outfit:
    DB = "fashion_inventory"
    
    def __init__(self,data):
        self.id = data['id']
        self.name = data['name']
        self.description = data['description']
        outfit_items = json.loads(data['outfit_items'])
        clothing = []
        for item in outfit_items:
            outfit_item = clothing_item.Clothing_items.get_clothing_by_id(int(item))
            clothing.append(outfit_item)
        self.outfit_items = clothing
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.user_id = data['user_id']
        self.user = None

    @classmethod
    def get_all(cls):
        query = "SELECT * FROM outfits LEFT JOIN users ON outfits.user_id = users.id ;"
        results = connectToMySQL(cls.DB).query_db(query)

        all_outfits = []
        for row in results:
            user_data = {
                "id" : row['users.id'],
                "first_name" : row['first_name'],
                "last_name" : row['last_name'],
                "email" : row['email'],
                "password" : row['password'],
                "created_at" : row['created_at'],
                "updated_at" : row['updated_at'],
            }
            clothing = cls(row)
            clothing.user = user.User(user_data)
            all_outfits.append(clothing)
        return all_outfits
    
    @classmethod
    def get_one_by_id(cls, id):
        data = {"id" : id}
        print("\n__item get_all Method__")
        query = "SELECT * FROM outfits LEFT JOIN users ON outfits.user_id = users.id WHERE outfits.id = %(id)s;"
        result = connectToMySQL(cls.DB).query_db(query, data)

        row = result[0]
        user_data = {
            "id" : row['id'],
            "first_name" : row['first_name'],
            "last_name" : row['last_name'],
            "email" : row['email'],
            "password" : row['password'],
            "created_at" : row['created_at'],
            "updated_at" : row['updated_at']
        }

        clothing = cls(row)
        clothing.user = user.User(user_data)
        return clothing
    
    @classmethod
    def get_all_by_user_id(cls,id):
        data = {"id" : id}
        query = "SELECT * FROM outfits LEFT JOIN users ON outfits.user_id = users.id WHERE outfits.user_id = %(id)s ;"
        results = connectToMySQL(cls.DB).query_db(query, data)

        all_outfits = []
        for row in results:
            user_data = {
                "id" : row['users.id'],
                "first_name" : row['first_name'],
                "last_name" : row['last_name'],
                "email" : row['email'],
                "password" : row['password'],
                "created_at" : row['created_at'],
                "updated_at" : row['updated_at'],
            }
            clothing = cls(row)
            clothing.user = user.User(user_data)
            all_outfits.append(clothing)
        return all_outfits
    
    @classmethod
    def save_outfit(cls, data):
        query = """INSERT INTO outfits ( name, description, outfit_items, created_at, updated_at, user_id) 
        VALUES ( %(name)s, %(description)s, %(outfit_items)s, NOW(), NOW(), %(user_id)s );
        """
        return connectToMySQL(cls.DB).query_db(query, data)
    
    @classmethod
    def update_outfit(cls, data ):
        query = """UPDATE outfits SET name=%(name)s, description=%(description)s, outfit_items=%(outfit_items)s WHERE id=%(outfit_id)s;
        """
        return connectToMySQL(cls.DB).query_db(query, data)
    
    @classmethod
    def delete_outfit(cls, id):
        data = {"id" : id}
        query = "DELETE FROM outfits WHERE id=%(id)s;"
        return connectToMySQL(cls.DB).query_db(query, data)
    
    @classmethod
    def validate_outfit(cls, data):
        is_valid = True

        print("\n___Item's validated data___", data)
        
        if len(data['name']) < 4:
            flash("Name must be at least 3 letters long","item_input")
            is_valid = False
        
        if data['description'] == "" or len(data['description']) < 4:
            flash("Please enter a longer description","item_input")
            is_valid = False
        
        if len(data['outfit_items']) < 1:
            flash("Please select at least 1 clothing item","item_input")
            is_valid = False
            
        return is_valid

