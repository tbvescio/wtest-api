import json
from flask import Blueprint, request
from flask.json import jsonify
from schema import Schema, SchemaError, Or
from pathlib import Path
from src.constants.http_status_codes import bad_request, is_success, server_error
from flasgger import swag_from


TASKS_PATH = Path(__file__).parent / "data/tasks.json"
tasks = Blueprint("tasks", __name__)


@tasks.route('/tasks')
@swag_from('./swagger/get_tasks.yml')
def get_tasks():
    try:
        completed = request.args.get('completed')
        Schema(Or("true", "false", None)).validate(completed)
        title = request.args.get('title')

        result = {"total_items": 0, "data": []}
        with open(TASKS_PATH, 'r') as f:
            tasks = json.loads(f.read())
            if not completed and not title:
                result["data"] = tasks
                result["total_items"] = len(result["data"])
                return jsonify(result)

            for task in tasks:
                if completed == "true" and task["completed"] == False:
                    continue
                if completed == "false" and task["completed"] == True:
                    continue
                if title not in task["title"]:
                    continue

                result["data"].append(task)
        result["total_items"] = len(result["data"])
        return is_success(result)
    except SchemaError:
        return bad_request()
    except:
        return server_error()


@tasks.route('/tasks/<taskId>')
@swag_from('./swagger/get_task_by_id.yml')
def get_task_by_id(taskId):
    try:
        Schema(int).validate(taskId)
        result = {}

        with open(TASKS_PATH, 'r') as f:
            tasks = json.loads(f.read())

            for task in tasks:
                if task["id"] == int(taskId):
                    result = task
                    break
        return is_success(result)
    except SchemaError:
        return bad_request()
    except:
        return server_error()


@tasks.route('/users/<userId>/tasks')
@swag_from('./swagger/get_tasks_by_userId.yml')
def get_tasks_by_userId(userId):
    try:
        Schema(int).validate(userId)
        result = {"total_items": 0, "data": []}

        with open(TASKS_PATH, 'r') as f:
            tasks = json.loads(f.read())

            for task in tasks:
                if task["user_id"] == int(userId):
                    result["data"].append(task)

        result["total_items"] = len(result["data"])
        return jsonify(result)
    except SchemaError:
        return bad_request()
    except:
        return server_error()
