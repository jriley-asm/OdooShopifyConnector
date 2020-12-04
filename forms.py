from flask_wtf import FlaskForm
from wtforms import TextField, PasswordField, StringField, IntegerField, FileField, BooleanField, SubmitField, SelectField, HiddenField, TextAreaField, RadioField, SelectMultipleField, FloatField
from wtforms.fields.html5 import DateField
from wtforms.validators import DataRequired, EqualTo, Length, InputRequired
from wtforms.fields.html5 import EmailField, DecimalRangeField, DateTimeLocalField
from wtforms import validators

class OdooProductForm(FlaskForm):
    shopify_domain = StringField('Shopify Store Domain', validators=[DataRequired()])
    shopify_password = StringField('Shopify Store Password', validators[])
    product_id = StringField('Pull and Push Product', validators=[DataRequired()])