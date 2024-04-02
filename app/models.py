
from datetime import datetime, timedelta, timezone
from hashlib import md5
from app import app, db, login
import jwt

from flask_login import UserMixin

from werkzeug.security import generate_password_hash, check_password_hash


watchlist = db.Table(
    'watchlist',
    db.Column('follower_id', db.Integer, db.ForeignKey('user.id')),
    db.Column('followed_post_id', db.Integer, db.ForeignKey('post.id'))
)


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    about_me = db.Column(db.String(140))
    last_seen = db.Column(db.DateTime, default=datetime.utcnow)
    followed_post = db.relationship(
        'User', secondary=watchlist,
        primaryjoin=(watchlist.c.follower_id == id),
        backref=db.backref('watchlist', lazy='dynamic'), lazy='dynamic')

    def __repr__(self) -> str:
        return f'<User {self.username}>'

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def avatar(self, size):
        digest = md5(self.email.lower().encode("utf-8")).hexdigest()
        return 'https://www.gravatar.com/avatar/{}?d=identicon&s={}'.format(
            digest, size)

    def follow(self, post):
        if not self.is_following(post):
            self.followed_post.append(post)

    def unfollow(self, post):
        if self.is_following(post):
            self.followed_post.remove(post)

    def is_following(self, post):
        return self.followed_post.filter(watchlist.c.followed_post_id == post.id).count() > 0

    def followed_posts(self):
        followed = Post.query.join(
            watchlist, watchlist.c.followed_post_id == Post.id
        ).filter(watchlist.c.follower_id == self.id)
        # own = Post.query.filter_by(user_id=self.id)
        return followed.order_by(Post.create_time.desc())

    def get_reset_password_token(self, expires_in=600):
        return jwt.encode({"reset_password": self.id,
                           "exp": datetime.now(tz=timezone.utc) + timedelta(seconds=expires_in)},
                          app.config["SECRET_KEY"], algorithm="HS256")

    @staticmethod
    def verify_reset_password_token(token):
        try:
            id = jwt.decode(token, app.config["SECRET_KEY"], algorithms="HS256")[
                "reset_password"]
        except:           
            return None
        return User.query.get(id)


@login.user_loader
def load_user(id):
    return User.query.get(int(id))


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    article_title = db.Column(db.String(140), index=True, unique=True)
    article_content = db.Column(db.String(2000))
    create_time = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    edit_time = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    follower = db.relationship(
    'Post', secondary=watchlist,
    primaryjoin=(watchlist.c.followed_post_id == id),
    backref=db.backref('watchlist', lazy='dynamic'), lazy='dynamic')

    def __repr__(self) -> str:
        return f'<Post {self.article_content}>'