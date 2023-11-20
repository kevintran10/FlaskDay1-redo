from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from flask_login import UserMixin
from werkzeug.security import generate_password_hash


# Creating the instance of the database
db = SQLAlchemy()

team = db.Table('team',
    db.Column('user_id', db.Integer, db.ForeignKey('user.id')),
    db.Column('pokemon_id', db.Integer, db.ForeignKey('pokemon.id'))
)

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String, nullable=False)
    last_name = db.Column(db.String, nullable=False)
    email = db.Column(db.String, unique=True, nullable=False)
    password = db.Column(db.String, nullable=False)
    created_on = db.Column(db.DateTime, default=datetime.utcnow())
    catch_pokemon = db.relationship('Pokemon',secondary = team, backref = db.backref('user'),lazy='dynamic')
                                                      

    def __init__(self,  first_name, last_name, email, password):
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.password = generate_password_hash(password)

class Pokemon(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, unique=True, nullable=False)
    ability_name = db.Column(db.String, nullable=False)
    attack_base_stat = db.Column(db.Integer, nullable=False)
    defense_base_stat = db.Column(db.Integer, nullable=False)
    hp_base_stat = db.Column(db.Integer, nullable=False)
    sprites = db.Column(db.String, nullable=False)
    created_on = db.Column(db.DateTime, default=datetime.utcnow())
                           
    def __init__(self, name, ability_name, attack_base_stat, defense_base_stat, hp_base_stat, sprites):
        self.name = name
        self.ability_name = ability_name
        self.attack_base_stat = attack_base_stat
        self.defense_base_stat = defense_base_stat
        self.hp_base_stat = hp_base_stat
        self.sprites = sprites
        
        

# class PokemonUser(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     pokeuser_id = db.Column(db.Integer, db.ForeignKey('user_id'), unique=True, nullable=False)
#     pokemon_id = db.Column(db.Integer, db.ForeignKey('name'), nullable=False)
