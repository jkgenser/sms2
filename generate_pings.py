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
        start_date += datetime.timedelta(1)
        if start_date.weekday() < 5:
            yield start_date

def gen_times(date, frequency):
    """
    yields times between 9 and 5 based on frequency given, with slight random shocks
    added to the interval
    """
    ping = datetime.datetime(year=date.year, month=date.month, day=date.day, hour=9, minute=0)
    interval = 480 / frequency
    for i in range(frequency):
        new_interval = random.normalvariate(interval, interval/10)
        ping += datetime.timedelta(minutes = new_interval)
        yield ping


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
    for i in gen_dates(start, duration):
        for j in gen_times(i, frequency):
            ping_times.append(j)
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
        db.session.add(Ping(**ping))
        db.session.commit()


