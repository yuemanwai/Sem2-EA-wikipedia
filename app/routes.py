from datetime import datetime, timedelta
from flask import render_template, flash, redirect, url_for, request, g, make_response, session
from flask_login import login_user, logout_user, current_user, login_required
from werkzeug.urls import url_parse
from flask_babel import _, get_locale
from app import app, db
from app.forms import LoginForm, RegistrationForm, EditForm, PostForm, \
    ResetPasswordRequestForm, ResetPasswordForm, DonationForm, PaymentForm, CeventForm
from app.models import User, Post, Image, Donor, Payment, IP, Current_event
from app.email import send_password_reset_email
from random import randint
from werkzeug.utils import secure_filename
import os


@app.before_request
def before_request():
    if current_user.is_authenticated:
        current_user.last_seen = datetime.utcnow()
        db.session.commit()
    g.locale = str(get_locale())


@app.route('/', methods=['GET'])
@app.route('/wiki/Main_Page', methods=['GET'])
def index():
    return render_template('index.html.j2', category=_('Main Page'))


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash(_('Invalid username or password'))
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data,
                   duration=timedelta(days=365))
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('index')
        return redirect(next_page)
    return render_template('login.html.j2', title=_('Log in'), form=form)


@app.route('/logout')
def logout():
    logout_user()
    return render_template('logout.html.j2', title=_('Log out'))


