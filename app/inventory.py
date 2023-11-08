from flask import render_template, redirect, url_for, flash, request
from werkzeug.urls import url_parse
from flask_login import login_user, logout_user, current_user
from flask_wtf import FlaskForm
from wtforms import IntegerField, PasswordField, BooleanField, SubmitField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo
import datetime

# from .models.seller import Seller
from .models.inventory import Inventory


from flask import Blueprint
bp = Blueprint('Inventory', __name__)


class SellerForm(FlaskForm):
    userID = IntegerField('Seller ID', validators=[DataRequired()])
    submit = SubmitField('View Inventory')

@bp.route('/inventory', methods=['GET', 'POST'])
def sellers():
    form = SellerForm()
    available_inventory = Inventory.get_inventory_by_sid(form.userID.data)
    print("Inventory: ", available_inventory)
    return render_template('inventory.html', title='Inventory', form=form, available_inventory=available_inventory)