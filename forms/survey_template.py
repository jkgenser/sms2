{
    "title": "Survey for Care Partners",
    "prompt": "What are you doing now?",
    "question": {
        "A": {
            "text": "travel",
            "options":
                {
            "1": "travel_category_1",
            "2": "travel_category_2",
            "3": "travel_category_3",
                }
        },
        "B": {
            "text": "admin",
            "options":
                {
            "4": "admin_category_1",
            "5": "admin_category_2",
            "6": "admin_category_3",
                }
        },
        "C": {
            "text": "clinical",
            "options":
                {
            "7": "clinical_category_1",
            "8": "clinical_category_2",
            "9": "clinical_category_3",
            "10": "clinical_category_4"
                }
        },
    }
}

{"question": {"A": {"text": "travel", "options": {"1": "travel_category_1", "3": "travel_category_3", "2": "travel_category_2"}}, "C": {"text": "clinical", "options": {"9": "clinical_category_3", "8": "clinical_category_2", "7": "clinical_category_1", "10": "clinical_category_4"}}, "B": {"text": "admin", "options": {"5": "admin_category_2", "4": "admin_category_1", "6": "admin_category_3"}}}, "prompt": "What are you doing now?", "title": "Survey for Care Partners"}



from app import db
from models import Survey
import datetime
import random
date = db.session.query(Survey).get(6).start_date

def gen_dates(start_date, duration):
    for i in range(duration):
        start_date += datetime.timedelta(1)
        if start_date.weekday() < 5:
            yield start_date

def gen_times(date, frequency):
    ping = datetime.datetime(year=date.year, month=date.month, day=date.day, hour=9, minute=0)
    interval = 480 / frequency
    for i in range(frequency):
        new_interval = random.normalvariate(interval, interval/10)
        ping += datetime.timedelta(minutes = new_interval)
        yield ping



gen_dates(date, 10)




