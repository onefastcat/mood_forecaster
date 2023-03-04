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


def validate_data(data):
    if data.count(data[0]) == len(data):
        return False

    return True


def mood_temp_calc():

    if (not validate_data(mood_list)) or (not validate_data(temperature)):
        return None

    mood_temp_corr = np.corrcoef(mood_list, temperature)[0,1]

    return mood_temp_corr


def mood_precip_calc():

    if (not validate_data(mood_list)) or (not validate_data(precipitation)):
        return None

    mood_precip_corr = np.corrcoef(mood_list, precipitation)[0,1]

    return mood_precip_corr


def mood_pressure_calc():

    if (not validate_data(mood_list)) or (not validate_data(pressure)):
        return None

    mood_pressure_corr = np.corrcoef(mood_list, pressure)[0,1]

    return mood_pressure_corr


def energy_temp_calc():

    if (not validate_data(energy_list)) or (not validate_data(temperature)):
        return None

    energy_temp_corr = np.corrcoef(energy_list, temperature)[0,1]

    return energy_temp_corr

def energy_precip_calc():

    if (not validate_data(energy_list)) or (not validate_data(precipitation)):
        return None

    energy_precip_corr = np.corrcoef(energy_list, precipitation)[0,1]

    return energy_precip_corr


def energy_pressure_calc():

    if (not validate_data(energy_list)) or (not validate_data(pressure)):
        return None

    energy_pressure_corr = np.corrcoef(energy_list, pressure)[0,1]

    return energy_pressure_corr
