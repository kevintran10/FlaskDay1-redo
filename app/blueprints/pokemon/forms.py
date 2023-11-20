from flask_wtf import FlaskForm
from wtforms import SubmitField, StringField
from wtforms.validators import DataRequired

class SearchPokemonForm(FlaskForm):
    name = StringField('Pokemon name: ', validators=[DataRequired()])
    search_btn = SubmitField('Search') 
    
class PokemonForm(FlaskForm):
    name = StringField('Pokemon Name: ')
    poke_img_url=StringField('Pokemon Image URL: ', validators=[DataRequired()])
    catch_btn = SubmitField('Catch Pokemon!')

