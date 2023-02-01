from FashApp import app
from flask import render_template,request, redirect,session, url_for, flash
from FashApp.models import user
from FashApp.models import clothing_category
from FashApp.models import clothing_item
from datetime import datetime
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)
dateFormat = "%m/%d/%Y %I:%M %p"
import os


from werkzeug.utils import secure_filename

ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])

def allowed_file(filename):
	return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


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
    return render_template('new_item_copy.html',current_user = user.User.get_one(session["users_id"]), all_category = clothing_category.Clothing_catagories.get_all(), clothingcatergoryid=clothing_category.Clothing_catagories.get_category_by_id(id), all_clothing = clothing_item.Clothing_items.show_clothing_by_user(data))

@app.route('/new_clothing', methods=['get'])
def new_clothing():
    
    return render_template('new_item.html',current_user = user.User.get_one(session["users_id"]), all_category = clothing_category.Clothing_catagories.get_all(),  all_clothing = clothing_item.Clothing_items.show_clothing_by_user(session['users_id']))

@app.route('/create_clothing', methods=['POST'])
def create_clothing():
    
	if 'file' not in request.files: 
		flash('No file part')
	if not clothing_item.Clothing_items.validate_post(request.form):
		
		return redirect('/new_clothing')
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
			"clothing_catagory_id": request.form['category_id']
		}
    
		clothing_item.Clothing_items.insert_clothing_items(data)
		print(file.filename, "this is the file name")
	
		return redirect('/home') 
	else:
		flash('Allowed image types are -> png, jpg, jpeg, gif') 
		return redirect(request.url)

@app.route('/edit_clothing/<int:id>')
def edit_clothing(id):
    clothing = clothing_item.Clothing_items.get_clothing_by_id(id)
    
    
    return render_template('edit.html',current_user = user.User.get_one(session["users_id"]), 
        all_category = clothing_category.Clothing_catagories.get_all(),  
        all_clothing = clothing_item.Clothing_items.show_clothing_by_user(session['users_id']),
        clothing = clothing)




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
		}
    
		clothing_item.Clothing_items.insert_clothing_items(data)
		print(file.filename, "this is the file name")
	
		return redirect('/home') 
	else:
		flash('Allowed image types are -> png, jpg, jpeg, gif') 
		return redirect(request.url)

@app.route('/display/<filename>')
def display_image(filename):
	return redirect(url_for('static', filename='uploads/' + filename), code=301)


@app.route('/category_clothing_list/<int:id>')
def clothing_list(id):
	if 'users_id' in session:
		clothing_in_category= clothing_item.Clothing_items.get_clothing_by_category(id)
		return render_template('clothing_list.html',current_user = user.User.get_one(session["users_id"]), 
            category = clothing_category.Clothing_catagories.get_category_by_id(id), 
            all_category = clothing_category.Clothing_catagories.get_all(), clothing_in_category=clothing_in_category)
	return redirect('/')

@app.route('/view_clothing/<int:id>')
def view_clothing(id):
    a_clothing_item = clothing_item.Clothing_items.get_clothing_by_id(id)
    all_category = clothing_category.Clothing_catagories.get_all()
    return render_template("view_clothing.html", clothing_item = a_clothing_item, all_category = all_category)