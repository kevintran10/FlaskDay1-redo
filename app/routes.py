from flask import request, render_template, redirect, url_for, flash
import requests
from app import app
from app.forms import LoginForm, SignupForm
from app.models import User, db
from werkzeug.security import check_password_hash
from flask_login import login_user, logout_user, current_user, login_required

# Home Route
@app.route('/')
@app.route('/home')
def home():
    return render_template('home.html')

REGISTERED_USER = {
    'example@email.com': {
        'name': 'Kevin Tran',
        'password': 'testpass123'
    }
}

# Login Route
@app.route('/login', methods=(['GET', 'POST']))
def login():
    form = LoginForm()
    if request.method == 'POST' and form.validate_on_submit():
        email = form.email.data
        password = form.password.data

        queried_user = User.query.filter(User.email == email).first()
        if queried_user and check_password_hash(queried_user.password, password):
            login_user(queried_user)
            flash(f'Hello, Pokemon Master {queried_user.first_name}!', 'success')
            return redirect(url_for('home'))
        else:          
            return 'Invalid email or password, please try again'
    else:
            return render_template('login.html', form=form)
    
# Sign up
@app.route('/signup', methods=(['GET', 'POST']))
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
        return redirect(url_for('login'))
    else:
        return render_template('signup.html', form=form)

# creating a logout route
@app.route('/logout')
@login_required
def logout():
    flash('Pokemon Master {first_name} has logged out', 'warning')
    logout_user()
    return redirect(url_for('login'))

# Pokemon Name/Pokedex Route  
@app.route('/pokemon_name', methods=['GET', 'POST'])
def get_pokemon_name():
    if request.method == 'POST':
        pokemon_name = request.form.get('pokemon_name')
        print(pokemon_name)
        url = f'https://pokeapi.co/api/v2/pokemon/{pokemon_name}'
        response = requests.get(url)
        poke_data = response.json()
        all_pokemon = get_pokemon_db(poke_data)
        print(all_pokemon)
        return render_template('form.html', all_pokemon=all_pokemon)
    else:
        return render_template('form.html')
    
def get_pokemon_db(data):
    new_pokemon_data = []

    pokemon_dictionary = {
        'name' : data['forms'][0]['name'],
        'ability_name' : data['abilities'][0]['ability']['name'],
        'base_experience' : data['base_experience'],
        'sprites' : data['sprites']['front_shiny'],
        'attack_base_stat' : data['stats'][1]['base_stat'],
        'hp_base_stat' : data['stats'][0]['base_stat'],
        'defense_base_stat' : data['stats'][2]['base_stat']
        }
    new_pokemon_data.append(pokemon_dictionary)
    return new_pokemon_data