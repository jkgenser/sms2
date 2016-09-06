from app import db

class Survey(db.Model):
    __tablename__ = 'surveys'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String) # name of the survey
    duration = db.Column(db.Integer)   # number of days the survey will run for
    frequency = db.Column(db.Integer)  # number of pings sent per day
    instrument = db.Column(db.String)  # string of the survey instrument

    participants = db.relationship('Participant', backref='survey')
    pings = db.relationship('Ping', backref='survey')

class Participant(db.Model):
    __tablename__ = 'participants'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String)
    phone_number = db.Column(db.String)
    role = db.Column(db.String)
    location = db.Column(db.String)
    survey_id = db.Column(db.Integer, db.ForeignKey('surveys.id'))


class Ping(db.Model):
    __tablename__ = 'pings'

    id = db.Column(db.Integer, primary_key=True)
    survey_id = db.Column(db.Integer, db.ForeignKey('surveys.id'))
    participant_id = db.Column(db.Integer, db.ForeignKey('participants.id'))
    from_num = db.Column(db.String)
    sent = db.Column(db.Integer)
    received = db.Column(db.Integer)
    received_time = db.Column(db.DateTime)
    sent_time = db.Column(db.DateTime)
    response = db.Column(db.String)

