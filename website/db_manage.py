from . import db
from .models import DataPoint
from datetime import date
from flask_login import current_user




def add_user_data(data):
    user = current_user

    today = date(date.today().year, date.today().month, date.today().day)
    todays_entry = DataPoint.query.filter(DataPoint.user_id == user.id and
                        DataPoint.date_created == today).first()

    # # if there's already an entry today, update it with new data
    # if todays_entry:
    #     props = {
    #         'mood_value' : data['mood'],
    #         'energy_value' : data['energy'],
    #         'temperature' : data['temperature'],
    #         'precipitation' : data['precipitation'],
    #         'pressure' : data['pressure']
    #     }
    #     for key, value in props.items():
    #         setattr(todays_entry, key, value)
    # # if its first submission today, add the data
    # else:
    #     todays_entry = DataPoint(mood_value=data['mood'], energy_value=data['energy'],
    #     temperature=data['temperature'], precipitation=data['precipitation'], pressure=data['pressure'],
    #     user_id = user.id)
    #     db.session.add(todays_entry)


    # entry_1 = DataPoint(mood_value=3, energy_value=5,
    #   temperature=34, precipitation=1, pressure=1000,
    #     user_id = user.id, date_created=date(2023, 1, 1))
    # db.session.add(entry_1)

    # entry_2 = DataPoint(mood_value=4, energy_value=5,
    #   temperature=40, precipitation=3, pressure=1060,
    #     user_id = user.id, date_created=date(2023, 1, 2))
    # db.session.add(entry_2)

    # entry_3 = DataPoint(mood_value=9, energy_value=10,
    #   temperature=32, precipitation=0, pressure=1100,
    #     user_id = user.id, date_created=date(2023, 1, 3))
    # db.session.add(entry_3)

    # entry_4 = DataPoint(mood_value=7, energy_value=8,
    #   temperature=35, precipitation=1, pressure=1024,
    #     user_id = user.id, date_created=date(2023, 1, 4))
    # db.session.add(entry_4)

    # entry_5 = DataPoint(mood_value=10, energy_value=7,
    #   temperature=44, precipitation=2, pressure=1000,
    #     user_id = user.id, date_created=date(2023, 1, 5))
    # db.session.add(entry_5)



    # DataPoint.query.delete()
    db.session.commit()

    # entries = DataPoint.query.filter(DataPoint.user_id == user.id).all()
    # print(entries)


    return
