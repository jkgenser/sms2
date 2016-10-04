from flask import Flask, render_template, request, url_for, flash, redirect
from flask.ext.sqlalchemy import SQLAlchemy
from twilio.rest import TwilioRestClient as Client
from celery import Celery
import config
import twilio.twiml
import os
import datetime
import json


app = Flask(__name__)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config.from_object(os.environ['APP_SETTINGS'])
db = SQLAlchemy(app)

twilio_account_sid = app.config['TWILIO_ACCOUNT_SID']
twilio_auth_token = app.config['TWILIO_AUTH_TOKEN']
twilio_number = app.config['TWILIO_NUMBER']

client = Client(twilio_account_sid, twilio_auth_token)

from models import Survey, Participant, Ping


# endpoint for twilio POST reqests
# TODO move this to a separate views module..
@app.route('/message', methods=['GET', 'POST'])
def survey_controller():


    # Who the message came from
    from_number = request.values['From']

    # Body of the message
    body = request.values['Body']

    # Look up participant that the number belongs to:
    participant = db.session.query(Participant).filter(Participant.phone_number == from_number).all()[0]

    # Look up survey categories for that survey
    survey_json = db.session.query(Survey).get(s_id).body
    categories = survey_json['question'].keys()

    if body.upper() in categories:
        return redirect(url_for('subcategory_controller',
                                body=body,
                                p_id = participant.id,
                                s_id = participant.survey_id))

    # Also add logic to make sure that they have gone through the top level question ...
    # Arbitrarily entering a 1 will not result in storing that value
    try:
        if type(int(body)) == int:
            sub_categories = []
            for key in survey_json['question'].keys():
                for branch in survey_json['question'][key]['options'].keys():
                    sub_categories.append(branch)
            print sub_categories

    except ValueError:
        print 'Please give me a better answer!'



@app.route('/sub_category', methods=['GET', 'POST'])
def subcategory_controller():
    body = request.args['body']
    p_id = request.args['p_id']
    s_id = request.args['s_id']

    survey_json = db.session.query(Survey).get(s_id).body
    sub_categories = survey_json['question'][body]['options'].keys()

    if body.upper() in survey_json['question'].keys():
        send_list = ["Thanks! What is the more granular type of work?: "]
        for sub in sub_categories:
            stub = ''.join([sub, '(', survey_json['question'][body]['options'][sub], ') ', ])
            send_list.append(stub)


    client.messages.create(
        to=request.values['From'],
        from_=twilio_number,
        body=''.join(send_list),)

    print 'cool'
    print request.values['Body']


if __name__ == '__main__':
    app.run()

