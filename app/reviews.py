from flask import render_template, redirect, url_for, flash, request, jsonify
from werkzeug.urls import url_parse
from flask_login import login_user, logout_user, current_user
from flask_wtf import FlaskForm
from wtforms import IntegerField, PasswordField, BooleanField, SubmitField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo, Optional

from .models.review import Review

from flask import Blueprint
bp = Blueprint('reviews', __name__)


class ReviewsForm(FlaskForm):
    productID = IntegerField('Product ID', validators=[Optional()])
    submit = SubmitField('See Reviews')

@bp.route('/reviews', methods=['GET', 'POST'])
def reviews():
    form = ReviewsForm()
    page = request.args.get('page', 1, type=int)
    user_id = request.args.get('user_id', type=int)
    product_id = request.args.get('product_id', type=int) 

    if form.validate_on_submit():
        product_id = form.productID.data 
        return redirect(url_for('reviews.reviews', page=1, user_id=current_user.id, product_id=product_id))

    recent_reviews = Review.get_paginated_reviews(page, user_id=current_user.id, product_id=product_id)
    total_reviews = Review.count_reviews(user_id=current_user.id, product_id=product_id)
    total_pages = (total_reviews + 9) // 10

    return render_template('reviews.html', title='Reviews', form=form, recent_reviews=recent_reviews, page=page, total_pages=total_pages, user_id=current_user.id, product_id=product_id)

@bp.route('/submit_review', methods=['POST'])
def submit_review():
    data = request.json
    user_id = data['user_id']
    product_id = data['product_id']
    rating = data['rating']
    comment = data['comment']
    
    try:
        new_review_id = Review.create_review(product_id, user_id, rating, comment)
        return jsonify({"success": True, "review_id": new_review_id}), 201
    except ValueError as e:
        return jsonify({"success": False, "message": str(e)}), 400
    

@bp.route('/remove_review', methods=['POST'])
def remove_review():
    data = request.json
    print(data) 
    user_id = data['user_id']
    product_id = data['product_id']

    if not current_user.is_authenticated:
        return jsonify({"success": False, "message": "You must be logged in to remove a review."}), 400
    elif not Review.has_reviewed(user_id, product_id):
        return jsonify({"success": False, "message": "You have not reviewed this product."}), 400

    try:
        Review.remove_review(user_id, product_id)
        return jsonify({"success": True}), 200
    except Exception as e:
        return jsonify({"success": False, "message": str(e)}), 400


@bp.route('/edit_review', methods=['POST'])
def edit_review():
    data = request.json
    user_id = data['user_id']
    product_id = data['product_id']
    rating = data['rating']
    comment = data['comment']

    if not current_user.is_authenticated:
        return jsonify({"success": False, "message": "You must be logged in to edit a review."}), 400
    elif not Review.has_reviewed(user_id, product_id):
        return jsonify({"success": False, "message": "You have not reviewed this product."}), 400

    try:
        Review.edit_review(user_id, product_id, rating, comment)
        return jsonify({"success": True}), 200
    except Exception as e:
        return jsonify({"success": False, "message": str(e)}), 400