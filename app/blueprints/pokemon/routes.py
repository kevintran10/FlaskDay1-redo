from . import pokemon
from flask import render_template, request, flash, redirect, url_for
from flask_login import login_required, current_user
import requests
from app.models import Pokemon, db
from .forms import SearchPokemonForm

# Home Route
@pokemon.route('/')
@pokemon.route('/home')
def home():
    return render_template('home.html')


# Pokemon Name/Pokedex Route  
@pokemon.route('/pokemon_name', methods=['GET', 'POST'])
@login_required
def get_pokemon_name():
    form = SearchPokemonForm()
    if request.method == 'POST' and form.validate_on_submit():
        pokemon_name= form.name.data.lower()
        print(pokemon_name)
        poke_query = Pokemon.query.filter(Pokemon.name==pokemon_name).first()
        print(poke_query)
        if poke_query:
            return  render_template('pokemon_name.html', poke=poke_query, form=form)
        else:
            try:
                url = f'https://pokeapi.co/api/v2/pokemon/{pokemon_name}'
                response = requests.get(url)
                poke_data = response.json()
                pokemon_dictionary = {
                    'name' : poke_data['forms'][0]['name'],
                    'ability_name' : poke_data['abilities'][0]['ability']['name'],
                    'sprites' : poke_data['sprites']['front_shiny'],
                    'attack_base_stat' : poke_data['stats'][1]['base_stat'],
                    'hp_base_stat' : poke_data['stats'][0]['base_stat'],
                    'defense_base_stat' : poke_data['stats'][2]['base_stat']
                }
                poke = Pokemon(name=pokemon_dictionary['name'], ability_name=pokemon_dictionary['ability_name'], 
                    attack_base_stat=pokemon_dictionary['attack_base_stat'], hp_base_stat=pokemon_dictionary['hp_base_stat'],
                    defense_base_stat=pokemon_dictionary['defense_base_stat'], sprites=pokemon_dictionary['sprites'])
            
                db.session.add(poke)
                db.session.commit()
                return render_template('pokemon_name.html', poke=poke, form=form)
            except:
                return render_template('pokemon_name.html', form=form)
    else:
        return render_template('pokemon_name.html', form=form)


@pokemon.route('/catch/<int:pokemon_id>', methods=['POST'])
@login_required
def catch_Pokemon(pokemon_id):
# query the Pokemon from the database using .filter because using id
    try:
        caught_pokemon = Pokemon.query.filter(id=pokemon_id).first()

# create boolean statements for caught or not
        if not caught_pokemon:
            flash(f"{pokemon_id} isn't on your team!", "danger")
            return redirect(url_for('pokemon.home'))
        
        if caught_pokemon in current_user.pokmeon: 
            flash(f"{pokemon_id} is already on your team!", "warning")
            return redirect(url_for('pokemon.home'))
        
# add to the team
        current_user.pokemon.append(caught_pokemon)
        
        db.session.commit()
        flash(f"Hooray! You have caught {caught_pokemon.name}!", "success")
        return redirect(url_for('pokemon.home'))

    except: 
        flash(f"Oopsy! Invalid, try again.", "danger")
        return redirect(url_for('pokemon.home'))


@pokemon.route('/release/<int:pokemon_id>', methods=['POST'])
@login_required
def release_Pokemon(pokemon_id):
    try:
# query the Pokemon from database again using .filter method because of id
        rel_pokemon = Pokemon.query.filter(id=pokemon_id)

# create a boolean(if statement) to check if the pokemon IS on the team
        if not rel_pokemon:
            flash(f"{pokemon_id} is not available!", "danger")
            return redirect(url_for('pokemon.hom'))
        
        if rel_pokemon not in current_user.pokemon:
            flash(f"{pokemon_id} is not currently on your team!", "warning")
            return redirect(url_for('pokemon.home'))

# remove from the team
        current_user.pokemon.remove(rel_pokemon)
        
        db.session.commit()
        flash(f"You have released {rel_pokemon.name} from your team!", 'success')
        return redirect(url_for('pokemon.home'))
    except: 
        flash(f"Oopsy! Invalid, try again.", "danger")
        return redirect(url_for('pokemon.home'))
   