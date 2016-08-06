from app import db

class Participant(db.Model):
    __tablename__ = 'participants'

    id = db.Column(db.Integer, primary_key=True)
    p_num = db.Column(db.String)
    role = db.Column(db.String)

class Survey(db.Model):
    __tablename__ = 'surveys'

    id = db.Column(db.Integer, primary_key=True)
    survey_name = db.Column(db.String)
    participant_id = db.Column(db.Integer, db.ForeignKey('participants.id'))

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

