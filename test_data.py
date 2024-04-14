import os
from app import db, app
from app.models import User, Post
# from app.search import create_index

app_context = app.app_context()
app_context.push()
db.drop_all()
db.create_all()

u1 = User(username='john', email='john@example.com')
u2 = User(username='jusan', email='susan@example.com')
u1.set_password("j")
u2.set_password("s")
db.session.add(u1)
db.session.add(u2)

p1 = Post(title='A',body='A is the first letter of the Latin alphabet')
p2 = Post(title='B',body='B is the second letter of the Latin alphabet')
p3 = Post(title='C',body='C is the third letter of the Latin alphabet')
p4 = Post(title='AA',body='AA is ......是但la')
p5 = Post(title='AAA',body='AAA is ......是但la')
p6 = Post(title='AAAA',body='AAAA is ......是但la')
p7 = Post(title='AAAAA',body='AAAAA is ......是但la')
p8 = Post(title='AAAAAA',body='AAAAAA is ......是但la')

u1.follow(p3)
u2.follow(p3)
db.session.add_all([p1, p2, p3, p4, p5, p6, p7, p8])
db.session.commit()
# create_index()