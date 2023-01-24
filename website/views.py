from flask import Blueprint, render_template, request, redirect, url_for
from flask_login import current_user


views = Blueprint('views', __name__)


@views.route('/', methods=['GET','POST'])
@views.route('/home', methods=['GET','POST'])
def home():

    if request.method == 'POST':

        data = request.get_json()

        from .db_manage import add_user_data

        if current_user.is_authenticated:

            print('authenticated')
            add_user_data(data)

            return redirect(url_for('views.home'))

    return render_template('home.html')


@views.route('/mood-forecast', methods=['GET','POST'])
def forecast():
    if request.method == 'POST':
        # forecast for next 7 days
        data = request.get_json()
        print(data)

        from .calculations import mood_forecast
        # calculates mood forecast

        mood_forecast(data)

        return redirect(url_for('views.forecast'))


    return render_template('forecast.html')
