import re
import string

from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SubmitField, TextAreaField, PasswordField
from wtforms.validators import (
    InputRequired,
    Length,
    Email,
    EqualTo,
    ValidationError
)

from .models import User, Post

class SearchForm(FlaskForm):
    search_query = StringField(
        "Query", validators=[InputRequired(), Length(min=1, max=100)]
    )
    submit = SubmitField("Search")


class PostCommentForm(FlaskForm):
    text = TextAreaField(
        "Comment", validators=[InputRequired(), Length(min=5, max=500)]
    )
    submit = SubmitField("Enter Comment")


class PostForm(FlaskForm):
    title = StringField(
        "Post Title", validators=[InputRequired(), Length(min=1, max=40)]
    )
    text = TextAreaField(
        "Post", validators=[InputRequired(), Length(min=5, max=5000)]
    )
    submit = SubmitField("Post")

    def validate_title(self, title):
        post = Post.objects(post_title=title.data).first()
        if post is not None:
            raise ValidationError("There exists another one of your posts with this title. Choose another title")


class RegistrationForm(FlaskForm):
    username = StringField(
        "Username", validators=[InputRequired(), Length(min=1, max=40)]
    )
    email = StringField("Email", validators=[InputRequired(), Email()])
    password = PasswordField("Password", validators=[InputRequired(), Length(min=12)])
    confirm_password = PasswordField(
        "Confirm Password", validators=[InputRequired(), EqualTo("password")]
    )
    submit = SubmitField("Sign Up")

    def validate_username(self, username):
        user = User.objects(username=username.data).first()
        if user is not None:
            raise ValidationError("Username is taken")

    def validate_email(self, email):
        user = User.objects(email=email.data).first()
        if user is not None:
            raise ValidationError("Email is taken")

    def validate_password(self, password):
        invalidcharacters= set(string.punctuation)

        if not any(char in invalidcharacters for char in password.data):
            raise ValidationError("Password must contain at least one special character")

        if not any(ele.isupper() for ele in password.data):
            raise ValidationError("Password must contain at least one upper case character")
            

class LoginForm(FlaskForm):
    username = StringField(
        "Username", validators=[InputRequired(), Length(min=1, max=40)]
    ) 
    password = PasswordField(
        "Password", validators=[InputRequired()]
    ) 
    submit = SubmitField("Login")


class UpdateUsernameForm(FlaskForm):
    username = StringField(
        "Username", validators=[InputRequired(), Length(min=1, max=40)]
    ) 
    submit = SubmitField("Update Username")

    def validate_username(self, username):
        user = User.objects(username=username.data).first()
        if user is not None:
            raise ValidationError("Username is taken")