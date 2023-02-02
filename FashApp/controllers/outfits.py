from FashApp import app
from flask import render_template, request, redirect, session, flash
from FashApp.models import user
from FashApp.models import clothing_category
from FashApp.models import clothing_item

from datetime import datetime


@app.route("/new_outfit")
def new_outfit():
    current_user = user.User.get_one(session['users_id'])
    clothing_by_category = {}
    all_category = clothing_category.Clothing_catagories.get_all()
    for category in all_category:
        clothing_by_category[category.name] = clothing_item.Clothing_items.get_clothing_by_category(category.id)
    print(category)
    for clothing in clothing_by_category:
        print("Clothing in category", clothing_by_category[clothing])
    return render_template("create_outfit.html", current_user = current_user, clothing_by_category = clothing_by_category, all_category = all_category)


# this is just to remove the name from the request form so the array just has ids
def remove_first(array):
    resultArray = []
    for x in range(len(array) - 1) :
        resultArray.append(array[(x+1)])
    return resultArray



@app.route("/create_outfit", methods = ['POST'])
def save_new_outfit():
    clothingIdArray = []
    dictionary = request.form.to_dict()
    print(dictionary)
    for category in dictionary:
            clothingIdArray.append(dictionary[category])
    clothingIdArray = remove_first(clothingIdArray)
    print(clothingIdArray)
    # clothing id array contains the ids of the clothing items selected
    return(redirect('/home'))


