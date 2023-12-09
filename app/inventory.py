from flask import render_template, redirect, url_for, flash, request
from werkzeug.urls import url_parse
from flask_login import login_user, logout_user, current_user
from flask_wtf import FlaskForm
from wtforms import IntegerField, PasswordField, BooleanField, SubmitField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo
import datetime


from .models.inventory import Inventory
from .models.orders import Order


from flask import Blueprint
from flask import request
bp = Blueprint('Inventory', __name__)


class SellerForm(FlaskForm):
    userID = IntegerField('Seller ID', validators=[DataRequired()])
    submit = SubmitField('View Inventory')



@bp.route('/inventory', methods=['GET', 'POST'])
def sellers():
    form = SellerForm()
    seller_id = request.args.get('seller_id', type=int)
    page = request.args.get('page', 1, type=int)
    per_page = 10

    seller_orders = []  #initialize an empty list

    if request.method == 'POST' and form.validate_on_submit():
        seller_id = form.userID.data
        return redirect(url_for('Inventory.sellers', seller_id=seller_id))

    if seller_id:
        available_inventory = Inventory.get_inventory_by_sid(seller_id, page, per_page)
        total_inventory_count = Inventory.get_count_by_sid(seller_id)
        seller_orders = Order.get_orders_by_user_id(seller_id)  #active orders of the seller
    else:
        available_inventory = []
        total_inventory_count = 0

    if not available_inventory and request.method == 'GET':
        flash('No inventory items found or invalid Seller ID.')

    #pass both inventory and orders data 
    return render_template('inventory.html', form=form, seller_id=seller_id,
                           available_inventory=available_inventory,
                           total_inventory_count=total_inventory_count,
                           seller_orders=seller_orders,  # Add this line to pass orders
                           page=page, per_page=per_page)

@bp.route('/seller/<int:seller_id>')
def view_seller_orders(seller_id):
    seller_orders = Order.query.filter_by(user_id=seller_id).all()  # Assuming 'user_id' is the seller's ID
    return render_template('inventory.html', seller_orders=seller_orders)