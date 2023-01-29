from FashApp.config.mysqlconnection import connectToMySQL
from flask import flash
import re
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
mydb = 'fashion_inventory'


class User:
    def __init__( self , data ):
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
        self.password = data['password']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at'] 

    @staticmethod
    def validate_create(request):
        is_valid = True
        if len(request['first_name']) < 1:
            flash("please Enter A first name", 'regError')
            is_valid = False
        elif len(request['first_name']) < 3:
            flash("First Name must be longer than two characters",'regError')
            is_valid = False 
        if len(request['last_name']) < 1:
            flash("please enter a last_name",'regError')
            is_valid = False
        elif len(request['last_name']) < 3:
            flash("Last Name must be longer than two characters", 'regError')
            is_valid = False 
        if len(request['email']) < 1:
            flash("please enter a email",'regError')
            is_valid = False
        elif not EMAIL_REGEX.match(request['email']) :
            flash("invaild email address",'regError')
            is_valid = False
        if len(request['password']) < 1: 
            flash("please enter a last_name",'regError')
            is_valid = False
        elif len(request['password']) < 9:
            flash("Last Name must be longer than nine characters",'regError')
            is_valid = False 
        if len(request['confirm_password']) < 1:
            flash("please confirm password",'regError')
            is_valid = False 
        elif request['password'] != request['confirm_password']:
            flash('password doesnt match','regError')
            is_valid - False
        return is_valid 
    
    @classmethod
    def getthis(cls):
        query =  "SELECT * from users;" 
        results = connectToMySQL(mydb).query_db(query)
            
        getthis = []
        # Iterate over the db results and create instances of friends with cls.
            
        for user in results:
            getthis.append( cls(user) )
        return getthis

    @classmethod
    def save(cls, data ):
        query = "INSERT INTO users ( first_name , last_name , email ,password, created_at, updated_at ) VALUES ( %(first_name)s , %(last_name)s , %(email)s ,%(password)s, NOW() , NOW());"
        
        return connectToMySQL(mydb).query_db( query, data )

    @classmethod
    def get_one(cls,data):
        print(data)
        query = "SELECT * FROM users WHERE users.id =%(id)s;"
        results = connectToMySQL(mydb).query_db(query, data)
        if len(results) < 1:
            return False 
        return cls(results[0])

    @classmethod
    def get_by_email(cls,data):
        print(data)
        query = "SELECT * FROM users WHERE email =%(email)s;"
        results = connectToMySQL(mydb).query_db(query, data)
        if len(results) < 1:
            return False 
        return cls(results[0])