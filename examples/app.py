# -*- coding: utf-8 -*-
from flask import Flask, render_template, request, flash, Markup, jsonify

from flask_wtf import FlaskForm, CSRFProtect
from wtforms import StringField, SubmitField, BooleanField, PasswordField, IntegerField, TextField,\
    FormField, SelectField, FieldList
from wtforms.validators import DataRequired, Length
from wtforms.fields import *

from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.secret_key = 'dev'

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'

# set default button sytle and size, will be overwritten by macro parameters
app.config['BOOTSTRAP_BTN_STYLE'] = 'primary'
app.config['BOOTSTRAP_BTN_SIZE'] = 'sm'

bootstrap = Bootstrap(app)
db = SQLAlchemy(app)
csrf = CSRFProtect(app)


class ExampleForm(FlaskForm):
    """An example form that contains all the supported bootstrap style form fields."""
    date = DateField(description="We'll never share your email with anyone else.")  # add help text with `description`
    datetime = DateTimeField(render_kw={'placeholder': 'this is placeholder'})  # add HTML attribute with `render_kw`
    image = FileField(render_kw={'class': 'my-class'})  # add your class
    option = RadioField(choices=[('dog', 'Dog'), ('cat', 'Cat'), ('bird', 'Bird'), ('alien', 'Alien')])
    select = SelectField(choices=[('dog', 'Dog'), ('cat', 'Cat'), ('bird', 'Bird'), ('alien', 'Alien')])
    selectmulti = SelectMultipleField(choices=[('dog', 'Dog'), ('cat', 'Cat'), ('bird', 'Bird'), ('alien', 'Alien')])
    bio = TextAreaField()
    title = StringField()
    secret = PasswordField()
    remember = BooleanField('Remember me')
    submit = SubmitField()


class HelloForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(1, 20)])
    password = PasswordField('Password', validators=[DataRequired(), Length(8, 150)])
    remember = BooleanField('Remember me')
    submit = SubmitField()


class ButtonForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(1, 20)])
    submit = SubmitField()
    delete = SubmitField()
    cancel = SubmitField()


class TelephoneForm(FlaskForm):
    country_code = IntegerField('Country Code')
    area_code = IntegerField('Area Code/Exchange')
    number = TextField('Number')


class IMForm(FlaskForm):
    protocol = SelectField(choices=[('aim', 'AIM'), ('msn', 'MSN')])
    username = TextField()


class ContactForm(FlaskForm):
    first_name = TextField()
    last_name = TextField()
    mobile_phone = FormField(TelephoneForm)
    office_phone = FormField(TelephoneForm)
    emails = FieldList(TextField("Email"), min_entries=3)
    im_accounts = FieldList(FormField(IMForm), min_entries=2)


class Message(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.Text)
    author = db.Column(db.String(100))
    category = db.Column(db.String(100))
    sender = db.Column(db.String(100))
    create_time = db.Column(db.String(100))


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/form', methods=['GET', 'POST'])
def test_form():
    form = HelloForm()
    return render_template('form.html', form=form, telephone_form=TelephoneForm(), contact_form=ContactForm(), im_form=IMForm(), button_form=ButtonForm(), example_form=ExampleForm())


@app.route('/nav', methods=['GET', 'POST'])
def test_nav():
    return render_template('nav.html')


@app.route('/pagination', methods=['GET', 'POST'])
def test_pagination():
    db.drop_all()
    db.create_all()
    for i in range(100):
        m = Message()
        db.session.add(m)
    db.session.commit()
    page = request.args.get('page', 1, type=int)
    pagination = Message.query.paginate(page, per_page=10)
    messages = pagination.items
    return render_template('pagination.html', pagination=pagination, messages=messages)


@app.route('/static', methods=['GET', 'POST'])
def test_static():
    return render_template('static.html')


@app.route('/flash', methods=['GET', 'POST'])
def test_flash():
    flash('A simple primary alert—check it out!', 'primary')
    flash('A simple secondary alert—check it out!', 'secondary')
    flash('A simple success alert—check it out!', 'success')
    flash('A simple danger alert—check it out!', 'danger')
    flash('A simple warning alert—check it out!', 'warning')
    flash('A simple info alert—check it out!', 'info')
    flash('A simple light alert—check it out!', 'light')
    flash('A simple dark alert—check it out!', 'dark')
    flash(Markup('A simple success alert with <a href="#" class="alert-link">an example link</a>. Give it a click if you like.'), 'success')
    return render_template('flash.html')


@app.route('/table')
def test_table():
    db.drop_all()
    db.create_all()
    for i in range(20):
        m = Message(
            text='Test message {}'.format(i+1),
            author='Author {}'.format(i+1),
            category='Category {}'.format(i+1),
            sender='Sender {}'.format(i+1),
            create_time='Today'
            )
        db.session.add(m)
    db.session.commit()
    page = request.args.get('page', 1, type=int)
    pagination = Message.query.paginate(page, per_page=10)
    messages = pagination.items
    titles = [('id', '#'), ('text', 'Message'), ('author', 'Author'), ('category', 'Category'), ('sender', 'Sender'), ('create_time', 'Create Time')]
    return render_template('table.html', messages=messages, titles=titles)


@app.route('/table/<message_id>/view')
def view_message(message_id):
    return f'Viewing {message_id}'


@app.route('/table/<message_id>/edit')
def edit_message(message_id):
    return f'Editing {message_id}'


@app.route('/table/<message_id>/delete', methods=['POST'])
def delete_message(message_id):
    return f'Deleting {message_id}'


if __name__ == '__main__':
    app.run(debug=True)
