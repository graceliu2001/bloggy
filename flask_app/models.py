from . import db, login_manager
from flask_login import UserMixin

@login_manager.user_loader
def load_user(user_id):
    return User.objects(username=user_id).first()

class User(db.Document, UserMixin):
    username = db.StringField(required=True, unique=True, min_length = 1, max_length = 40)
    email = db.EmailField(required=True, unique=True)
    password = db.StringField(required=True)

    # Returns unique string identifying our object
    def get_id(self):
        return self.username

class Comment(db.Document):
    commenter = db.ReferenceField(User)
    content = db.StringField(min_length=5, max_length=500, required=True)
    date = db.StringField(required=True)
    post_title = db.StringField(min_length=1, max_length=100, required=True)

class Post(db.Document):
    poster = db.ReferenceField(User)
    content = db.StringField(min_length=5, max_length=5000, required=True)
    date = db.StringField(required=True)
    post_title = db.StringField(min_length=1, max_length=40, required=True)