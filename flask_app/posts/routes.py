from plotly import utils
import plotly.graph_objects as go
import json

from flask import Blueprint
from flask import Flask, render_template, redirect, url_for, flash, request
from flask_login import (
    current_user,
    login_user,
    login_required,
    logout_user
)

from ..forms import (
    PostForm,
    PostCommentForm,
    SearchForm
)
from ..models import User, Comment, Post, load_user
from ..utils import current_time

posts = Blueprint("posts", __name__)

@posts.route("/plot/<username>")
def plotly(username):
    user = User.objects(username=username).first()
    post = Post.objects(poster=user)
    comment = Comment.objects(commenter=user)

    num_post = len(post)
    num_comment = len(comment)

    labels = ["Number of Posts", "Number of comments"]
    values = [num_post, num_comment]

    fig = go.Figure(data=[go.Pie(labels=labels, values=values)])
    graphJSON = json.dumps(fig, cls=utils.PlotlyJSONEncoder)

    return render_template("plot.html", graphJSON=graphJSON, values=values, username=username)

    
@posts.route("/about")
def about():
    return render_template("about.html")

@posts.route("/", methods=["GET", "POST"])
@login_required
def index():
    form = SearchForm()

    if form.validate_on_submit():
        return redirect(url_for("posts.search", username=form.search_query.data))

    return render_template("index.html", form=form)


@posts.route("/search/<username>", methods=["GET"])
@login_required
def search(username):
    user = User.objects(username=username).first()
    error = None

    first_letter = username[0]
    results = []

    for i in User.objects:
        if i.username[0] == first_letter:
            results.append(i)

    if len(results) == 0:
        error = "User does not exist"
        return render_template('404.html', error=error)

    elif user is not None:
        comments = Comment.objects(commenter=user)
        posts = Post.objects(poster=user)
        return render_template('user_detail.html', username=user.username, comments=comments, posts=posts)

    return render_template('search.html', results=results)


@posts.route("/posts/<post_title>", methods=["GET", "POST"])
@login_required
def post_detail(post_title):
    post = Post.objects(post_title=post_title).first()

    username = post.poster.username

    form = PostCommentForm()
    if form.validate_on_submit():
        comment = Comment(
            commenter=current_user._get_current_object(),
            content=form.text.data,
            date=current_time(),
            post_title=post_title,
        )
        comment.save()

        return redirect(request.path)

    comments = Comment.objects(post_title=post_title)
    comments_final = []
    for comment in comments:
        comments_final.append({
            'commenter': comment.commenter,
            'content': comment.content,
            'date': comment.date,
            'post_title': comment.post_title
        })

    return render_template(
        "post_detail.html", username=username, form=form, post=post, comments=comments_final
    )


@posts.route("/<username>/posts", methods=["GET", "POST"])
@login_required
def create_post(username):
    user = User.objects(username=username).first()

    form = PostForm()
    if form.validate_on_submit():
        post = Post(
            poster=user,
            content=form.text.data,
            date=current_time(), 
            post_title =form.title.data
        )
        post.save()

        return redirect(request.path)

    return render_template(
        "create_post.html", form=form
    )


@posts.route("/user/<username>")
@login_required
def user_detail(username):
    user = User.objects(username=username).first()
    error = None

    if user is None:
        error = "User does not exist"
        return render_template('404.html', error=error)
    else: 
        comments = Comment.objects(commenter=user)
        posts = Post.objects(poster=user)
        return render_template('user_detail.html', username=user.username, comments=comments, posts=posts, error=error)


@posts.errorhandler(404)
def custom_404(e):
    return render_template('404.html', error=e)