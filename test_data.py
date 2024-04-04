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

p1 = Post(title='A',body='A is the first letter of the Latin alphabet')
p2 = Post(title='B',body='B is the second letter of the Latin alphabet')
p3 = Post(title='C',body='C is the second letter of the Latin alphabet')
u1.follow(p3)
u2.follow(p3)
db.session.add(p1)
db.session.add(p2)
db.session.add(p3)

db.session.commit()
