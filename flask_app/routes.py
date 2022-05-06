# from flask import Flask, render_template, redirect, url_for, flash, request
# from flask_login import (
#     current_user,
#     login_user,
#     login_required,
#     logout_user
# )
# # from flask_bcrypt import Bcrypt

# # from . import app, bcrypt
# from .forms import (
#     RegistrationForm,
#     LoginForm,
#     UpdateUsernameForm,
#     PostForm,
#     PostCommentForm,
#     SearchForm
# )
# from .models import User, Comment, Post, load_user
# from .utils import current_time


# @app.route("/", methods=["GET", "POST"])
# @login_required
# def index():
#     form = SearchForm()

#     if form.validate_on_submit():
#         return redirect(url_for("search", username=form.search_query.data))

#     return render_template("index.html", form=form)


# @app.route("/search/<username>", methods=["GET"])
# @login_required
# def search(username):
#     user = User.objects(username=username).first()
#     error = None

#     first_letter = username[0]
#     results = []

#     for i in User.objects:
#         if i.username[0] == first_letter:
#             results.append(i)

#     if len(results) == 0:
#         error = "User does not exist"
#         return render_template('404.html', error=error)

#     elif user is not None:
#         comments = Comment.objects(commenter=user)
#         posts = Post.objects(poster=user)
#         return render_template('user_detail.html', username=user.username, comments=comments, posts=posts)

#     return render_template('search.html', results=results)


# @app.route("/posts/<post_title>", methods=["GET", "POST"])
# @login_required
# def post_detail(post_title):
#     post = Post.objects(post_title=post_title).first()

#     username = post.poster.username
#     print(username)

#     form = PostCommentForm()
#     if form.validate_on_submit():
#         comment = Comment(
#             commenter=current_user._get_current_object(),
#             content=form.text.data,
#             date=current_time(),
#             post_title=post_title,
#         )
#         comment.save()

#         return redirect(request.path)

#     comments = Comment.objects(post_title=post_title)
#     comments_final = []
#     for comment in comments:
#         comments_final.append({
#             'commenter': comment.commenter,
#             'content': comment.content,
#             'date': comment.date,
#             'post_title': comment.post_title
#         })

#     return render_template(
#         "post_detail.html", username=username, form=form, post=post, comments=comments_final
#     )


# @app.route("/<username>/posts", methods=["GET", "POST"])
# @login_required
# def create_post(username):
#     user = User.objects(username=username).first()

#     form = PostForm()
#     if form.validate_on_submit():
#         post = Post(
#             poster=user,
#             content=form.text.data,
#             date=current_time(), 
#             post_title =form.title.data
#         )
#         post.save()

#         return redirect(request.path)

#     return render_template(
#         "create_post.html", form=form
#     )


# @app.route("/user/<username>")
# @login_required
# def user_detail(username):
#     user = User.objects(username=username).first()
#     error = None

#     if user is None:
#         error = "User does not exist"
#         return render_template('404.html', error=error)
#     else: 
#         comments = Comment.objects(commenter=user)
#         posts = Post.objects(poster=user)
#         return render_template('user_detail.html', username=user.username, comments=comments, posts=posts, error=error)


# @app.errorhandler(404)
# def custom_404(e):
#     return render_template('404.html', error=e)

# """ ************ User Management views ************ """

# @app.route("/login", methods=["GET", "POST"])
# def login():
#     if current_user.is_authenticated:
#         return redirect(url_for('account'))

#     form = LoginForm()
#     if form.validate_on_submit():
#         user = User.objects(username=form.username.data).first()

#         if (user is not None and bcrypt.check_password_hash(user.password, form.password.data)):
#             login_user(user)
#             return redirect(url_for('account'))
#         else:
#             flash('Login failed. Check your username or password')

#     return render_template('login.html', title="Login", form=form)


# @app.route("/register", methods=["GET", "POST"])
# def register():
#     if current_user.is_authenticated:
#         return redirect(url_for('account'))

#     form = RegistrationForm()

#     if form.validate_on_submit():
#         hashed = bcrypt.generate_password_hash(form.password.data).decode('utf-8')    
#         user = User(username=form.username.data, email=form.email.data, password=hashed)
        
#         user.save()
#         return redirect(url_for('login'))

#     return render_template('register.html', title='Register', form=form)


# @app.route("/logout")
# @login_required
# def logout():
#     logout_user()
#     return redirect(url_for('login'))


# @app.route("/account", methods=["GET", "POST"])
# @login_required
# def account():
#     form_username = UpdateUsernameForm()

#     if form_username.validate_on_submit():
#         current_user.username = form_username.username.data
#         current_user.save()
#         return redirect(url_for('account'))

#     return render_template("account.html", form_username=form_username)