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