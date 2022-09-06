from dateutil.relativedelta import relativedelta
from datetime import datetime


def generateEmployeeEmail(name, lastname, company):
    email = name + '.' + lastname + '@' + company + '.com'
    email = email.replace(" ", "_").lower()
    return email


def generateEmployeeExperience(startdate, experience):
    now1 = datetime.now()
    now = datetime.date(now1)
    rdelta = relativedelta(now, startdate)
    time = float(rdelta.years) + experience
    return time