from . import pokemon
from flask import request, render_template, flash, redirect, url_for 
from app.models import db, Pokemon, main
from flask_login import current_user, login_required
import requests

# Home Route
@main.route('/')
@main.route('/home')
def home():
    return render_template('home.html')


# Pokemon Name/Pokedex Route  
@main.route('/pokemon_name', methods=['GET', 'POST'])
@login_required
def get_pokemon_name():
    if request.method == 'POST':
        poke_query = Pokemon.query.get('pokemon_name')
        pokemon_name = request.form.get('pokemon_name')
        url = f'https://pokeapi.co/api/v2/pokemon/{pokemon_name}'
        response = requests.get(url)
        poke_data = response.json()
        all_pokemon = get_pokemon_db(poke_data)
        
        return render_template('form.html', all_pokemon=all_pokemon)
    else:
        url = f'https://pokeapi.co/api/v2/pokemon/{pokemon_name}'
        response = requests.get(url)
        poke_data = response.json()
        all_pokemon = get_pokemon_db(poke_data)

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













# Creating Catch route
@pokemon.route('/catch', methods=["GET", "POST"])
@login_required
def catch_pokemon_team():
    form = CatchForm()

# trying to catch/pull the pokemon into the db
    # need to add restrictions of no more then 6 pokemons
    if len(current_user.team) >= 6:
        flash(f"Your team is full. Release a Pokemon if you want to catch more Pokemon's.", "warning")
        return redirect(url_for('main.pokemon_name'))
    # pkmn = Pokemon.query.get({name})
    # if request.method == "POST":
    #     name = Pokemon.name.data
    #     ability = Pokemon.ability_name.data
    #     attack_base_stat = Pokemon.attack_base_stat.data
    #     defense_base_stat = Pokemon.defense_base_stat.data
    #     hp_base_stat = Pokemon.hp_base_stat.data
    #     sprites = Pokemon.sprites.data
    #     user_id = current_user.id
            
# checking to see pokemon teams status 


# Need to add the Pokemon to the team (creating instance?)
    pokemon_team = Pokemon(name, ability, attack_base_stat, defense_base_stat, hp_base_stat, sprites, user_id)
    
    db.session.add(pokemon_team)
    db.session.commit()

    flash(f'{name} has been added to the team.', 'success')
    return redirect(url_for('main.pokemon_name'))
