from flask.ext.script import Manager
from flask.ext.migrate import Migrate, MigrateCommand
from flask_migrate import upgrade as upgrade_database
from app import app, db

manager = Manager(app)
migrate = Migrate(app, db)
manager.add_command('db', MigrateCommand)


@manager.command
def retrieve_scheduled_pings():
    twilio_account_sid = app.config['TWILIO_ACCOUNT_SID']
    twilio_auth_token = app.config['TWILIO_AUTH_TOKEN']
    twilio_number = app.config['TWILIO_NUMBER']
    from models import Participant, Survey, Ping
    from sqlalchemy import and_
    import datetime
    current_time = datetime.datetime.now()
    minutes_ago = current_time - datetime.timedelta(minutes=30)

    # Retrieve pings that need to be sent
    # Between 'minutes_ago' and 'current_time'
    try:
        all_pings = db.session.query(Ping).filter(and_(Ping.sent_time > minutes_ago, Ping.sent_time < current_time)).all()
    except NoResultFound:
        return
    for i in all_pings:
        # Code here for sending each of the prompts to the correct people

def send_prompt(ping):
    to = db.session.query(Participant).get(ping.participant_id).phone_number
    survey_json = db.session.query(Survey).get(ping.survey_id).body



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


if __name__ == "__main__":
    manager.run()

