from flask import render_template, redirect, url_for, flash, request
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
    submit = SubmitField('See Reviews')

@bp.route('/reviews', methods=['GET', 'POST'])
def reviews():
    form = ReviewsForm()
    recent_reviews = Review.five_most_recent_by_user_id(form.userID.data)
    print("Five most recent reviews: ", recent_reviews)
    return render_template('reviews.html', title='Reviews', form=form, recent_reviews=recent_reviews)

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