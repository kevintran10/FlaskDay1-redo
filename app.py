from flask import Flask, request, render_template
import requests

app = Flask(__name__)

# Routings
@app.route('/')
@app.route('/home')
def hello_pokemon_master():
    return '<h1>Welcome to the Pokedex, Pokemon Trainer!</h1>'

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