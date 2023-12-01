from flask import render_template, request, redirect, url_for, flash
from flask_login import current_user
import datetime

from .models.product import Product
from .models.purchase import Purchase

from flask import Blueprint
bp = Blueprint('index', __name__) 

visits = 0

# Create index that gives the top k most expensive products which are passed in through a form submit
@bp.route('/', methods=['GET', 'POST'])
def index():

    global visits
    visits += 1
    print(f'visits: {visits}')

    if visits == 1:
        Product.product_rating_init() # Can comment out for faster loading
        Product.inventory_init() # Can comment out for faster loading
        # Product.shipping_speed_init(current_user.longitude, current_user.latitude)

    # get the k value from the url parameters. For reference, the url looks like: /price_desc?k=5
    k = request.args.get('price_desc')

    # get the page number from the url parameters. For reference, the url looks like: /?page=2
    currentPage = request.args.get('page')
    if currentPage is not None and currentPage != '':
        currentPage = int(currentPage) - 1
    else:
        currentPage = 0

    # get the number of products per page from the url parameters. For reference, the url looks like: /?page=2&n=10
    n = request.args.get('n')
    if n is not None and n != '':
        n = int(n)
    else:
        n = 12

    # if k is not None, then convert it to an int
    if k is not None and k != '':
        k = int(k)

        # ensure k is a positive integer
        if k < 0:
            flash('k must be a positive integer')
            return redirect(url_for('index.index'))

        # get the k most expensive products
        products = Product.k_most_expensive(k)

    else:
        # products = Product.get_k_page_of_n(currentPage, n)
        # products = Product.get_all(True)
        query = request.args.get('query')
        fil = request.args.get('filter')
        if fil is not None:
            fil, order = fil.split('_')
        else:
            order = None
        category = request.args.get('category')

        products = Product.get_k_page_of_n(currentPage, n, fil, order, category, query)

        # get the stock of each product
        for product in products:
            product.stock = Product.count_product_quantity(product.id)

        length = Product.get_query_length(fil, order, category, query)

    # find the products current user has bought:
    if current_user.is_authenticated:
        purchases = Purchase.get_all_by_uid_since(
            current_user.id, datetime.datetime(1980, 9, 14, 0, 0, 0))
    else:
        purchases = None
    # render the page by adding information to the index.html file
    return render_template('index.html',
                        avail_products=products,
                        res=length,
                        purchase_history=purchases)

