from flask import render_template, redirect, url_for, flash, request, jsonify
from werkzeug.urls import url_parse
from flask_login import login_user, logout_user, current_user
from flask_wtf import FlaskForm
from wtforms import IntegerField, PasswordField, BooleanField, SubmitField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo

from .models.review import Review

from flask import Blueprint
bp = Blueprint('reviews', __name__)


class ReviewsForm(FlaskForm):
    userID = IntegerField('User ID', validators=[DataRequired()])
    productID = IntegerField('Product ID', validators=[DataRequired()])
    submit = SubmitField('See Reviews')

@bp.route('/reviews', methods=['GET', 'POST'])
def reviews():
    form = ReviewsForm()
    page = request.args.get('page', 1, type=int)
    user_id = request.args.get('user_id', type=int)
    product_id = request.args.get('product_id', type=int) 

    if form.validate_on_submit():
        user_id = form.userID.data
        product_id = form.productID.data 
        return redirect(url_for('reviews.reviews', page=1, user_id=user_id, product_id=product_id))

    recent_reviews = Review.get_paginated_reviews(page, user_id=user_id, product_id=product_id)
    total_reviews = Review.count_all_reviews(user_id=user_id, product_id=product_id)
    total_pages = (total_reviews + 9) // 10

    return render_template('reviews.html', title='Reviews', form=form, recent_reviews=recent_reviews, page=page, total_pages=total_pages, user_id=user_id, product_id=product_id)

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
    user_id = data['user_id']
    product_id = data['product_id']

    try:
        Review.remove_review(product_id, user_id)
        return jsonify({"success": True}), 200
    except Exception as e:
        return jsonify({"success": False, "message": str(e)}), 400