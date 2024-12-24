from flask import Flask, render_template
from config import Config
from models import *
from routes import routes
from flask_login import LoginManager
from api_routes import api_routes

app = Flask(__name__)
app.config.from_object(Config)

db.init_app(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'

with app.app_context():
    db.create_all()

app.register_blueprint(routes)
app.register_blueprint(api_routes)

@app.route('/')
def home():
    return render_template('home.html')

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

if __name__ == '__main__':
    app.run(debug=True)
