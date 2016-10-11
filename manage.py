from flask.ext.script import Manager
from flask.ext.migrate import Migrate, MigrateCommand
from flask_migrate import upgrade as upgrade_database
from twilio.rest import TwilioRestClient as Client
from app import app, db
from models import Participant, Survey, Ping
import arrow

manager = Manager(app)
migrate = Migrate(app, db)
manager.add_command('db', MigrateCommand)

twilio_account_sid = app.config['TWILIO_ACCOUNT_SID']
twilio_auth_token = app.config['TWILIO_AUTH_TOKEN']
twilio_number = app.config['TWILIO_NUMBER']
client = Client(twilio_account_sid, twilio_auth_token)


@manager.command
def retrieve_scheduled_pings():

    # from models import Participant, Survey, Ping
    from sqlalchemy import and_
    import datetime
    current_time = datetime.datetime.utcnow()
    current_time = current_time - datetime.timedelta(hours=4)
    minutes_ago = current_time - datetime.timedelta(minutes=30)

    # Retrieve pings that need to be sent
    # Between 'minutes_ago' and 'current_time'
    try:
        all_pings = db.session.query(Ping).filter(and_(Ping.sent_time > minutes_ago,
                                                       Ping.sent_time < current_time)).all()
    except:
        return

    for ping in all_pings:
        send_prompt(ping)


def send_prompt(ping):
    # Get the number of the person to send a text to
    to = db.session.query(Participant).get(ping.participant_id).phone_number

    # Get the survey instrument for the person I'm sending the text to
    survey_json = db.session.query(Survey).get(ping.survey_id).body
    body = '{0} A ({1}), B ({2}), or C ({3})?'.format(survey_json['prompt'],
                                                   survey_json['question']['A']['text'],
                                                   survey_json['question']['B']['text'],
                                                   survey_json['question']['C']['text'])

    client.messages.create(
        to=to,
        from_=twilio_number,
        body=body)
    return



@manager.command
def add_pings(start_year, start_month, start_day, duration, frequency, survey_id, participant_id):
    from generate_pings import gen_dates, gen_times, gen_ping_object, ping_loader
    from datetime import datetime

    start_year = int(start_year)
    start_month = int(start_month)
    start_day = int(start_day)
    duration = int(duration)
    frequency = int(frequency)
    survey_id = int(survey_id)
    participant_id = int(participant_id)

    start_date = datetime(start_year, start_month, start_day)
    ping_obj = gen_ping_object(start_date, duration, frequency, survey_id, participant_id)
    ping_loader(ping_obj)


@manager.command
def add_survey(name, survey_name):
    from forms import surveys
    survey = {}
    survey['name'] = name
    survey['body'] = surveys.survey_dict[survey_name]

    db.session.add(Survey(**survey))
    db.session.commit()
    print 'survey added!'


@manager.command
def add_participant(name,phone_number,role,location,survey_id):
    participant = {}
    participant['name'] = name
    participant['phone_number'] = phone_number
    participant['role'] = role
    participant['location'] = location
    participant['survey_id'] = int(survey_id)

    db.session.add(Participant(**participant))
    db.session.commit()
    print 'participant added!'



if __name__ == "__main__":
    manager.run()

