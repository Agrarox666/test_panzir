from flask import Flask, jsonify, request

app = Flask(__name__)
# Input data
tasks = [
    {
        'id': 1,
        'title': u'Buy groceries',
        'description': u'Milk, Cheese, Pizza, Fruit, Tylenol',
        'done': False
    },
    {
        'id': 2,
        'title': u'Learn Python',
        'description': u'Need to find a good Python tutorial on the web',
        'done': False
    }
]


@app.route('/todo/api/v1.0/tasks', methods=['GET'])
def get_tasks():
    """Get all the tasks."""
    return jsonify({'tasks': tasks})


@app.route('/todo/api/v1.0/tasks/<int:task_id>', methods=['GET'])
def get_task(task_id):
    """Get a specific task by its ID."""
    selected_task = \
        (next((task for task in tasks if task['id'] == task_id), None))

    if selected_task is None:
        return jsonify({'error': 'Not found'}), 404

    return jsonify({'task': selected_task})


@app.route('/todo/api/v1.0/tasks', methods=['POST'])
def create_task():
    """Create a new task."""

    # request.json doesn't indicate type of data, request.get_json does
    if not request.get_json(silent=True) or 'title' not in request.json:
        return jsonify({'error': 'Bad request'}), 400

    new_task = {
        'id': tasks[-1]['id'] + 1,
        'title': request.json['title'],
        'description': request.json.get('description', ""),
        'done': False
    }
    tasks.append(new_task)
    return jsonify({'task': new_task}), 201


@app.route('/todo/api/v1.0/tasks/<int:task_id>', methods=['DELETE'])
def delete_task(task_id):
    """Delete a specific task by its ID."""
    task_to_delete = \
        (next((task for task in tasks if task['id'] == task_id), None))

    if task_to_delete is None:
        return jsonify({'error': 'Not found'}), 404

    tasks.remove(task_to_delete)
    return jsonify({'result': True})


@app.route('/todo/api/v1.0/tasks/<int:task_id>', methods=['PUT'])
def update_task(task_id):
    """Update a specific task by its ID."""
    task_to_update = \
        (next((task for task in tasks if task['id'] == task_id), None))
    if task_to_update is None:
        return jsonify({'error': 'Not found'}), 404

    # check if data is correct and is not empty
    try:
        new_task = request.json
        task_to_update.update(new_task)
    except TypeError:
        return jsonify({'error': 'Bad request'}), 400

    return jsonify({'task': task_to_update})


if __name__ == '__main__':
    app.run(debug=True)
