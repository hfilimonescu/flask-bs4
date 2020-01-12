from datetime import date

from flask import Flask, render_template, flash

from flask_bs4 import Bootstrap
from flask_wtf import FlaskForm

from wtforms import TextField, SelectField, PasswordField, SelectMultipleField
from wtforms import SubmitField, BooleanField, RadioField, FileField
from wtforms import FloatField, DecimalField, IntegerField
from wtforms.fields.html5 import DateField, DateTimeField, EmailField, IntegerRangeField
from wtforms.fields.html5 import DateTimeLocalField
from wtforms.validators import DataRequired, Email, Length


app = Flask(__name__)
app.config['SECRET_KEY'] = 'you-will-never-guess'
app.config['BOOTSTRAP_SERVE_LOCAL'] = True

bootstrap = Bootstrap(app)


class TestForm(FlaskForm):
    name = TextField('Your name', validators=[Length(3, 5)],
                     render_kw={'autofocus': 'autofocus'})
    password = PasswordField(description='Your favorite password', validators=[])
    email = EmailField(u'Your email address')
    remember = BooleanField('Check me out', validators=[],
                            description='Lorem ipsum dolor sit amet, consectetur '
                                        'adipiscing elit. Mauris ultricies libero '
                                        'lacus, eu ornare ex imperdiet quis. Sed non '
                                        'aliquet magna. Praesent gravida odio id massa '
                                        'condimentum, quis imperdiet nunc luctus.')
    ranger = IntegerRangeField('Ranger', render_kw={'step': 1})
    a_float = FloatField(u'A floating point number')
    a_decimal = DecimalField(places=2, rounding='ROUND_HALF_UP',
                             validators=[])
    a_integer = IntegerField(u'An integer')
    sample_file = FileField(u'Your favorite file', description='A file you would like to upload.')
    radio = RadioField('Radio', choices=[('ch_01', 'Choice 01'),
                                         ('ch_02', 'Choice 02'),
                                         ('ch_03', 'Choice 03')],
                       default='ch_02',
                       description='Lorem ipsum dolor sit amet, consectetur '
                                   'adipiscing elit. Mauris ultricies libero '
                                   'lacus, eu ornare ex imperdiet quis. Sed non '
                                   'aliquet magna. Praesent gravida odio id massa '
                                   'condimentum, quis imperdiet nunc luctus.')
    select = SelectField('Person',
                         choices=[('ch_01', 'Choice 01'),
                                  ('ch_02', 'Choice 02'),
                                  ('ch_03', 'Choice 03')],
                         default='ch_03',
                         validators=[DataRequired()])
    select_multi = SelectMultipleField('Persons',
                                       choices=[('ch_01', 'Choice 01'),
                                                ('ch_02', 'Choice 02'),
                                                ('ch_03', 'Choice 03')],
                                       default=['ch_01', 'ch_03'],
                                       validators=[DataRequired()])
    birthday = DateField(u'Your birthday', default=date.today())

    submit = SubmitField(u'Submit Form')


@app.route("/", methods=['GET', 'POST'])
def index():
    form = TestForm()

    if form.validate_on_submit():
        flash('Message')

    return render_template('quick_form.html.j2', form=form)

@app.route("/alternative", methods=['GET', 'POST'])
def alternative():
    form = TestForm()

    if form.validate_on_submit():
        flash('Message')

    return render_template('render_template.html.j2', form=form)