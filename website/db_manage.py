from . import db
from .models import DataPoint
from datetime import date
from flask_login import current_user
import numpy




def add_user_data(data):
    user = current_user

    today = date(date.today().year, date.today().month, date.today().day)
    todays_entry = DataPoint.query.filter(DataPoint.user_id == user.id and
                        DataPoint.date_created == today).first()

    # if there's already an entry today, update it with new data
    if todays_entry:
        props = {
            'mood_value' : data['mood'],
            'energy_value' : data['energy'],
            'temperature' : numpy.average(data['temperature']),
            'precipitation' : numpy.sum(data['precipitation']),
            'pressure' : numpy.average(data['pressure']),
        }
        for key, value in props.items():
            setattr(todays_entry, key, value)
    # if its first submission today, add the data
    else:
        todays_entry = DataPoint(mood_value=data['mood'], energy_value=data['energy'],
        temperature=data['temperature'], precipitation=data['precipitation'], pressure=data['pressure'],
        user_id = user.id)
        db.session.add(todays_entry)




    # DataPoint.query.delete()
    db.session.commit()

    # entries = DataPoint.query.filter(DataPoint.user_id == user.id).all()
    # print(entries)


    return
