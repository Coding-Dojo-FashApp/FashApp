from FashApp import app
from flask import render_template,request, redirect,session
from FashApp.models import user, outfit, clothing_item, clothing_category
from datetime import datetime
from flask_bcrypt import Bcrypt
from flask import flash
bcrypt = Bcrypt(app)
dateFormat = "%m/%d/%Y %I:%M %p"
mydb = 'fashion_inventory'


@app.route('/post/create',methods=['POST'])
def clothingitems_display_page():
    if not clothing_item.mydb.validate_clothingitem(request.form):
        return redirect('/clothingitems/create')
    data = {
    "name" : request.form['name'],
    "cost" : request.form['cost'],
    "material" : request.form['material'],
    "style" : request.form['style'],
    "primary_color" : request.form['primary_color'],
    "secondary_color" : request.form['secondary_color'],
    "location_aquired" : request.form['location_aquired'],
    "img_path" : request.form['img_path'],
    "created_at" : request.form['created_at'],
    "updated_at" : request.form['updated_at'],
    "id" : id
    }
    result = clothing_item.mydb.save(data)
    return redirect('/clothingitems')


@app.route('/clothingitems')
def clothing_index():
    if 'user_id' in session:
        return render_template('index.html', 
        current_user = user.User.getById({'id': session['user_id']}),
        all_clothingitems = mydb.clothing_items.get_all_clothingitems()
        )
    return redirect('/')

@app.route('/clothingitems/destroy/<int:id>')
def destroy(id):
    data ={
        'id': id
    }
    mydb.clothing_items.destroy(data)
    return redirect('/clothingitems')

@app.route('/clothingitems/edit/<int:id>')
def edit(id):
    data ={ 
    "id":id
    }
    return render_template("edit.html",clothing_item=mydb.clothing_items.get_one(data),current_user = user.User.getById({'id': session['user_id']}))

@app.route('/clothingitems/edit/<int:id>',methods=['POST'])
def update(id):
    if not mydb.clothing_items.validate_clothingitems(request.form):
        return redirect(f'/clothingitems/edit/{id}')
    data ={
    "name" : request.form['name'],
    "cost" : request.form['cost'],
    "material" : request.form['material'],
    "style" : request.form['style'],
    "primary_color" : request.form['primary_color'],
    "secondary_color" : request.form['secondary_color'],
    "location_aquired" : request.form['location_aquired'],
    "img_path" : request.form['img_path'],
    "created_at" : request.form['created_at'],
    "updated_at" : request.form['updated_at'],
    "id" : id
    }
    mydb.clothing_items.update(data)
    return redirect('/clothingitems')

@app.route('/clothingitem/show/<int:id>')
def show(id):
    data ={ 
        "id":id
    }
    return render_template("view_outfit_items.html",clothing_item=mydb.clothing_items.get_one(data),current_user = user.User.getById({'id': session['user_id']}))

@app.route("/clothingitems/create")
def clothingitems_create_page():
    if 'user_id' in session:
        return render_template('create_outfit.html', 
        current_user = user.User.getById({'id': session['user_id']}),
        all_clothingitems = mydb.clothing_items.get_all_clothingitems()
        )
    return render_template("index.html")

