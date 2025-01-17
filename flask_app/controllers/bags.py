from flask import Flask, render_template, redirect, session, request
from flask_app import app
from flask_app.models.user import User
from flask_app.models.matcha import Matcha
from flask_app.models.review import Review
from flask_app.models.bag import Bag
from flask import flash
from werkzeug.datastructures import ImmutableMultiDict



@app.route('/home')
def home_page():
    if 'user_id' not in session:
        flash("You must be logged in to access the dashboard.")
        return redirect('/')
    user = User.get_by_id(session["user_id"])
    matchas = Matcha.get_all_matchas()
    review = Review.get_all_reviews()
    bags = Bag.get_all_matchas_in_bag()
    return render_template('home.html',bags = bags, user = user, matchas=matchas, review =review)


@app.route("/bag")
def shopping_bag():
    if 'user_id' not in session:
        flash("You must be logged in to access the dashboard.")
        return redirect('/')
    user = User.get_by_id(session["user_id"])
    bags = Bag.get_all_matchas_in_bag()
    totals = Bag.price_total()
    item = Bag.adding_item_amount()
    my_data = {'item_qty': 1}
    # matchas = Matcha.get_all_matchas()
    # review = Review.get_all_reviews()
    
    return render_template("shopping_bag.html",item=item,my_data = my_data, totals= totals, bags=bags, user=user)
    

@app.route("/add_item", methods = ["POST"])
def add_item():
    if not Bag.add_to_bag(request.form):
        return redirect('/faq')
    print(f"=====++++++======{request.form.getlist('matcha_id')[0]}")
    return redirect('/matchas')


@app.route("/matcha/delete/<int:matcha_id>")
def remove_item(matcha_id):
    Bag.remove_from_bag(matcha_id)
    return redirect("/bag")