from flask import Flask, render_template, request, url_for, flash, redirect
from flask.ext.sqlalchemy import SQLAlchemy
import config
import twilio.twiml
import os
import datetime


app = Flask(__name__)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config.from_object(os.environ['APP_SETTINGS'])
db = SQLAlchemy(app)

from models import Participant, Survey, Ping


@app.route('/', methods=['GET', 'POST'])
def show_participants():
    from models import Participant
    participants = db.session.query(Participant).all()
    return render_template('participants.html',
                       participants=participants

# Eventually use WTForms for this
# Eventually move this function to the views module
@app.route('/new', methods=['GET', 'POST'])
def add_participant():
    new_participant = {}
    # get next ID in the increment
    new_participant['id'] = db.session.query(Participant).order_by(Participant.id.desc()).first().id + 1
    new_participant['name'] = request.form['name']
    new_participant['phone_number'] = request.form['phone']
    new_participant['role'] = request.form['role']
    new_participant['location'] = request.form['location']
    db.session.add(Participant(**new_participant))
    db.session.commit()
    flash('Participant succesfully added!')
    return render_template('participants.html',
                       participants=db.session.query(Participant).all())

# with app.test_request_context():
#     print url_for('show_participants')
#     print url_for('add_participant')
#     print(request.form)

# endpoint for twilio POST reqests
# EVENTUALLY move this to a separate views module..
@app.route('/message', methods=['GET', 'POST'])
def store_response():

    try:
        ping = {}

        # Eventually make this do a lookup from participants
        # if the number is not in participants, do not store the ping in DB.
        ping['from_num'] = request.values['From']

        # Eventually check if response is integer, otherwise store as string
        # Or always store as string ... not sure
        ping['response'] = request.values['Body']

        ping['received_time'] = datetime.datetime.now()
        ping['received'] = 1
        ping['sent'] = 0

        db.session.add(Ping(**ping))
        db.session.commit()
        print('ping data was saved succesfully')

    except:
        print('something went wrong')

    print(request.values['From'], request.values['Body'], datetime.datetime.now())
    print(ping)


    return


if __name__ == '__main__':
    app.run()


