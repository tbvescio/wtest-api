from src.constants.http_status_codes import bad_request, is_success, not_found, server_error
import json
from flask import Blueprint, request
from flask.json import jsonify
from schema import Schema, SchemaError
from pathlib import Path

USERS_PATH = Path(__file__).parent / "data/users.json"
users = Blueprint("users", __name__)


@users.route('/users')
def get_users():
    """Retrieves all users
    ---
    definitions:
      Palette:
        type: object
        properties:
          palette_name:
            type: array
            items:
              $ref: '#/definitions/Color'
      Color:
        type: string
    responses:
      200:
        description: A list of colors (may be filtered by palette)
        schema:

        examples:
          rgb: ['red', 'green', 'blue']
    """
    try:
        result = {"total_items": 0, "data": []}
        with open(USERS_PATH, 'r') as f:
            users = json.loads(f.read())
            result["total_items"] = len(users)
            result["data"] = users
        return is_success(result)
    except:
        return server_error()


@users.route('/users/<userId>')
def get_user_by_id(userId):
    try:
        Schema(int).validate(userId)

        result = {}
        with open(USERS_PATH, 'r') as f:
            users = json.loads(f.read())
            for user in users:
                if user["id"] == int(userId):
                    result = user
                    break

        if result == {}:
            return not_found()
        return is_success(result)
    except SchemaError:
        return bad_request()
    except:
        return server_error()
