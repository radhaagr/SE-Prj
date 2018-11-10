from sqlalchemy import and_, func, between
from flask_login import login_required, current_user
from flask import Flask, render_template, redirect, url_for, session, g, Blueprint, request, jsonify, url_for

import datetime
from datetime import datetime as dt
from datetime import timedelta

from FoodOrderClient import db, app, socketio
import helper

from .models import Users, Restaurant, FoodItem, Cart
import json

mod_client = Blueprint('client', __name__)



#To display the home page after retrieval from database

@mod_client.route('/', methods=['GET', 'POST'])
def show_home():
    restaurant_objs = Restaurants.query.filter().all()
    restaurants = []
    for restaurant in restaurant_objs:
        rest_json = restaurant.json()
        cur_rest_id = restaurant.rest_id
        item_objets = FoodItem.query.filter_by(rest_id = cur_rest_id).all()
        Items = []
        for item in item_objets:
            item_json = item.json()
            Items.append(item_json)
        rest_json[0]['Items'] = Items
        restaurants.append(rest_json)

    return searchedRestaurants,200


#display the cart but it needs login
@app.route("/cart")
@login_required
def cart():
    email = request.form['email']
    user = Users.query.filter_by(email=email).first()
    if user is not None and user.authenticate(password):
        user.authenticated = True
        cur_id = user.id
        carts  = Cart.query.filter_by(user_id = cur_id).all()
        user_json = user.json()
        totalPrice = 0
        Cart = []
        Items = []
        totalprice = 0
        for cart in carts:
            id = cart.id
            cur_prod = cart.product_id
            cur_item = FoodItem.query.filter_by(item_id = cur_prod).all()
            price = cur_item.price
            item_quantity =  cart.quantity
            totalprice = totalprice + (item_quantity * price)

            prod_json = cur_item.json()
            Items.append(prod_json)
    else:
        #ask user to login before it is able to see the cart as cart is for any user
        render_template("login.html")
    return json.dumps({"User" : user_json, "items": Items, "Total_Price" : total_price })



@app.route("/addToCart", methods=['GET', 'POST'])
@login_required
def addToCart():
    email = request.form['email']
    user = Users.query.filter_by(email=email).first()
    if user is None:
        render_template("login.html")
    else:
        productId = int(request.args.get('productId'))
        id  = user.id
        getProduct = Cart.query.filter_by(user_id = id, product_id = productId ).first()
        #if no product is present for given user id and product id
        #create a new cart and and add to it
        if( getProduct is None) :
            cartNew = Cart( user_id =  user.id , product_id = productId, quantity = 1 )
            db.session.add(cartNew)
            db.session.commit()
        else:
            #else increment the qunatity and commit the session
            getProduct.quantity += 1
            db.session.commit()

    return redirect(url_for('root'))


#similarty write for removeFromCart



@app.route("/RemoveFromCart", methods=['GET', 'POST'])
@login_required
def addToCart():
    email = request.form['email']
    user = Users.query.filter_by(email=email).first()
    if user is None:
        render_template("login.html")
    else:
        productId = int(request.args.get('productId'))
        id  = user.id
        getProduct = Cart.query.filter_by(user_id = id, product_id = productId ).first()
        #if no product is present for given user id and product id
        #create a new cart and and add to it
        if( getProduct is None) :
            #Print Error login
            print "Error"
        else:
            #else increment the qunatity and commit the session
            db.session.query(Foo).filter_by(user_id = id, product_id = productId).delete()
            db.session.commit()

    return redirect(url_for('root'))
