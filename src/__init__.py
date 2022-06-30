
from flask import Flask
from src.users import users
from src.tasks import tasks
from flasgger import Swagger

def create_app():
    app = Flask(__name__)

    app.register_blueprint(users)
    app.register_blueprint(tasks)


    Swagger(app)

    return app
