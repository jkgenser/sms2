from flask import Flask, render_template, request, url_for, flash, redirect, make_response, session
from flask.ext.sqlalchemy import SQLAlchemy
from twilio.rest import TwilioRestClient as Client
from celery import Celery
import config
from twilio import twiml
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

    from_number = request.values['From']
    body = request.values['Body']
    participant = db.session.query(Participant).filter(Participant.phone_number == from_number).all()[0]
    survey_json = db.session.query(Survey).get(participant.survey_id).body
    categories = survey_json['question'].keys()

    # If you gave me A, B, C then redirect to next level
    if body.upper() in categories:
        return redirect(url_for('subcategory_controller',
                                body=body,
                                p_id = participant.id,
                                s_id = participant.survey_id))

    # If conversation has not expired
    if session.get('conv_expires') > datetime.datetime.now():
        print 'conversation is still alive'
        try:
            if type(int(body)) == int:
                sub_categories = []
                for first_level_option in survey_json['question'].keys():
                    for second_level_option in survey_json['question'][first_level_option]['options'].keys():
                        sub_categories.append(second_level_option)

                if body in sub_categories:
                    print 'one of sub-categories chosen'

                    if session['response_logged'] != 1:
                        print 'response not yet logged, now will be logged'

                        response = twiml.Response()
                        response.message('Thanks! We logged your response.')
                        session['response_logged'] = 1
                        return str(response)

                    if session['response_logged'] == 1:
                        print 'but response was already logged'

                        response = twiml.Response()
                        response.message('There is no survey in progress. Please wait for next prompt!')
                        return str(response)

        except:
            response = twiml.Response()
            response.message('Did you have a typo? Please enter a number corresponding to your choice.')
            return str(response)

    if session.get('conv_expires') < datetime.datetime.now():
        response = twiml.Response()
        response.message('There is no survey in progress. Please wait for next prompt!')
        return str(response)






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

        response = twiml.Response()
        response.message(''.join(send_list))

        session['conv_expires'] = datetime.datetime.now() + datetime.timedelta(minutes=15)
        session['response_logged'] = 0
        session['last_answer'] = body

        return str(response)



if __name__ == '__main__':
    app.run()