@app.route('/CreateAccount', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash(_('Congratulations, you are now a registered user!'))
        return redirect(url_for('index'))
    return render_template('register.html.j2', title=_('Create account'), form=form)


@app.route('/reset_password_request', methods=['GET', 'POST'])
def reset_password_request():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = ResetPasswordRequestForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user:
            send_password_reset_email(user)
        flash(
            _('Check your email for the instructions to reset your password'))
        return redirect(url_for('login'))
    return render_template('reset_password_request.html.j2',
                           title=_('Reset Password'), form=form)


@app.route('/reset_password/<token>', methods=['GET', 'POST'])
def reset_password(token):
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    user = User.verify_reset_password_token(token)
    if user is None:
        return redirect(url_for('index'))
    form = ResetPasswordForm()
    if form.validate_on_submit():
        user.set_password(form.password.data)
        db.session.commit()
        flash(_('Your password has been reset.'))
        return redirect(url_for('login'))
    return render_template('reset_password.html.j2', form=form)


@app.route('/homepage', methods=['GET', 'POST'])
@login_required
def user():
    user = User.query.filter_by(username=current_user.username).first_or_404()
    form = PostForm()
    if form.validate_on_submit():
        post = Post.query.filter_by(
            title=current_user.username).first() or None
        if not post:
            post = Post(title=current_user.username, body=form.body.data)
            db.session.add(post)
            ip = IP.query.filter_by(post_id=post.id).first() or None
            if not ip:
                ip = IP(post_id=post.id, ip_addr=request.remote_addr)
                db.session.add(ip)
                flash('We will store your IP address')
        else:
            if form.title.data != current_user.username:
                flash('Cannot change user page title.')
                return redirect(url_for('user', username=current_user.username))
            post.body = form.body.data
            image = Image.query.filter_by(post_id=post.id).first() or None
            if image:
                image.post_id = post.id
                image.filename = post.title
            f = form.image.data
            filename = secure_filename(post.title)
            f.save(os.path.join(
                "app", 'static', 'image', filename)+'.jpg')
            image = Image(post_id=post.id, filename=post.title)
            db.session.add(image)
        db.session.commit()
        flash(_('Your user page has been saved.'))
        return redirect(url_for('user', username=current_user.username))
    elif request.method == 'GET':
        post = Post.query.filter_by(
            title=current_user.username).first() or None
        if post:
            form.title.data = post.title
            form.body.data = post.body
    image_path = os.path.join('static', 'image', user.username)+'.jpg'
    return render_template('homepage.html.j2',  title=_(f'Hello, {current_user.username.capitalize()}!'), form=form, user=user, image_path=image_path)


@app.route('/edit', methods=['GET', 'POST'])
def edit():  # 唔可以係呢個位用title, 會出現TypeError
    title = request.args.get('title')
    if title is None:
        print("No title provided")
    post = Post.query.filter_by(title=title).first()
    form = EditForm(edit_post=post.body)
    if form.validate_on_submit():
        if form.submit.data:
            post.body = form.edit_post.data
            db.session.commit()
            flash(_('Changes have been saved.'))
        elif form.cancel.data:
            flash(_('Changes have been canceled.'))
        return redirect(url_for('wiki', title=title))
    elif request.method == 'GET':
        form.edit_post.data = post.body
    return render_template('edit.html.j2', title=_(f'Editing {post.title}'), form=form)


@app.route('/follow/<title>', methods=['POST'])
@login_required
def follow(title):
    post = Post.query.filter_by(title=title).first()
    current_user.follow(post)
    db.session.commit()
    following_article = True
    flash(_('<%(title)s> and its talk page have been added to your watchlist permanently.', title=title))
    return redirect(url_for('wiki', title=title, following_article=following_article))


@app.route('/unfollow/<title>', methods=['POST'])
@login_required
def unfollow(title):
    post = Post.query.filter_by(title=title).first()
    current_user.unfollow(post)
    db.session.commit()
    following_article = False
    flash(_('<%(title)s> and its talk page have been removed from your watchlist.', title=title))
    return redirect(url_for('wiki', title=title, following_article=following_article))


@app.route('/Watchlist/<username>')
@login_required
def watchlist(username):
    user = User.query.filter_by(username=username).first_or_404()
    posts = user.followed_posts().all()
    count = user.followed_posts().count()
    return render_template('watchlist.html.j2', title=_('Watchlist'), posts=posts, count=count)


@app.route('/random_article')
def get_random_article():
    count = Post.query.count()
    if count:
        random_id = randint(1, count)
        random_post = Post.query.get(random_id)
        if random_post:
            title = random_post.title
            return redirect(url_for('wiki', title=title))
    flash('Article not found')
    return redirect(url_for('index'))


@app.route('/wiki/<title>')
def wiki(title):
    post = Post.query.filter_by(title=title).first()
    if post:
        if current_user.is_authenticated:
            following_post = current_user.is_following(post)
            return render_template('random_article.html.j2', category=_('Article'), title=title, posts=[post], following_post=following_post)
        return render_template('random_article.html.j2', category=_('Article'), title=title, posts=[post], following_post=False)
    return render_template('random_article.html.j2', category=_('Article'), title=title, posts=[], following_post=False)


@app.route('/search')
def search():
    keyword = request.args.get('keyword', '')
    if keyword is None:
        return redirect(url_for('index'))
    page_num = request.args.get('page', 1, type=int)
    posts = Post.query.filter(Post.title.like(f'%{keyword}%')).paginate(
        page=page_num, per_page=app.config["POSTS_PER_PAGE"], error_out=False)
    next_url = url_for('search', keyword=keyword,
                       page=page_num + 1) if posts.has_next else None
    prev_url = url_for('search', keyword=keyword,
                       page=page_num - 1) if posts.has_prev else None
    return render_template('search.html.j2', title=_('Search results'), posts=posts.items, keyword=keyword, next_url=next_url, prev_url=prev_url)


@app.route('/donate', methods=['GET', 'POST'])
def donate():
    form = DonationForm()
    count_total = None
    if form.validate_on_submit():
        option = form.once_or_monthly.data
        amount = form.amount.data
        fee = form.transaction_fee.data
        count_total = int(amount)
        if fee:
            count_total *= 1.04  # Amount+交易手續費
        if form.card.data:
            pay_method = 'card'
        elif form.paypal.data:
            pay_method = 'paypal'
        else:
            pay_method = 'GPay'
        return redirect(url_for('payment', pay_method=pay_method, amount=count_total, donate_form=form))
    return render_template('donate.html.j2', form=form)


@app.route('/payment/<pay_method>/<amount>/<donate_form>', methods=['GET', 'POST'])
def payment(pay_method, amount, donate_form):
    payment_form = PaymentForm(submit=pay_method)
    if payment_form.validate_on_submit():
        print (donate_form.once_or_monthly.data)
        if donate_form.once_or_monthly.data == "monthly":
            monthly = True
        else:
            monthly = False

        donor = Donor(firstname=payment_form.firstname.data, lastname=payment_form.lastname.data, \
                      email=payment_form.email.data, monthly=monthly)
        payment=Payment(donor_id=donate_form.donor_id.data, pay_method=donate_form.pay_method.data, \
                      pay_acc=donate_form.pay_acc.data, amount_hkd=donate_form.amount.data,donate_on=datetime.utcnow())
        db.session.add(donor)
        db.session.add(payment)
        db.session.commit()
        flash('Thank you for donation!')
        return redirect(url_for('payment'))
    elif request.method == 'GET':
        payment_form.submit.label.text = f'Donate with {pay_method}'
    return render_template('donate_payment.html.j2', form=payment_form, amount=amount)

@app.route('/c_event', methods=['GET', 'POST'])
def c_event():
    Cform=CeventForm()
    if Cform.validate_on_submit():
        name =Cform.name.data
        message =Cform.message.data
        current_event = Current_event(name=name, message=message)
        db.session.add(current_event)
        db.session.commit()
        flash('WikiLove Sent Successfully!')
        return render_template('c_event.html.j2', form=Cform)
    return redirect(url_for('index'))