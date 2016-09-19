from flask import Flask, render_template, request, url_for, flash, redirect
from flask.ext.sqlalchemy import SQLAlchemy
import config
import twilio.twiml
import os
import datetime
import json


app = Flask(__name__)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config.from_object(os.environ['APP_SETTINGS'])
db = SQLAlchemy(app)

from models import Survey, Question, Participant, Ping
from forms.new_survey import NewSurveyForm
from forms.new_participant import NewParticipantForm
from forms.add_participant import AddParticipantForm

# View to see all participants who have been added to the application
@app.route('/participants', methods=['GET', 'POST'])
def show_participants():
    form = NewParticipantForm(request.form)
    return render_template('participants.html',
                           participants=db.session.query(Participant).order_by(Participant.id).all(),
                           form=form)


# TODO use WTForms for this
# TODO move this function to the views module
# TODO Use phonenumber module to validate phone numbers that are added to the database.
@app.route('/create_participant', methods=['POST'])
def create_participant():
    form = NewParticipantForm(request.form)
    new_participant = Participant(**form.data)
    # new_participant.id = db.session.query(Participant).order_by(Participant.id.desc()).first().id + 1
    db.session.add(new_participant)
    db.session.commit()
    flash('Participant succesfully added!')
    return redirect(url_for('show_participants'))


# View to see all current surveys
@app.route('/surveys', methods=['GET'])
def show_surveys():
    form = NewSurveyForm(request.form)
    surveys = db.session.query(Survey).all()
    return render_template('surveys.html', surveys=surveys, form=form)


@app.route('/create_survey', methods=['POST'])
def create_survey():
    form = NewSurveyForm(request.form)
    surveys = db.session.query(Survey).all()

    new_survey = Survey(**form.data)
    new_survey.body = json.loads(form.data['body'])

    db.session.add(new_survey)
    db.session.commit()

    return render_template('surveys.html', surveys=surveys, form=form)


# View to add participants to a given survey
@app.route('/surveys/<id>', methods=['GET'])
def show_survey_id(id):
    survey = db.session.query(Survey).get(id)
    participants = db.session.query(Participant).filter(Participant.survey_id == id)
    form = AddParticipantForm(request.form).new()
    question_form = NewQuestionOneForm(request.form)
    questions = survey.body['question']

# for letter, branch in questions.iteritems():
#     for number, option in branch['options'].iteritems():
#         number, option
#
# for letter, branch in questions.iteritems():
#     branch

    return render_template('survey.html', survey=survey,
                           form=form, question_form=question_form, participants=participants, questions=questions)


@app.route('/add_participant', methods=['POST'])
def add_to_survey():
    form = AddParticipantForm(request.form).new()
    participant_id = form.data['new_participant']
    survey_id = int(str.split(request.referrer, "/")[-1])
    participant = db.session.query(Participant).filter(Participant.id == participant_id).one()
    participant.survey_id = survey_id
    db.session.commit()

    return redirect(url_for('show_survey_id', id=survey_id))


#
# with app.test_request_context():
#     print url_for('show_participants')
#     print url_for('add_to_survey')
#     print url_for('show_surveys')
#     print url_for('show_survey_id', id=1)


# endpoint for twilio POST reqests
# TODO move this to a separate views module..
@app.route('/message', methods=['GET', 'POST'])
def store_response():

    try:
        ping = {}

        # TODO make this do a lookup from participants
        # if the number is not in participants, do not store the ping in DB.
        ping['from_num'] = request.values['From']

        # TODO check if response is integer, otherwise store as string
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


