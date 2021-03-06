from flask import url_for, render_template, redirect, flash, g, Blueprint, request, jsonify
from flask_login import login_required, logout_user, login_user, current_user
from FoodOrderClient import app, db
from .models import Users


mod_auth = Blueprint('authentication', __name__)


@app.route('/login', methods=['GET','POST'])
def login():
    errorMsg = ''
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        user = Users.query.filter_by(email=email).first()
        if user is not None and user.authenticate(password):
            user.authenticated = True
            db.session.add(user)
            db.session.commit()
            login_user(user)
            flash('Thanks for logging in, {}'.format(current_user.email))
            return redirect(url_for('client.show_home', headerTitle='DigIn - Login'))
        else:
            errorMsg = 'Invalid Login! Try Again.'
    return render_template('login.html', headerTitle='DigIn - Login', errorMessage=errorMsg)


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'GET':
        return render_template('register.html')
    user = Users(request.form['firstname'], request.form['lastname'], request.form['email'], request.form['password'])
    db.session.add(user)
    db.session.commit()
    flash('User successfully registered')
    return redirect(url_for('authentication.login'))


@mod_auth.route('/logout')
@login_required
def logout():
    user = current_user
    user.authenticated = False
    db.session.add(user)
    db.session.commit()
    logout_user()
    flash('Goodbye!', 'info')
    return redirect(url_for('authentication.login'))


@mod_auth.route('/change_password', methods=['POST'])
@login_required
def change_password():
    old_password = request.form['old_password']
    new_password = request.form['new_password']
    if current_user.change_password(old_password, new_password):
        flash('Password changed successfully', 'info')
        return redirect(url_for('authentication.login'))
    else:
        flash('Some error occured', 'error')
        return redirect(url_for('authentication.change_password'))
