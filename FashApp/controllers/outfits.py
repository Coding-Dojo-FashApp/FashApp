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
    categories = clothing_category.Clothing_catagories.get_all()
    for category in categories:
        clothing_by_category[category.name] = clothing_item.Clothing_items.get_clothing_by_category(category.id)
    print(category)
    for clothing in clothing_by_category:
        print("Clothing in category", clothing_by_category[clothing])
    return render_template("create_outfit.html", current_user = current_user, clothing_by_category = clothing_by_category)