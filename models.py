from app import db
from sqlalchemy import ForeignKey
from sqlalchemy.dialects.postgresql import JSON

class Survey(db.Model):
    __tablename__ = 'survey'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    duration = db.Column(db.Integer)    # number of days the survey will run for
    frequency = db.Column(db.Integer)   # number of pings sent per day
    start_date = db.Column(db.DateTime) # date the survey begins
    body = db.Column(JSON)
    prompt = db.Column(db.String)

    participants = db.relationship('Participant', backref='survey')
    pings = db.relationship('Ping', backref='survey')


class Participant(db.Model):
    __tablename__ = 'participant'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    survey_id = db.Column(db.Integer, ForeignKey('survey.id'))
    name = db.Column(db.String)
    phone_number = db.Column(db.String)
    role = db.Column(db.String)
    location = db.Column(db.String)


class Ping(db.Model):
    __tablename__ = 'ping'

    id = db.Column(db.Integer, primary_key=True)
    survey_id = db.Column(db.Integer, ForeignKey('survey.id'))
    participant_id = db.Column(db.Integer, ForeignKey('participant.id'))
    from_num = db.Column(db.String)
    sent = db.Column(db.Integer)
    received = db.Column(db.Integer)
    received_time = db.Column(db.DateTime)
    sent_time = db.Column(db.DateTime)
    response = db.Column(db.String)
    response_scale = db.Column(db.String)

