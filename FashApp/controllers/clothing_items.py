from flask_app import app
from flask import render_template, request, redirect, session, flash
from flask_app.models import user, outfit, clothing_item
mydb = 'fashion_inventory'


@app.route('/clothingitems')
def index():
    if 'user_id' in session:
        return render_template('index.html', 
        current_user = user.User.getById({'id': session['user_id']}),
        all_clothingitems = clothing_items.fashion_inventory.get_all_clothingitems()
        )
    return redirect('/')

@app.route('/clothingitems/destroy/<int:id>')
def destroy(id):
    data ={
        'id': id
    }
    clothing_items.fashion_inventory.destroy(data)
    return redirect('/clothingitems')

@app.route('/clothingitems/edit/<int:id>')
def edit(id):
    data ={ 
    "id":id
    }
    return render_template("edit.html",clothing_items=clothing_items.fashion_inventory.get_one(data),current_user = users.User.getById({'id': session['user_id']}))

@app.route('/clothingitems/edit/<int:id>',methods=['POST'])
def update(id):
    if not clothing_items.fashion_inventory.validate_outfit(request.form):
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
    clothing_items.fashion_inventory.update(data)
    return redirect('/clothingitems')

@app.route('/clothingitem/show/<int:id>')
def show(id):
    data ={ 
        "id":id
    }
    return render_template("view_outfit_items.html",clothing_items=clothing_items.fashion_inventory.update(data),current_user = users.User.getById({'id': session['user_id']}))

@app.route("/clothingitems/create")
def outfit_create_page():
    if 'user_id' in session:
        return render_template('create_outfit.html', 
        current_user = user.User.getById({'id': session['user_id']}),
        all_clothingitems = clothing_items.fashion_inventory.get_all_clothingitems()
        )
    return render_template("index.html")

@app.route('/post/create',methods=['POST'])
def clothingitems_display_page():
    if not clothing_items.fashion_inventory.validate_clothingitem(request.form):
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
    result = clothing_items.fashion_inventory.save(data)
    return redirect('/clothingitems')