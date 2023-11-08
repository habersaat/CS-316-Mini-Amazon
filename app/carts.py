from flask import render_template, redirect, url_for, flash, request
from werkzeug.urls import url_parse
from flask_login import login_user, logout_user, current_user
from flask_wtf import FlaskForm
from wtforms import IntegerField, PasswordField, BooleanField, SubmitField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo

from .models.cart import Cart


from flask import Blueprint
bp = Blueprint('carts', __name__)


class CartsForm(FlaskForm):
    userID = IntegerField('User ID', validators=[DataRequired()])
    submit = SubmitField('My Cart')

@bp.route('/carts', methods=['GET', 'POST'])
def carts():
    form = CartsForm()
    uid = request.args.get('id')
    cart_items = Cart.items_by_uid(uid)
    print("The cart items are: ", cart_items)
    return render_template('carts.html', title='My Cart', form=form, cart_items=cart_items)