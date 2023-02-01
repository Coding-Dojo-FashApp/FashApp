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