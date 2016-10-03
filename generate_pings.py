def gen_dates(start_date, duration):
    '''
    yields a vector of days based on the duration provided, excludes
    weekdays.
    '''
    for i in range(duration):
        start_date += datetime.timedelta(1)
        if start_date.weekday() < 5:
            yield start_date

def gen_times(date, frequency):
    '''
    yields times between 9 and 5 based on frequency given, with slight random shocks
    added to the interval
    '''
    ping = datetime.datetime(year=date.year, month=date.month, day=date.day, hour=9, minute=0)
    interval = 480 / frequency
    for i in range(frequency):
        new_interval = random.normalvariate(interval, interval/10)
        ping += datetime.timedelta(minutes = new_interval)
        yield ping