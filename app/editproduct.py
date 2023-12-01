from flask import render_template, redirect, url_for, flash, request
from werkzeug.urls import url_parse
from werkzeug.datastructures import MultiDict
from flask_login import login_user, logout_user, current_user
from flask_wtf import FlaskForm
from wtforms import IntegerField, PasswordField, BooleanField, SubmitField, StringField, TextAreaField, FloatField, FileField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo
import datetime

from .models.inventory import Inventory
from .models.product import Product
from .models.tag import Tag

from flask import Blueprint
bp = Blueprint('editproduct', __name__)


class EditProductForm(FlaskForm):
    userID = IntegerField('ID', validators=[DataRequired()])
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

@bp.route('/edit/', methods=['GET', 'POST'])
def editproduct():
    form = EditProductForm()
    if current_user.is_authenticated:
        id = request.args.get('id')
        instance = Inventory.get_instance_by_id(id)

        tags = Tag.get_tagnames_by_pid(instance.pid)
        tags = ','.join(tags)
        
        name = Product.get(instance.pid).name
        updatedProduct = Inventory.update_product_in_inventory(instance.id, current_user.id, form.productname.data, form.shortdescription.data, form.longdescription.data, form.category.data, form.tags.data, form.imageurl.data, form.price.data, form.quantity.data)
        if updatedProduct:
            return redirect(url_for('seller.seller'))

    else:
        instance = None
    return render_template('editproduct.html', title='Edit Product', form=EditProductForm(formdata=MultiDict({
        'productname': name,
        'shortdescription': instance.description_short,
        'longdescription': instance.description_long,
        'category': instance.category,
        'tags': tags,
        'price': instance.price,
        'quantity': instance.quantity,
        'imageurl': instance.image_url
        })), instance=instance, updatedProduct=updatedProduct)

@bp.route('/delete/', methods=['GET', 'POST'])
def deleteproduct():
    if current_user.is_authenticated:
        id = request.args.get('id')
        instance = Inventory.get_instance_by_id(id)
        deletedProduct = Inventory.delete_product_from_inventory(instance.id)
        if deletedProduct:
            return redirect(url_for('seller.seller'))

    else:
        instance = None

    return None