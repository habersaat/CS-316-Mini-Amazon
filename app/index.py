from flask import render_template, request, redirect, url_for, flash
from flask_login import current_user
import datetime

from .models.product import Product
from .models.purchase import Purchase

from flask import Blueprint
bp = Blueprint('index', __name__) 

# Create index that gives the top k most expensive products which are passed in through a form submit
@bp.route('/', methods=['GET', 'POST'])
def index():
    # get the k value from the url parameters. For reference, the url looks like: /price_desc?k=5
    k = request.args.get('price_desc')

    # if k is not None, then convert it to an int
    if k is not None and k != '':
        k = int(k)

        # ensure k is a positive integer
        if k < 0:
            flash('k must be a positive integer')
            return redirect(url_for('index.index_post'))

        # get the k most expensive products
        products = Product.k_most_expensive(k)

    else:
        # get all available products for sale:
        products = Product.get_all(True)

    # find the products current user has bought:
    if current_user.is_authenticated:
        purchases = Purchase.get_all_by_uid_since(
            current_user.id, datetime.datetime(1980, 9, 14, 0, 0, 0))
    else:
        purchases = None
    # render the page by adding information to the index.html file
    return render_template('index.html',
                        avail_products=products,
                        purchase_history=purchases)

