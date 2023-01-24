import numpy as np
from flask_login import current_user
from .models import DataPoint
from .models import db


#get current_user's data lists

mood_list = [val for (val,) in db.session.query(DataPoint.mood_value).filter(DataPoint.user_id == current_user.id).all()]
energy_list = [val for (val,) in db.session.query(DataPoint.energy_value).filter(DataPoint.user_id == current_user.id).all()]
temperature = [val for (val,) in db.session.query(DataPoint.temperature).filter(DataPoint.user_id == current_user.id).all()]
precipitation = [val for (val,) in db.session.query(DataPoint.precipitation).filter(DataPoint.user_id == current_user.id).all()]
pressure = [val for (val,) in db.session.query(DataPoint.pressure).filter(DataPoint.user_id == current_user.id).all()]


def mood_temp_calc():

    mood_temp_corr = np.corrcoef(mood_list, temperature)[0,1]

    return mood_temp_corr


def mood_precip_calc():

    mood_precip_corr = np.corrcoef(mood_list, precipitation)[0,1]

    return mood_precip_corr


def mood_pressure_calc():

    mood_pressure_corr = np.corrcoef(mood_list, pressure)[0,1]

    return mood_pressure_corr


def energy_temp_calc():

    energy_temp_corr = np.corrcoef(energy_list, temperature)[0,1]

    return energy_temp_corr

def energy_precip_calc():

    energy_precip_corr = np.corrcoef(energy_list, precipitation)[0,1]

    return energy_precip_corr


def energy_pressure_calc():

    energy_pressure_corr = np.corrcoef(energy_list, pressure)[0,1]

    return energy_pressure_corr



# returns an object with 'mood' and 'energy' lists. Each list has values for the next 7 days of the week
# these values will be used by a template and displayd next for each day forecast
def mood_forecast(data):

    # extract data for each weather metric
    pressure = data['pressure']
    temp = data['temp']
    precip = data['precip']
    historical_temp = data['historical_temp']
    historical_pressure = data['historical_pressure']
    historical_precip = data['historical_precip']

    # calculate historical averages
    avg_historical_temp = sum(historical_temp) / len(historical_temp)
    avg_historical_pressure = sum(historical_pressure) / len(historical_pressure)
    avg_historical_precip = sum(historical_precip) / len(historical_pressure)

    # get mood and energy correlations
    mood_temp_corr = mood_temp_calc()

    #check what mood and energy to expect
    # later change the .1 to .7
    if mood_temp_corr >= .1:
        if temp[0] > avg_historical_temp:
            print('expect good mood')
        else:
            print(temp[0])
            print(avg_historical_temp)
            print('expect bad mood')
