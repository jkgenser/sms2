from flask_wtf import Form
from wtforms import StringField, SelectField, IntegerField, TextAreaField
from wtforms.fields.html5 import DateField
from wtforms.validators import DataRequired, Length


class NewSurveyForm(Form):
    name = StringField('Name of survey', validators=[DataRequired()])
    duration = IntegerField('Duration of survey in days', validators=[DataRequired()])
    frequency = IntegerField('Frequency (number of pings per day)', validators=[DataRequired()])
    start_date = DateField('Start date of the survey', validators=[DataRequired()])
    body = TextAreaField('JSON field of the survey contents', validators=[DataRequired()])