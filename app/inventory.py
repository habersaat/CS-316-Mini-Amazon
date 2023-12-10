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
        seller_orders = []  #initialize an empty list

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

@bp.route('/new_order')
def new_order():
    return render_template('neworder.html')

@bp.route('/handle_new_order', methods=['POST'])
def handle_new_order():
    # Get data from the form submission
    order_id = request.form.get('order_id')
    seller_id = request.form.get('seller_id')
    customer_id = request.form.get('customer_id')
    total_amount = request.form.get('total_amount')
    recipient_address = request.form.get('recipient_address')
    order_status = request.form.get('order_status')
    delivery_date = request.form.get('delivery_date')

    return render_template('inventory.html')