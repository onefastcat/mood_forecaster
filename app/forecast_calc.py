from .calculations import mood_pressure_calc, mood_temp_calc, energy_temp_calc, energy_pressure_calc


# returns an object with 'mood' and 'energy' lists. Each list has values for the next 7 days of the week
# these values will be used by a template and displayd next for each day forecast
def mood_forecast(data):

    # extract data for each weather metric
    pressure = data['pressure']
    temp = data['temp']

    historical_temp = data['historical_temp']
    historical_pressure = data['historical_pressure']

    moods_vals = moodPrediction(temp, pressure, historical_temp, historical_pressure)
    energy_vals = energyPrediction(temp, pressure, historical_temp, historical_pressure)

    if not moods_vals:
        print('no mood')
        moods_vals = [-100]*7

    if not energy_vals:
        print('no energy')
        energy_vals = [-100]*7

    mood_labels = []
    energy_labels = []

    for i, mood in  enumerate(moods_vals):
        if mood == -100:
            mood_labels.append('no data')
        elif mood < 5:
            mood_labels.append('lower')
        elif mood < 7:
            mood_labels.append('average')
        elif mood < 9:
            mood_labels.append('better')
        else:
            mood_labels.append('great')

    for i, energy_val in  enumerate(energy_vals):
        if energy_val == -100:
            energy_labels.append('no data')
        elif energy_val < 5:
            energy_labels.append('lower')
        elif energy_val < 7:
            energy_labels.append('average')
        elif energy_val < 9:
            energy_labels.append('higher')
        else:
            energy_labels.append('high')

    mood_energy_forecast = {'moods' : mood_labels,
                             'energy' : energy_labels}

    return mood_energy_forecast



def moodPrediction(futureTemp, futurePressure,  pastTemp, pastPressure):

    # set significant correlation value
    threshold_corr_value = .7
    # get mood correlations
    mood_temp_corr = mood_temp_calc()
    mood_pressure_corr = mood_pressure_calc()
    avg_past_temp = sum(pastTemp) / len(pastTemp)
    avg_past_pressure = sum(pastPressure) / len(pastPressure)
    base_moods = [5,5,5,5,5,5,5]

    if not mood_temp_corr and not mood_pressure_corr:
        return None

    # if mood directly correlates with temp., calculate change in mood
    if mood_temp_corr and mood_temp_corr > threshold_corr_value:
        for i, temp in enumerate(futureTemp):
            if temp > avg_past_temp:
                base_moods[i] += 2
            elif temp < avg_past_temp:
                base_moods[i] -= 2
    # if mood directly correlates with pressure, calculate change in mood
    if mood_pressure_corr and mood_pressure_corr > threshold_corr_value:
        for i, pressure in enumerate(futurePressure):
            if pressure > avg_past_pressure:
                base_moods[i] += 2
            if pressure < avg_past_pressure:
                base_moods[i] -= 2
    # if mood is inversly correlated with temperature
    elif mood_temp_corr and mood_temp_corr < -threshold_corr_value:
        for i, temp in enumerate(futureTemp):
            if temp < avg_past_temp:
                base_moods[i] += 2
            elif temp > avg_past_temp:
                base_moods[i] -= 2
    # if mood is inversly correlated with pressure
    elif mood_pressure_corr and mood_pressure_corr < -threshold_corr_value:
        for i, pressure in enumerate(futurePressure):
            if pressure < avg_past_pressure:
                base_moods[i] += 2
            elif pressure > avg_past_pressure:
                base_moods[i] -= 2

    return base_moods


def energyPrediction(futureTemp, futurePressure,  pastTemp, pastPressure):

    # set significant correlation value
    threshold_corr_value = .7
    # get mood correlations
    energy_temp_corr = energy_temp_calc()
    energy_pressure_corr = energy_pressure_calc()
    avg_past_temp = sum(pastTemp) / len(pastTemp)
    avg_past_pressure = sum(pastPressure) / len(pastPressure)
    base_energy = [5,5,5,5,5,5,5]

    if not energy_temp_corr and not energy_pressure_corr:
        return None

    # if mood directly correlates with temp., calculate change in mood
    if energy_temp_corr and energy_temp_corr > threshold_corr_value:
        for i, temp in enumerate(futureTemp):
            if temp > avg_past_temp:
                base_energy[i] += 2
            elif temp < avg_past_temp:
                base_energy[i] -= 2

    if energy_pressure_corr and energy_pressure_corr > threshold_corr_value:
        for i, pressure in enumerate(futurePressure):
            if pressure > avg_past_pressure:
                base_energy[i] += 2
            if pressure < avg_past_pressure:
                base_energy[i] -= 2
    # if mood is inversly correlated with temperature
    elif energy_temp_corr and energy_temp_corr < -threshold_corr_value:
        for i, temp in enumerate(futureTemp):
            if temp < avg_past_temp:
                base_energy[i] += 2
            elif temp > avg_past_temp:
                base_energy[i] -= 2

    elif energy_pressure_corr and energy_pressure_corr < -threshold_corr_value:
        for i, pressure in enumerate(futurePressure):
            if pressure < avg_past_pressure:
                base_energy[i] += 2
            elif pressure > avg_past_pressure:
                base_energy[i] -= 2


    return base_energy
