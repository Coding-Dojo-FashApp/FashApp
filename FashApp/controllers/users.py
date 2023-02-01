from FashApp import app
from flask import render_template,request, redirect,session
from FashApp.models import user
from FashApp.models import clothing_category
from datetime import datetime
from flask_bcrypt import Bcrypt
from flask import flash
bcrypt = Bcrypt(app)
dateFormat = "%m/%d/%Y %I:%M %p"


@app.route('/') 
def index():
    return render_template('login_register.html') 

@app.route("/getlogin")
def getlogin():
    return render_template('login.html')

@app.route("/getreg")
def getreg():
    return redirect("/")

@app.route('/register', methods = ['POST'])
def register():
    if user.User.validate_create(request.form):
        print(request.form['password'])
        pw_hash = bcrypt.generate_password_hash(request.form['password'])
        print(pw_hash)
        data = {
            'first_name': request.form['first_name'],
            'last_name': request.form['last_name'], 
            'email': request.form['email'],
            'password': pw_hash
        } 
        session['users_id'] = user.User.save(data)
        return redirect('/home')
    return redirect('/getlogin')

@app.route('/login', methods = ['POST'])
def login():
    data = {"email" : request.form["email"]} 
    user_in_db = user.User.get_by_email(data)
    if user_in_db: 
        if bcrypt.check_password_hash(user_in_db.password, request.form['password']):
            session['users_id'] = user_in_db.id
            return redirect('/home')
    flash("Invaid crediencals", 'regError')
    return redirect('/')

@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')

@app.route('/home') 
def dashboard():
    if 'users_id' in session:

        return render_template('index.html',current_user = user.User.get_one(session["users_id"]), all_category = clothing_category.Clothing_catagories.get_all() )
    return redirect('/')