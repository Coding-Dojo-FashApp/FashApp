from FashApp import app

from flask import render_template,request, redirect,session, url_for, flash
from datetime import datetime
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)
dateFormat = "%m/%d/%Y %I:%M %p"
import os
from FashApp import render_template, redirect, session, request, flash
from FashApp.models import user, outfit, clothing_item, clothing_category
mydb = 'fashion_inventory'



@app.route('/post/create',methods=['POST'])
def clothingitems_display_page():
    if not clothing_item.fashion_inventory.validate_clothingitem(request.form):
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
    result = clothing_item.fashion_inventory.save(data)
    return redirect('/clothingitems')


@app.route('/clothingitems')
def dashboard():
    if 'user_id' in session:
        return render_template('index.html', 
        current_user = user.User.getById({'id': session['user_id']}),
        all_clothingitems = mydb.clothing_items.get_all_clothingitems()
        )
    return redirect('/')


@app.route('/create_category', methods = ['Post']) 
def new_category():
    data = { 
        "user_id": request.form['user_id'],
        "name": request.form['name']
    } 
    clothing_category.Clothing_catagories.save(data)
    return redirect('/home')

@app.route('/getintocategory/<int:id>/<int:user_id>/', methods=['get'])
def getintocategory(id,user_id):
    data = {
        "id": id,
        "user_id" : user_id
    }
    print(data)
    return render_template('new_item.html',current_user = user.User.get_one({'id': session["users_id"]}), all_category = clothing_category.Clothing_catagories.get_all(), clothingcatergoryid=clothing_category.Clothing_catagories.get_category_by_id(id), all_clothing = clothing_item.Clothing_items.show_clothing_by_user(data))

@app.route('/new_clothing/<int:id>/<int:user_id>/', methods = ['post'])
def create_item(id,user_id):
	newdata = {
		"id": id,
		"user_id" : user_id
		}
	if 'file' not in request.files: 
		flash('No file part')
	if not clothing_item.Clothing_items.validate_post(request.form):
		
		return redirect(f'/getintocategory/{id}/{user_id}/')
	file = request.files['file']
	if file.filename == '': 
		flash('No image selected for uploading')
		return redirect(request.url) 
	if file and allowed_file(file.filename):
		filename = secure_filename(file.filename) 
		file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
		print(file.filename)
		print('upload_image filename: ' + filename)
		flash('Image successfully uploaded and displayed below')
		data = {
		"name": request.form['name'],
		"material": request.form['material'],
		"cost": request.form['cost'],
        "style": request.form['style'],
		"primary_color": request.form['primary_color'],
		"secondary_color": request.form['secondary_color'], 
		"location_aquired": request.form['location_aquired'],
        "img_path": filename,
		"user_id": request.form['user_id'],
        "clothing_catagory_id": request.form['clothing_catagory_id']

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
    return render_template("edit.html",clothing_item=mydb.clothing_items.get_one(data),current_user = users.User.getById({'id': session['user_id']}))

@app.route('/clothingitems/edit/<int:id>',methods=['POST'])
def update(id):
    if not fashion_inventory.clothing_items.validate_clothingitems(request.form):
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
    return render_template("view_outfit_items.html",clothing_item=mydb.clothing_items.get_one(data),current_user = users.User.getById({'id': session['user_id']}))

@app.route("/clothingitems/create")
def clothingitems_create_page():
    if 'user_id' in session:
        return render_template('create_outfit.html', 
        current_user = user.User.getById({'id': session['user_id']}),
        all_clothingitems = mydb.clothing_items.get_all_clothingitems()
        )
    return render_template("index.html")

