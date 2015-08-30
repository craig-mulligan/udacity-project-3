from flask_wtf import Form
from wtforms import StringField
from wtforms.widgets import TextArea
from wtforms.validators import DataRequired

class addItemForm(Form):
	'''
	This form is used to validate both adding items and updating them
	'''
	name = StringField('name', validators=[DataRequired()])
	description = StringField('description', widget=TextArea(), validators=[DataRequired()])
	category = StringField('category', validators=[DataRequired()])