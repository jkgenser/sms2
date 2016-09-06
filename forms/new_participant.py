from flask_wtf import Form
from wtforms import StringField, SelectField
from wtforms.validators import DataRequired, Length

def _locations():
    locations = ['CCA', 'CG East', 'CG West', 'CCC Springfield', 'CCC Framingham', 'CCC Boston']
    return locations

class NewParticipantForm(Form):
    name = StringField('Name', validators=[DataRequired()])
    phone_number = StringField('Phone number', validators=[
                               DataRequired(), Length(min=10, max=10)])
    role = StringField('Functional role', validators=[DataRequired()])
    location = StringField('Location', validators=[DataRequired()])