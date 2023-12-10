from flask import render_template, redirect, url_for, flash, request, jsonify
from werkzeug.urls import url_parse
from flask_login import login_user, logout_user, current_user
from flask_wtf import FlaskForm
from wtforms import IntegerField, PasswordField, BooleanField, SubmitField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo, Optional

from .models.seller_review import SellerReview

from flask import Blueprint
bp = Blueprint('seller_reviews', __name__)


class SellerReviewsForm(FlaskForm):
    sellerID = IntegerField('Seller ID', validators=[Optional()])
    submit = SubmitField('See Seller Reviews')

@bp.route('/seller_reviews', methods=['GET', 'POST'])
def seller_reviews():
    form = SellerReviewsForm()
    page = request.args.get('page', 1, type=int)
    user_id = request.args.get('user_id', type=int)
    seller_id = request.args.get('seller_id', type=int) 

    if form.validate_on_submit():
        seller_id = form.sellerID.data 
        return redirect(url_for('seller_reviews.seller_reviews', page=1, user_id=current_user.id, seller_id=seller_id))

    recent_reviews = SellerReview.get_paginated_reviews(page, user_id=current_user.id, seller_id=seller_id)
    total_reviews = SellerReview.count_all_reviews(user_id=current_user.id, seller_id=seller_id)
    total_pages = (total_reviews + 9) // 10

    return render_template('seller_reviews.html', title='Seller Reviews', form=form, recent_reviews=recent_reviews, page=page, total_pages=total_pages, user_id=current_user.id, seller_id=seller_id)

@bp.route('/submit_seller_review', methods=['POST'])
def submit_seller_review():
    data = request.json
    user_id = data['user_id']
    seller_id = data['seller_id']
    rating = data['rating']
    comment = data['comment']
    
    try:
        new_review_id = SellerReview.create_review(seller_id, user_id, rating, comment)
        return jsonify({"success": True, "review_id": new_review_id}), 201
    except ValueError as e:
        return jsonify({"success": False, "message": str(e)}), 400

@bp.route('/remove_seller_review', methods=['POST'])
def remove_seller_review():
    data = request.json
    print(data) 
    user_id = data['user_id']
    seller_id = data['seller_id']

    if not current_user.is_authenticated:
        return jsonify({"success": False, "message": "You must be logged in to remove a review."}), 400
    elif not SellerReview.has_reviewed(user_id, seller_id):
        return jsonify({"success": False, "message": "You have not reviewed this seller."}), 400

    try:
        SellerReview.remove_review(user_id, seller_id)
        return jsonify({"success": True}), 200
    except Exception as e:
        return jsonify({"success": False, "message": str(e)}), 400
    
@bp.route('/edit_seller_review', methods=['POST'])
def edit_seller_review():
    data = request.json
    user_id = data['user_id']
    seller_id = data['seller_id']
    rating = data['rating']
    comment = data['comment']

    if not current_user.is_authenticated:
        return jsonify({"success": False, "message": "You must be logged in to edit a review."}), 400
    elif not SellerReview.has_reviewed(user_id, seller_id):
        return jsonify({"success": False, "message": "You have not reviewed this seller."}), 400

    try:
        SellerReview.edit_review(user_id, seller_id, rating, comment)
        return jsonify({"success": True}), 200
    except Exception as e:
        return jsonify({"success": False, "message": str(e)}), 400
    
    