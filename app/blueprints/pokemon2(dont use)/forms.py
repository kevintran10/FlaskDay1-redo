from flask_wtf import FlaskForm
from wtforms import SubmitField, StringField
from wtforms.validators import DataRequired

class CatchForm(FlaskForm):
    name = StringField('Pokemon Name: ')
    poke_img_url=StringField('Pokemon Image URL: ', validators=[DataRequired()])
    catch_btn = SubmitField('Catch Pokemon!')
    