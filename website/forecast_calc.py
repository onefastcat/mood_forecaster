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

    moods = []
    energy = []

    print(moods_vals)

    for i, mood in  enumerate(moods_vals):
        print(i)
        if mood < 5:
            moods.append('lower')
        elif mood < 7:
            moods.append('average')
        elif mood < 9:
            moods.append('better')
        else:
            moods.append('great')

    for i, energy_val in  enumerate(energy_vals):
        if energy_val < 5:
            energy.append('lower')
        elif energy_val < 7:
            energy.append('average')
        elif energy_val < 9:
            energy.append('higher')
        else:
             energy.append('high')

    mood_energy_forecast = {'moods' : moods,
                             'energy' : energy}


    return mood_energy_forecast



def moodPrediction(futureTemp, futurePressure,  pastTemp, pastPressure):

    # set significant correlation value
    threshold_corr_value = .1
    # get mood correlations
    mood_temp_corr = mood_temp_calc()
    mood_pressure_corr = mood_pressure_calc()
    avg_past_temp = sum(pastTemp) / len(pastTemp)
    avg_past_pressure = sum(pastPressure) / len(pastPressure)
    moods = [5,5,5,5,5,5,5]


    # if mood directly correlates with temp., calculate change in mood
    if mood_temp_corr > threshold_corr_value:
        for i, temp in enumerate(futureTemp):
            if temp > avg_past_temp:
                moods[i] += 2
            elif temp < avg_past_temp:
                moods[i] -= 2

    if mood_pressure_corr > threshold_corr_value:
        for i, pressure in enumerate(futurePressure):
            if pressure > avg_past_pressure:
                moods[i] += 2
            if pressure < avg_past_pressure:
                moods[i] -= 2
    # if mood is inversly correlated with temperature
    elif mood_temp_corr < -threshold_corr_value:
        for i, temp in enumerate(futureTemp):
            if temp < avg_past_temp:
                moods[i] += 2
            elif temp > avg_past_temp:
                moods[i] -= 2

    elif mood_pressure_corr < -threshold_corr_value:
        for i, pressure in enumerate(futurePressure):
            if pressure < avg_past_pressure:
                moods[i] += 2
            elif pressure > avg_past_pressure:
                moods[i] -= 2

    return moods


def energyPrediction(futureTemp, futurePressure,  pastTemp, pastPressure):

     # set significant correlation value
    threshold_corr_value = .1
    # get mood correlations
    energy_temp_corr = energy_temp_calc()
    energy_pressure_corr = energy_pressure_calc()
    avg_past_temp = sum(pastTemp) / len(pastTemp)
    avg_past_pressure = sum(pastPressure) / len(pastPressure)
    energy = [5,5,5,5,5,5,5]


    # if mood directly correlates with temp., calculate change in mood
    if energy_temp_corr > threshold_corr_value:
        for i, temp in enumerate(futureTemp):
            if temp > avg_past_temp:
                energy[i] += 2
            elif temp < avg_past_temp:
                energy[i] -= 2

    if energy_pressure_corr > threshold_corr_value:
        for i, pressure in enumerate(futurePressure):
            if pressure > avg_past_pressure:
                energy[i] += 2
            if pressure < avg_past_pressure:
                energy[i] -= 2
    # if mood is inversly correlated with temperature
    elif energy_temp_corr < -threshold_corr_value:
        for i, temp in enumerate(futureTemp):
            if temp < avg_past_temp:
                energy[i] += 2
            elif temp > avg_past_temp:
                energy[i] -= 2

    elif energy_pressure_corr < -threshold_corr_value:
        for i, pressure in enumerate(futurePressure):
            if pressure < avg_past_pressure:
                energy[i] += 2
            elif pressure > avg_past_pressure:
                energy[i] -= 2


    return energy
