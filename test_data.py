from app import db, app
from app.models import User, Post

app_context = app.app_context()
app_context.push()
db.drop_all()
db.create_all()

u1 = User(username='wai', email='wai@example.com')
u2 = User(username='marco', email='marco@example.com')
u3 = User(username='markus', email='markus@example.com')
u4 = User(username='sam', email='sam@example.com')
u1.set_password("w")
u2.set_password("m")
u3.set_password("m")
u4.set_password("s")
db.session.add_all([u1, u2, u3, u4])

p1 = Post(title='A',body='<b>A</b> is the first letter of the Latin alphabet')
p2 = Post(title='B',body='<b>B</b> is the second letter of the Latin alphabet')
p3 = Post(title='C',body='<b>C</b> is the third letter of the Latin alphabet')
p4 = Post(title='AA',body='AA is ......是但la')
p5 = Post(title='AAA',body='AAA is ......是但la')

u1.follow(p1)
u2.follow(p2)
db.session.add_all([p1, p2, p3, p4, p5])
db.session.commit()