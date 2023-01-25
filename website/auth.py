from flask import Blueprint, render_template, redirect, url_for, request, flash, session
from . import db
from .models import User
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from .validate import validate_sign_up

auth = Blueprint('auth', __name__)

@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        user = User.query.filter_by(email=email).first()

        if user:
            if check_password_hash(user.password, password):
                flash('Logged in', category='success')
                login_user(user, remember=True)

                return redirect(url_for('views.home'))
            else:
                flash('Wrong password', category = 'error')
        else:
            flash('No account with this email has been found', category = 'error')

    if current_user.is_authenticated:
        return redirect(url_for('views.home'))

    return render_template('login.html')


@auth.route('/sign-up', methods=['GET', 'POST'])
def signup():

    if request.method == 'POST' and validate_sign_up():

        email = request.form.get('email')
        username = request.form.get('username')
        password = request.form.get('password')

        hashed_pass = generate_password_hash(password, method='sha256')
        new_user = User(email=email, username=username, password=hashed_pass)

        db.session.add(new_user)
        db.session.commit()

        login_user(new_user, remember=True)
        flash('User created')

        return redirect(url_for('views.home'))

    if current_user.is_authenticated:
        return redirect(url_for('views.home'))

    return render_template('signup.html')

@auth.route('/logout')
@login_required
def logout():
    session.clear()
    logout_user()
    return redirect(url_for('views.home'))
