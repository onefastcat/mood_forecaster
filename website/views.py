from flask import Blueprint, render_template, request, redirect, url_for
from flask_login import current_user


views = Blueprint('views', __name__)


@views.route('/', methods=['GET','POST'])
@views.route('/home', methods=['GET','POST'])
def home():

    if request.method == 'POST':

        data= request.get_json()

        from .db_manage import add_user_data

        if current_user.is_authenticated:
            from .calculations import mood_temp_calc, mood_precip_calc, mood_pressure_calc, \
                                        energy_temp_calc, energy_precip_calc, energy_pressure_calc
            print('authenticated')
            add_user_data(data)
            mood_temp_corr = mood_temp_calc()
            mood_precip_corr = mood_precip_calc()
            mood_pressure_corr = mood_pressure_calc()

            energy_temp_corr = energy_temp_calc()
            energy_precip_corr = energy_precip_calc()
            energy_pressure_corr = energy_pressure_calc()


            print(mood_temp_corr)
            print(mood_precip_corr)
            print(mood_pressure_corr)

            print(energy_temp_corr)
            print(energy_precip_corr)
            print(energy_pressure_corr)

            return redirect(url_for('views.home'))

    return render_template('home.html')
