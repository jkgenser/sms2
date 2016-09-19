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

from models import Survey, Question, Participant, Ping
from forms.new_survey import NewSurveyForm
from forms.new_participant import NewParticipantForm
from forms.add_participant import AddParticipantForm
from forms.add_question import NewQuestionOneForm

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
    # new_survey.id = db.session.query(Survey).order_by(Survey.id.desc()).first().id + 1
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

    try:
        question_one_text = db.session.query(Question).\
            filter(Question.survey_id == id).filter(Question.\
            question_one_text != None).first().question_one_text
    except:
        question_one_text = 'Text not yet configured.'

    return render_template('survey.html', survey=survey,
                           form=form, question_form=question_form, participants=participants,
                           question_one_text=question_one_text)


@app.route('/add_participant', methods=['POST'])
def add_to_survey():
    form = AddParticipantForm(request.form).new()
    participant_id = form.data['new_participant']
    survey_id = int(str.split(request.referrer, "/")[-1])
    participant = db.session.query(Participant).filter(Participant.id == participant_id).one()
    participant.survey_id = survey_id
    db.session.commit()

    return redirect(url_for('show_survey_id', id=survey_id))


@app.route('/add_question_one', methods=['POST'])
def add_question_one():
    question_form = NewQuestionOneForm(request.form)
    survey_id = int(str.split(request.referrer, "/")[-1])

    q_template = ('What are you doing now? '
                  + ' '.join([question_form.data['option_one'],
                              ('(' + question_form.data['option_one_letter'] + ')'),
                              question_form.data['option_two'],
                              ('(' + question_form.data['option_two_letter'] + ')'),
                              question_form.data['option_three'],
                              ('(' + question_form.data['option_three_letter'] + ')')]
                             )
                  )
    letters = ','.join([question_form.data['option_one_letter'],
                                                   question_form.data['option_two_letter'],
                                                   question_form.data['option_three_letter']])

    if db.session.query(Question).filter(Question.survey_id == survey_id).count() == 0:
        question = {}
        question['survey_id'] = survey_id
        question['question_one_text'] = q_template
        question['question_one_letter'] = letters
        new_question = Question(**question)
        db.session.add(new_question)
        db.session.commit()
    else:
        q_to_update = db.session.query(Question).\
            filter(Question.survey_id == survey_id).\
            filter(Question.question_one_text != None).first()
        q_to_update.question_one_text = q_template
        q_to_update.question_one_letter = letters
        db.session.commit()

    return redirect(url_for('show_survey_id', id=survey_id))

@app.route('/add_question_two', methods=['POST'])
def add_question_two():
    question_form_2 = NewQuestionTwoForm(request.form)
    survey_id = int(str.split(request.referrer, "/")[-1])


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


