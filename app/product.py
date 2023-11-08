from flask import render_template, redirect, url_for, flash, request
from werkzeug.urls import url_parse
from flask_login import login_user, logout_user, current_user
from flask_wtf import FlaskForm
from wtforms import IntegerField, PasswordField, BooleanField, SubmitField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo

from .models.product import Product


from flask import Blueprint
bp = Blueprint('product', __name__)

@bp.route('/product', methods=['GET', 'POST'])
def product_info():
    prod_id = request.args.get('id')
    product = Product.get_all_info_by_id(prod_id)

    return render_template('product.html', title='Product Info', avail_products=product)