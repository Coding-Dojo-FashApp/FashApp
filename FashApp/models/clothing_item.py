from flask_app.config.MySQLConnection import connect
from flask import flash
from flask_app.models import clothing_items, outfits, users
mydb = 'fashion_inventory'

class ClothingItem:
    def __init__(self,data):
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

    @staticmethod
    def validate_clothingitems(clothingitem):
        is_valid = True
        if len(clothingitem['name']) <1:
            flash('Must provide name.')
            is_valid = False
        if len(clothingitem['cost']) <1:
            flash('Must provide cost.')
            is_valid = False
        if len(clothingitem['material']) <1:
            flash('Must provide material.')
            is_valid = False
        if len(clothingitem['style']) <1:
            flash('Must provide style.')
            is_valid = False
        if len(clothingitem['primary_color']) <1:
            flash('Must provide primary color.')
            is_valid = False
        if len(clothingitem['secondary_color']) <1:
            flash('Must provide secondary color.')
            is_valid = False
        if len(clothingitem['location_aquired']) <1:
            flash('Must provide location.')
            is_valid = False
        if len(clothingitem['img_path']) <1:
            flash('Must provide image.')
            is_valid = False
        print(f"is_valid: {is_valid}")
        return is_valid

    @classmethod
    def save(cls,data):
        query = '''
        INSERT INTO clothing_items 
        (name,cost,material,style,primary_color,secondary_color,location_aquired,img_path,created_at,updated_at) 
        VALUES(%(name)s,%(cost)s,%(material)s,%(style)s,%(primary_color)s,%(secondary_color)s,%(location_aquired)s,%(img_path)s,%(created_at)s,%(updated_at)s);'''
        results = connect(mydb).query_db(query, data)
        print(f"results: {results}")
        return results
    
    @classmethod
    def getById(cls, data):
        print(data)
        query = '''
        SELECT * 
        FROM clothing_items 
        WHERE id = %(id)s;'''
        results = connect(mydb).query_db(query, data)
        print(f"results: {results}")
        return cls(results[0])

    @classmethod
    def get_all_clothingitems(cls):
        query = '''
        SELECT * 
        FROM clothing_items 
        LEFT JOIN users
        ON users.id = clothing_items.users_id;'''
        results = connect(mydb).query_db(query)
        clothingitems = []
        for row in results:
            for key, value in row.items():
                this_clothingitem = cls(row)
            user_data={
                'id' : row ['users.id'],
                'first_name' : row['first_name'],
                'last_name' : row['last_name' ],
                'email': row['email'],
                'password': row['password'],
                'updated_at': row['updated_at'],
                'created_at' : row['created_at']
            }
            this_user = users.User(user_data)
            this_clothingitem.creator = this_user
            clothingitems.append(this_clothingitem)
        return clothingitems

    @classmethod
    def get_one(cls,data):
        query  = '''
        SELECT * 
        FROM clothing_items 
        WHERE id = %(id)s'''
        result = connect(mydb).query_db(query, data)
        return cls(result[0])

    @classmethod
    def destroy(cls,data):
        query  = '''
        DELETE 
        FROM clothing_items 
        WHERE id = %(id)s;'''
        return connect(mydb).query_db(query, data)

    @classmethod
    def update(cls,data):
        query = ''' 
        UPDATE fashion_inventory.clothing_items
        SET activity = %(activity)s, duration = %(duration)s ,
        positives = %(positives)s, negatives = %(negatives)s, date= %(date)s,users_id = %(user_id)s 
        WHERE clothing_items.id = %(id)s;'''
        return connect(mydb).query_db(query, data)

    @classmethod
    def joinId(cls, data):
        query = '''
            SELECT users.first_name, users.last_name, users.email
            FROM users
            JOIN fashion_inventory.clothing_items ON users.id = users_id;
        '''
        results = connect(mydb).query_db(query, data)
        print(f"results: {results}")
        output = cls(results[0])
        for row in results:
            clothing_info = {
                id : row['id'],
                "name" : row['post.name'],
                "cost" : row['post.cost'],
                "material" : row['post.material'],
                "style" : row['post.style'],
                "primary_color" : row['post.primary_color'],
                "secondary_color" : row['post.secondary_color'],
                "location_aquired" : row['post.location_aquired'],
                "img_path" : row['post.img_path'],
                "created_at" : row['post.created_at'],
                "updated_at" : row['post.updated_at'],
                #"users_id" : row['users_id'],
            }
            output.clothing_items.append(clothing_info)
        print(output)
        return(output)

