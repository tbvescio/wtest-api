
from flask import Flask
from src.users import users
from src.tasks import tasks
from flasgger import Swagger, LazyString
from flask_cors import CORS


def create_app():
    app = Flask(__name__)

    CORS(app)

    app.register_blueprint(users)
    app.register_blueprint(tasks)

    template = {
        "info": {
            "title": "Wazuh Test API",
            "version": "0.0.1"
        },
        "schemes": [
            "http",
            "https"
        ],
    }
    Swagger(app, template=template)

    return app
