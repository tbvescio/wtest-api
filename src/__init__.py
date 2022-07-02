
from flask import Flask
from src.users import users
from src.tasks import tasks
from flasgger import Swagger
from flask_cors import CORS

def create_app():
    app = Flask(__name__)

    CORS(app)

    app.register_blueprint(users)
    app.register_blueprint(tasks)

    Swagger(app)

    return app
