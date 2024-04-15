from flask_wtf import FlaskForm,RecaptchaField
from wtforms import StringField, PasswordField, BooleanField, SubmitField, \
    TextAreaField, SelectField, RadioField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo, \
    Length, InputRequired
from flask_babel import _, lazy_gettext as _l
from app.models import User
from app.config import Config

class LoginForm(FlaskForm):
    username = StringField(_l('Username'), validators=[DataRequired()])
    password = PasswordField(_l('Password'), validators=[DataRequired()])
    remember_me = BooleanField(_l('Keep me logged in (for up to one year)'))
    submit = SubmitField(_l('Log in'))


class RegistrationForm(FlaskForm):
    username = StringField(_l('Username'), validators=[DataRequired()])
    password = PasswordField(_l('Password'), validators=[DataRequired()])
    password2 = PasswordField(
        _l('Confirm password'), validators=[DataRequired(),
                                           EqualTo('password')])
    email = StringField(_l('Email address (recommended)'), validators=[DataRequired(), Email()])
    # 要有domain name先用到
    # recaptcha=RecaptchaField(_l('CAPTCHA Security check'))
    submit = SubmitField(_l('Create your account'))

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError(_('Please use a different username.'))

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError(_('Please use a different email address.'))


class ResetPasswordRequestForm(FlaskForm):
    email = StringField(_l('Email'), validators=[DataRequired(), Email()])
    submit = SubmitField(_l('Request Password Reset'))


class ResetPasswordForm(FlaskForm):
    password = PasswordField(_l('Password'), validators=[DataRequired()])
    password2 = PasswordField(
        _l('Repeat Password'), validators=[DataRequired(),
                                           EqualTo('password')])
    submit = SubmitField(_l('Request Password Reset'))


class EditForm(FlaskForm):
    edit_post = TextAreaField(_l(''),validators=[Length(min=0, max=2000)])
    submit = SubmitField(_l('Publish change'))
    cancel = SubmitField(_l('Cancel'))


class PostForm(FlaskForm):
    post = TextAreaField(_l('Say something'), validators=[DataRequired()])
    submit = SubmitField(_l('Submit'))


class DonationForm(FlaskForm):
    once_or_monthly = RadioField('', choices=[('once', 'Just Once'), ('monthly', 'Give Monthly')], validators=[InputRequired()])
    amount = RadioField('', choices=[('20', '$20'), ('50', '$50'), ('100', '$100'), ('200', '$200')], validators=[InputRequired()])
    transaction_fee = BooleanField(_l("I'll generously add 4% to cover the transaction fees so you can keep 100% of my donation."))
    card = SubmitField(_l('Donate by credit/debit card'))
    paypal = SubmitField(_l('Paypal'))
    gpay = SubmitField(_l('GPay'))

class PaymentForm(FlaskForm):
    fisrtname = StringField(_l('Fisrt name'), validators=[DataRequired()])
    lastname = StringField(_l('Last name'), validators=[DataRequired()])
    email = StringField(_l('Email address'), validators=[DataRequired(), Email()])
    submit = SubmitField(label=_l('Submit'))