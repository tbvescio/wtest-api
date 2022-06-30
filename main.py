import json
from flask import Flask, jsonify, request
from numpy import take
from sqlalchemy import true
app = Flask(__name__)

#TODO: validate params / sanitize input
#TODO: error cases

@app.route('/users')
def get_users():
  completed = request.args.get('completed')
  title = request.args.get('title')

  result = {"total_items": 0, "data": []}
  with open('users.json', 'r') as f:
    users = json.loads(f.read())
    result["total_items"] = len(users)
    result["data"] = users
  return jsonify(result)

@app.route('/users/<userId>')
def get_user_by_id(userId):
  result = {}
  with open('users.json', 'r') as f:
    users = json.loads(f.read())
    for user in users: 
      if user["id"] == int(userId):
        result = user
        break
  return jsonify(result)

@app.route('/tasks')
def get_tasks():
  completed = request.args.get('completed')
  title = request.args.get('title')

  result = {"total_items": 0, "data": []}

  with open('tasks.json', 'r') as f:
    tasks = json.loads(f.read())

    if not completed and not title:
      result["data"] = tasks
      result["total_items"] = len(result["data"])
      print("zukete")
      return jsonify(result)
      
    for task in tasks: 
      print("zuke", completed, task["completed"])
      if completed == "true" and task["completed"] == False: continue;
      if completed == "false" and task["completed"] == True: continue;

      if title and title not in task["title"]: continue;
      
      result["data"].append(task)

    result["total_items"] = len(result["data"])

  return jsonify(result)

@app.route('/tasks/<taskId>')
def get_tasks_by_id(taskId):
  result = {}

  with open('tasks.json', 'r') as f:
    tasks = json.loads(f.read())

    for task in tasks: 
      if task["id"] == int(taskId):
        result = task
        break
  return jsonify(result)

@app.route('/users/<userId>/tasks')
def get_tasks_by_userId(userId):
  result = {"total_items": 0, "data": []}

  with open('tasks.json', 'r') as f:
    tasks = json.loads(f.read())

    for task in tasks: 
      if task["user_id"] == int(userId):
        result["data"].append(task)

  result["total_items"] = len(result["data"])
  return jsonify(result)

if __name__ == '__main__':
    app.run(debug=True)

