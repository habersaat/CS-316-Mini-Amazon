from flask import render_template, redirect, url_for, flash, request
from werkzeug.urls import url_parse
from flask_login import login_user, logout_user, current_user
from flask_wtf import FlaskForm
from wtforms import IntegerField, PasswordField, BooleanField, SubmitField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo

from .models.inventory import Inventory
from .models.cart import Cart
from .models.product import Product
from .models.inventory import Inventory
from .models.review import Review
from .models.seller_review import SellerReview
from .models.user import User
from .models.tag import Tag

from flask import Blueprint
bp = Blueprint('carts', __name__)


class CartsForm(FlaskForm):
    userID = IntegerField('User ID', validators=[DataRequired()])
    submit = SubmitField('My Cart')

@bp.route('/carts', methods=['GET', 'POST'])
def carts():
    form = CartsForm()
    if not current_user.is_authenticated:
        return
    uid = current_user.id
    cart_items = Cart.items_by_uid(uid)
    findtotal = sum([item.price*item.quantity for item in cart_items])
    return render_template('carts.html', title='My Cart', form=form, cart_items=cart_items, findtotal=findtotal)

@bp.route('/carts/minus/<pid>,<quantity>,<price>', methods = ['GET', 'POST'])
def minus_item(pid, quantity, price):
    form = CartsForm()
    uid = current_user.id
    Cart.decrease_quantity(uid,pid,int(quantity))
    cart_items = Cart.items_by_uid(uid)
    return render_template('carts.html', title = "My Cart", form=form, cart_items=cart_items)

@bp.route('/carts/add/<pid>,<quantity>,<price>', methods = ['GET', 'POST'])
def add_item(pid, quantity,price):
    form = CartsForm()
    uid = current_user.id
    Cart.increase_quantity(uid,pid,int(quantity))
    cart_items = Cart.items_by_uid(uid)
    return render_template('carts.html', title = "My Cart", form=form, cart_items=cart_items)

@bp.route('/carts/<productId>/<quantity>/<sellerId>', methods = ['GET','POST'])
def addToCart(productId, quantity, sellerId):
    form = CartsForm()
    uid = current_user.id
    if (str(quantity)=="NaN"):
            quantity=1
    Cart.add_to_cart(uid, productId, quantity, sellerId)
    cart_items = Cart.items_by_uid(uid)
    return render_template('carts.html', title = "My Cart", form=form, cart_items=cart_items)

@bp.route('/carts/delete/<pid>/<sid>', methods = ['GET', 'DELETE'])
def delete_item(pid, sid):
    form = CartsForm()
    uid = current_user.id
    Cart.delete_from_cart(uid, pid, sid)
    cart_items = Cart.items_by_uid(uid)
    return render_template('carts.html', title = "My Cart", form=form, cart_items=cart_items)

@bp.route('/orders/', methods = ['GET','POST'])
def submit_order():
    form = CartsForm()
    uid = current_user.id
    sid = request.args.get('sid', type=int)
    order_items = Cart.items_by_uid(uid)

    # get seller reviews
    seller_reviews = SellerReview.get_paginated_reviews_by_seller_id(sid)

    has_reviewed_seller = False
    if current_user.is_authenticated and current_user.id in [seller_review.user_id for seller_review in seller_reviews]:
        has_reviewed_seller = True

    return render_template('orders.html', title = "My Orders", form=form, order_items=order_items, has_reviewed_seller=has_reviewed_seller)