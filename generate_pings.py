import datetime
import random
import arrow
from app import db
from models import Ping

def gen_dates(start_date, duration):
    """
    yields a vector of days based on the duration provided, excludes
    weekdays.
    """
    for i in range(duration):
        if i > 0:
            # increment date only after the first iteration
            start_date += datetime.timedelta(1)
        if start_date.weekday() < 5:
            yield start_date

def gen_times(date, frequency):
    """
    yields times between 9 and 5 based on frequency given, completely randomly spaced out
    """
    choices = []
    for i in range(480):
        choices.append(i)

    for i in range(frequency):
        new_time = random.choice(choices)
        ping_time = datetime.datetime(year=date.year, month=date.month, day=date.day, hour=9, minute=0)
        ping_time += datetime.timedelta(minutes=new_time)
        yield ping_time


def gen_ping_object(start, duration, frequency, survey_id, participant_id):
    """
    Create dictionary to hold pings for a given person
    start: datetime.date(year, month, day)
    frequency: integer, number of pings in a day
    survey_id: id of survey
    participant_id: id of participant to add pings for
    """
    pings = {}
    ping_times = []
    start = start
    for day in gen_dates(start, duration):
        for time in gen_times(day, frequency):
            ping_times.append(time)
    pings['ping_times'] = ping_times
    pings['survey_id'] = survey_id
    pings['participant_id'] = participant_id
    return pings


# ping_obj = gen_ping_object(datetime.date(2016,10,5), 16, 1, 1)

def ping_loader(ping_obj):
    for ping_time in ping_obj['ping_times']:
        ping = {}
        ping['sent_time'] = ping_time
        ping['survey_id'] = ping_obj['survey_id']
        ping['participant_id'] = ping_obj['participant_id']
        print 'ping {} added'.format(ping)
        db.session.add(Ping(**ping))
        db.session.commit()


