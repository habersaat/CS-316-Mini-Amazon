from flask import render_template, redirect, url_for, flash, request, jsonify
from werkzeug.urls import url_parse
from flask_login import login_user, logout_user, current_user
from flask_wtf import FlaskForm
from wtforms import IntegerField, PasswordField, BooleanField, SubmitField, StringField, TextAreaField, FloatField, FileField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo
import datetime

from .models.inventory import Inventory

from flask import Blueprint
bp = Blueprint('newproduct', __name__)


class NewProductForm(FlaskForm):
    userID = IntegerField('Product ID', validators=[DataRequired()])
    submit = SubmitField('Submit')

    productname = StringField('Product Name', validators=[DataRequired()])
    shortdescription = TextAreaField('Short Description', validators=[DataRequired()])
    longdescription = TextAreaField('Long Description', validators=[DataRequired()])
    category = StringField('Category', validators=[DataRequired()])
    tags = StringField('Tags')
    price = FloatField('Price', validators=[DataRequired()])
    quantity = IntegerField('Quantity', validators=[DataRequired()])
    imageurl = StringField('Image URL', validators=[DataRequired()])
    submit = SubmitField('List Product')

@bp.route('/new', methods=['GET', 'POST'])
def newproduct():
    form = NewProductForm()
    addedProduct = Inventory.add_product_to_inventory(current_user.id, form.productname.data, form.shortdescription.data, form.longdescription.data, form.category.data, form.tags.data, form.imageurl.data, form.price.data, form.quantity.data)
    if addedProduct:
            return redirect(url_for('seller.seller'))
    return render_template('newproduct.html', title='New Product', form=form, addedProduct=addedProduct)
