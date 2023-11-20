from flask import Flask
from config import Config
from flask_login import LoginManager
from app.models import db, User
from flask_migrate import Migrate

app = Flask(__name__)
app.config.from_object(Config)

login_manager = LoginManager()

login_manager.init_app(app)
db.init_app(app)
migrate = Migrate(app, db)

# login_manager settings
login_manager.login_view = 'auth.login'
login_manager.login_message = 'Please log-in before you use this page.'
login_manager.login_message_category = 'dark'

# Import Blueprints
from app.blueprints.auth import auth
from app.blueprints.pokemon import pokemon

# Register Blueprints
app.register_blueprint(auth)
app.register_blueprint(pokemon)


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)

