from flask import Flask, render_template, redirect, session, request
from flask_app import app
from flask_app.models.user import User
from flask_app.models.matcha import Matcha
from flask_app.models.review import Review
from flask_app.models.bag import Bag
from flask import flash


@app.route("/bag")
def shopping_bag():
    if 'user_id' not in session:
        flash("You must be logged in to access the dashboard.")
        return redirect('/')
    user = User.get_by_id(session["user_id"])
    bags = Bag.get_all_matchas_in_bag()
    # matchas = Matcha.get_all_matchas()
    # review = Review.get_all_reviews()
    
    return render_template("shopping_bag.html", bags=bags, user=user)
    

@app.route("/add_item", methods = ["POST"])
def add_item():
    if not Bag.add_to_bag(request.form):
        return redirect('/faq')
    print(request.form)
    matcha_name = request.form['matcha_name']
    matcha_names = matcha_name[2][0]
    
    print(f'{matcha_names}***************+++++++++')
    return redirect('/home')


@app.route("/matcha/delete/<int:matcha_id>")
def remove_item(matcha_id):
    Bag.remove_from_bag(matcha_id)
    return redirect("/bag")