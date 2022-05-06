from flask import Blueprint
from flask import Flask, render_template, redirect, url_for, flash, request
from flask_login import (
    current_user,
    login_user,
    login_required,
    logout_user
)
# from flask_bcrypt import Bcrypt

from .. import bcrypt
from ..forms import (
    RegistrationForm,
    LoginForm,
    UpdateUsernameForm,
)
from ..models import User, Comment, Post, load_user
from ..utils import current_time

users = Blueprint("users", __name__)

@users.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('users.account'))

    form = LoginForm()
    if form.validate_on_submit():
        user = User.objects(username=form.username.data).first()

        if (user is not None and bcrypt.check_password_hash(user.password, form.password.data)):
            login_user(user)
            return redirect(url_for('users.account'))
        else:
            flash('Login failed. Check your username or password')

    return render_template('login.html', title="Login", form=form)


@users.route("/register", methods=["GET", "POST"])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('users.account'))

    form = RegistrationForm()

    if form.validate_on_submit():
        hashed = bcrypt.generate_password_hash(form.password.data).decode('utf-8')    
        user = User(username=form.username.data, email=form.email.data, password=hashed)
        
        user.save()
        return redirect(url_for('users.login'))

    return render_template('register.html', title='Register', form=form)


@users.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for('users.login'))


@users.route("/account", methods=["GET", "POST"])
@login_required
def account():
    form_username = UpdateUsernameForm()

    if form_username.validate_on_submit():
        current_user.username = form_username.username.data
        current_user.save()
        return redirect(url_for('users.account'))

    return render_template("account.html", form_username=form_username)