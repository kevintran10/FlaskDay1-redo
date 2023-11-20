from app.blueprints.auth import auth
from .forms import LoginForm, SignupForm
from flask import request, flash, redirect, render_template, url_for
from app.models import User, db
from werkzeug.security import check_password_hash
from flask_login import login_user, logout_user, current_user, login_required


# Login Route
@auth.route('/login', methods=(['GET', 'POST']))
def login():
    form = LoginForm()
    if request.method == 'POST' and form.validate_on_submit():
        email = form.email.data
        password = form.password.data

        queried_user = User.query.filter(User.email == email).first()
        if queried_user and check_password_hash(queried_user.password, password):
            login_user(queried_user)
            flash(f'Hello, Pokemon Master {queried_user.first_name}!', 'success')
            return redirect(url_for('pokemon.home'))
        else:          
            return 'Invalid email or password, please try again'
    else:
            return render_template('login.html', form=form)
    
# Sign up
@auth.route('/signup', methods=(['GET', 'POST']))
def signup():
    form = SignupForm()
    if request.method == 'POST' and form.validate_on_submit():
        first_name = form.first_name.data
        last_name = form.last_name.data
        email = form.email.data
        password = form.password.data
        
        # creating an instance of our User Class
        user = User(first_name, last_name, email, password)

        db.session.add(user)
        db.session.commit()
        # REGISTERED_USER[email] = {
        #     'name': full_name,
        #     'password': password
        # }

        flash(f'Thank you for signing up {first_name}!', 'success')
        return redirect(url_for('auth.login'))
    else:
        return render_template('signup.html', form=form)

# creating a logout route
@auth.route('/logout')
@login_required
def logout():
    flash('Pokemon Master has logged out', 'warning')
    logout_user()
    return redirect(url_for('auth.login'))