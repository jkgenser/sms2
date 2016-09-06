from flask_wtf import Form
from wtforms import StringField, SelectField, IntegerField
from wtforms.validators import DataRequired, Length


class NewSurveyForm(Form):
    name = StringField('Name of survey', validators=[DataRequired()])
    duration = IntegerField('Duration of survey in days', validators=[DataRequired()])
    frequency = IntegerField('Frequency (number of pings per day)', validators=[DataRequired()])
    instrument = StringField('Instrument for the survey', validators=[DataRequired()])