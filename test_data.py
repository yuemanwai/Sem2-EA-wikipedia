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

p1 = Post(title='post1',body='body1')
p2 = Post(title='post2',body='body2')
p3 = Post(title='post3',body='<cite>Smith, John. "Example Cite web citation." Example.com. Retrieved March 31, 2024. <a href="https://www.example.com">https://www.example.com</a></cite>')
# u1.follow(p1)
# u2.follow(p2)
db.session.add(p1)
db.session.add(p2)
db.session.add(p3)

db.session.commit()
