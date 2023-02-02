from FashApp import app
from flask import render_template, request, redirect, session, flash
from FashApp.models import user
from FashApp.models import clothing_category
from FashApp.models import clothing_item
from FashApp.models import outfit
from datetime import datetime
import json


@app.route("/new_outfit")
def new_outfit():
    if 'users_id' not in session:
        return redirect("/")
    current_user = user.User.get_one(session['users_id'])
    all_category = clothing_category.Clothing_categories.get_all()
    clothing_by_category = {}
    for category in all_category:
        clothing_by_category[category.name] = clothing_item.Clothing_items.get_clothing_by_category(category.id)
    for clothing in clothing_by_category:
        print(f"Clothing in category {clothing}", clothing_by_category[clothing])
    return render_template("create_outfit.html", current_user = current_user, clothing_by_category = clothing_by_category, all_category = all_category)


# this is just to remove the name from the request form so the array just has ids
def remove_first(array):
    resultArray = []
    for x in range(len(array) - 1) :
        resultArray.append(array[(x+1)])
    return resultArray



@app.route("/create_outfit", methods = ['POST'])
def save_new_outfit():
    if 'users_id' not in session:
        return redirect("/")
    # clothingIdArray code was removed because it didn't account for name, description
    # if the user didn't want to select a particular item.

    data = {
        "name" : request.form['name'],
        "description" : request.form['description'],
        "user_id" : session['users_id']
    }
    categories = clothing_category.Clothing_categories.get_all()
    
    outfit_items = []
    for category in categories:
        if request.form[category.name] and  request.form[category.name] != 'none':
            outfit_items.append(int(request.form[category.name]))
            
    data['outfit_items'] = json.dumps(outfit_items)
            
    outfit.Outfit.save_outfit(data)
    
    return(redirect('/home'))

@app.route('/show_outfit/<int:id>')
def show_outfit(id):
    a_outfit = outfit.Outfit.get_one_by_id(id)
    current_user = user.User.get_one(session['users_id'])
    all_category = clothing_category.Clothing_categories.get_all()
    return render_template("view_outfit_items.html", outfit = a_outfit,
                current_user = current_user, all_category = all_category)
    
@app.route('/edit_outfit/<int:id>')
def edit_outfit(id):
    a_outfit = outfit.Outfit.get_one_by_id(id)
    current_user = user.User.get_one(session['users_id'])
    all_category = clothing_category.Clothing_categories.get_all()
    clothing_by_category = {}
    for category in all_category:
        clothing_by_category[category.name] = clothing_item.Clothing_items.get_clothing_by_category(category.id)
    return render_template("edit_outfit.html", outfit = a_outfit,
                current_user = current_user, clothing_by_category = clothing_by_category, all_category = all_category)


@app.route("/update_outfit", methods = ['POST'])
def update_outfit():
    if 'users_id' not in session:
        return redirect("/")
    # clothingIdArray code was removed because it didn't account for name, description
    # if the user didn't want to select a particular item.

    data = {
        "outfit_id" : request.form['outfit_id'],
        "name" : request.form['name'],
        "description" : request.form['description'],
        "user_id" : session['users_id']
    }
    categories = clothing_category.Clothing_categories.get_all()
    
    outfit_items = []
    for category in categories:
        if request.form[category.name] and  request.form[category.name] != 'none':
            outfit_items.append(int(request.form[category.name]))
            
    data['outfit_items'] = json.dumps(outfit_items)
            
    outfit.Outfit.update_outfit(data)
    
    return redirect('/home')

@app.route('/delete_outfit/<int:id>')
def delete_outfit(id):
    outfit.Outfit.delete_outfit(id)
    return redirect('/home')



