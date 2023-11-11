from flask import request, render_template
import requests
from app import app
from app.forms import LoginForm

# Home Route
@app.route('/')
@app.route('/home')
def hello_pokemon_master():
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

        if email in REGISTERED_USER and REGISTERED_USER[email]['password'] == password:
            return f'Hello Pokemon Master, {REGISTERED_USER[email]["name"]}'
        else:
            return 'Invalid email or password, please try again'
    else:
            return render_template('login.html', form=form)

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