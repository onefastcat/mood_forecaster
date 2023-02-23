from flask import request, flash
from .models import User


def validate_sign_up():
    email = request.form.get('email')
    username = request.form.get('username')
    password1 = request.form.get('password')
    password2 = request.form.get('password_reenter')

    email_exists = User.query.filter_by(email=email).first()
    user = User.query.filter_by(username=username).first()

    if email_exists:
        flash('There is already an account assosiated with this email', category='error')
        return False
    elif user:
        flash('This username is taken', category='error')
        return False
    elif password1 != password2:
        flash('Passwords don\'t match', category='error')
        return False
    elif len(username) < 4:
        flash('Username is too short', category='error')
        return False
    elif len(password1) < 8:
        flash('Password is too short', category='error')
        return False

    return True
