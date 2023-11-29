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
            return redirect(url_for('index.index_post'))

        # get the k most expensive products
        products = Product.k_most_expensive(k)

    else:
        # products = Product.get_k_page_of_n(currentPage, n)
        # products = Product.get_all(True)

        if request.args.get('query') is not None:
            if request.args.get('filter') == 'price_asc':
                products = Product.get_k_page_of_n_with_search_price_asc(currentPage, n, request.args.get('query'))
            elif request.args.get('filter') == 'price_desc':
                products = Product.get_k_page_of_n_with_search_price_desc(currentPage, n, request.args.get('query'))
            elif request.args.get('filter') == 'name_asc':
                products = Product.get_k_page_of_n_with_search_name_asc(currentPage, n, request.args.get('query'))
            elif request.args.get('filter') == 'name_desc':
                products = Product.get_k_page_of_n_with_search_name_desc(currentPage, n, request.args.get('query'))
            elif request.args.get('filter') == 'rating_asc':
                products = Product.get_k_page_of_n_with_search_rating_asc(currentPage, n, request.args.get('query'))
            elif request.args.get('filter') == 'rating_desc':
                products = Product.get_k_page_of_n_with_search_rating_desc(currentPage, n, request.args.get('query'))
            else:
                products = Product.get_k_page_of_n_with_search(currentPage, n, request.args.get('query'))

        else:
            if request.args.get('filter') == 'price_asc':
                products = Product.get_k_page_of_n_price_asc(currentPage, n)
            elif request.args.get('filter') == 'price_desc':
                products = Product.get_k_page_of_n_price_desc(currentPage, n)
            elif request.args.get('filter') == 'name_asc':
                products = Product.get_k_page_of_n_name_asc(currentPage, n)
            elif request.args.get('filter') == 'name_desc':
                products = Product.get_k_page_of_n_name_desc(currentPage, n)
            elif request.args.get('filter') == 'rating_asc':
                products = Product.get_k_page_of_n_rating_asc(currentPage, n)
            elif request.args.get('filter') == 'rating_desc':
                products = Product.get_k_page_of_n_rating_desc(currentPage, n)
            else:
                products = Product.get_k_page_of_n(currentPage, n)

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

