from datetime import datetime, timedelta, timezone
from hashlib import md5
import uuid
from app import app, db, login
import jwt
from flask import make_response
from flask_login import UserMixin

from werkzeug.security import generate_password_hash, check_password_hash


watchlist = db.Table(
    'watchlist',
    db.Column('user_id', db.Integer, db.ForeignKey('user.id'),nullable=False),
    db.Column('post_id', db.Integer, db.ForeignKey('post.id'),nullable=False)
)


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    last_seen = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self) -> str:
        return f'<Username : {self.username}>'

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
            self.posts.append(post)

    def unfollow(self, post):
        if self.is_following(post):
            self.posts.remove(post)

    def is_following(self, post):
        return self.posts.filter(watchlist.c.post_id == post.id).count() > 0

    def followed_posts(self):
        followed = Post.query.join(
            watchlist, watchlist.c.post_id == Post.id
        ).filter(watchlist.c.user_id == self.id)
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
    
    # @staticmethod
    # def sign_session_id(session_id):
    #     # 使用密鑰對會話 ID 進行簽名，生成 JWT
    #     signed_session_id = jwt.encode({'session_id': session_id}, app.config["SECRET_KEY"], algorithm='HS256')
    #     return signed_session_id

    # @staticmethod
    # def verify_session_id(signed_session_id):
    #     try:
    #         # 驗證 JWT 的簽名並解碼
    #         decoded_token = jwt.decode(signed_session_id, app.config["SECRET_KEY"], algorithms=['HS256'])
    #     except:           
    #         return None
    #     return decoded_token['session_id']  # 返回會話 ID

    # def generate_uuid_for_session_id(self):
    #     namespace = uuid.UUID('00000000-0000-0000-0000-000000000000')  # 自定義命名空間，可以使用您自己的命名空間 UUID
    #     user_id_str = str(self.id)
    #     generated_uuid = uuid.uuid5(namespace, user_id_str)
    #     return generated_uuid
    
@login.user_loader
def load_user(id):
    return User.query.get(int(id))


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(140), index=True, unique=True)
    body = db.Column(db.String(2000))
    create_time = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    edit_time = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    users = db.relationship('User', secondary=watchlist,
                            backref=db.backref('posts', lazy='dynamic'),
                            primaryjoin=(watchlist.c.post_id == id),
                            secondaryjoin=(watchlist.c.user_id == User.id),
                            lazy='dynamic')


    def __repr__(self) -> str:
        return f'<Post title : {self.title}>'
    
# class UserSession(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
#     session_id = db.Column(db.PickleType)

