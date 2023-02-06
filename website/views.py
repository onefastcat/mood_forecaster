from flask import Blueprint, render_template, request, redirect, url_for, session, flash, get_flashed_messages, jsonify
from flask_login import current_user



views = Blueprint('views', __name__)


@views.route('/', methods=['GET','POST'])
@views.route('/home', methods=['GET','POST'])
def home():

    if request.method == 'POST':

        if current_user.is_authenticated:
            print('authed')
            print(request.get_json())
            data = request.get_json()
            from .db_manage import add_user_data
            add_user_data(data)
            flash('Data Submitted', category='message')
            return jsonify()
        else:
            flash('Please Log In to submit form', category='error')
            return jsonify(), 401

    return render_template('home.html')


@views.route('/mood-forecast', methods=['GET','POST'])
def forecast():
    from .models import DataPoint

    if current_user.is_authenticated:
        data_points_num  = len(DataPoint.query.filter(DataPoint.user_id == current_user.id).all())
        least_num_for_forecast = 7

        if data_points_num < least_num_for_forecast:
            flash(f'You need at least {least_num_for_forecast} days of data. You currently have {data_points_num}.')
            return redirect(url_for('views.home'))

        if request.method == 'POST' and data_points_num >= least_num_for_forecast:
            # forecast for next 7 days
            data = request.get_json()

            from .forecast_calc import mood_forecast

            # calculates mood/energy forecast
            forecast_data = mood_forecast(data)
            #store it in session
            session['forecast'] = forecast_data
            session['pressure'] = data['pressure']
            session['temp'] = data['temp']
            session['precip'] = data['precip']

        if 'forecast' in session:
            return render_template('forecast.html', forecast=session['forecast'], pressure=session['pressure'], temp=session['temp'], precip=session['precip'])

    else:

        flash('Please Log In to see mood forecast', category='error')
        return jsonify(), 401
