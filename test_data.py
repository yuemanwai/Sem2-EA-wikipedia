from app import db, app
from app.models import User, Post


app_context = app.app_context()
app_context.push()
db.drop_all()
db.create_all()

u1 = User(username='John', email='john@example.com')
u2 = User(username='Susan', email='susan@example.com')
u1.set_password("j")
u2.set_password("s")
db.session.add(u1)
db.session.add(u2)

p1 = Post(title='USA',body='body1')
p2 = Post(title='HK',body='body1')
# u1.follow(p1)
# u2.follow(p2)
db.session.add(p1)
db.session.add(p2)

db.session.commit()
