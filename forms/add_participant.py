from flask_wtf import Form
from wtforms import StringField, SelectField, IntegerField
from wtforms.validators import DataRequired, Length
from app import db
from models import Participant

def get_unassigned():
    not_assigned = db.session.query(Participant).filter(Participant.survey_id == None)
    people = [(person.id, person.name) for person in not_assigned]
    return people

class AddParticipantForm(Form):
    new_participant = SelectField('New Participant')

    @classmethod
    def new(cls):
        # Instatiate the form
        form = cls()

        # Update the list of participants
        form.new_participant.choices = get_unassigned()
        return form