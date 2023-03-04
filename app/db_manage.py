from . import db
from .models import DataPoint
from datetime import date
from flask_login import current_user
import numpy


def add_user_data(data):
    user = current_user

    today = date(date.today().year, date.today().month, date.today().day)
    todays_entry = DataPoint.query.filter(DataPoint.user_id == user.id).filter(DataPoint.date_created == today).first()



    print(todays_entry)
    print(today)

    temp = numpy.average(data['temperature']).item()
    precip = numpy.sum(data['precipitation']).item()
    press = numpy.average(data['pressure']).item()

    # if there's already an entry today, update it with new data
    if todays_entry:
        print('updating db entry')
        props = {
            'mood_value' : data['mood'],
            'energy_value' : data['energy'],
            'temperature' : temp,
            'precipitation' : precip,
            'pressure' : press,
        }
        for key, value in props.items():
            setattr(todays_entry, key, value)
    # if its first submission today, add the data
    else:
        print('making new entry in the db')
        todays_entry = DataPoint(mood_value=data['mood'], energy_value=data['energy'],
        temperature=temp, precipitation=precip, pressure=press,
        user_id = user.id)
        db.session.add(todays_entry)

    db.session.commit()

    return
