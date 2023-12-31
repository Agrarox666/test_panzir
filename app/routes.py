import sqlite3

from flask import jsonify, request
from flask import Flask
from app.database import (create_task,
                          get_tasks,
                          get_task,
                          update_task,
                          delete_task)

app = Flask(__name__)
app.config['DATABASE_NAME'] = "app/tasks.db"


def connection_to_db(database=app.config['DATABASE_NAME']):
    """Return connection to database."""
    return sqlite3.connect(database)


@app.route('/todo/api/v1.0/tasks', methods=['POST'])
def create_task_route():
    if not request.get_json(silent=True) or 'title' not in request.json:
        return jsonify({'error': 'Bad request'}), 400

    new_task_data = {
        'title': request.json['title'],
        'description': request.json.get('description', ''),
        'done': request.json.get('done', False)
    }

    new_task = create_task(new_task_data, connection_to_db())
    return jsonify({'task': new_task.__dict__}), 201


@app.route('/todo/api/v1.0/tasks', methods=['GET'])
def get_tasks_route():
    tasks = get_tasks(connection_to_db())
    if not tasks:
        return jsonify({'empty': True})
    return jsonify({'tasks': [task.__dict__ for task in tasks]})


@app.route('/todo/api/v1.0/tasks/<int:task_id>', methods=['GET'])
def get_task_route(task_id):
    task = get_task(task_id, connection_to_db())
    if task:
        return jsonify({'task': task.__dict__})
    else:
        return jsonify({'error': 'Not found'}), 404


@app.route('/todo/api/v1.0/tasks/<int:task_id>', methods=['PUT'])
def update_task_route(task_id):
    task_to_update = get_task(task_id, connection_to_db())
    if not task_to_update:
        return jsonify({'error': 'Not found'}), 404

    # check if data is correct and is not empty
    try:
        updated_data = request.json
        task_to_update.__dict__.update(updated_data)
    except TypeError:
        return jsonify({'error': 'Bad request'}), 400

    updated_task = update_task(task_id, updated_data, connection_to_db())
    return jsonify({'task': updated_task.__dict__})


@app.route('/todo/api/v1.0/tasks/<int:task_id>', methods=['DELETE'])
def delete_task_route(task_id):
    task_to_delete = get_task(task_id, connection_to_db())
    if not task_to_delete:
        return jsonify({'error': 'Not found'}), 404

    delete_task(task_id, connection_to_db())
    return jsonify({'result': True})
