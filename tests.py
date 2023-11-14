from app import tasks as test_data_tasks, app

error_messages = {
    400: 'Bad request',
    404: 'Not found',
}

client = app.test_client()


def test_create_task():
    """Test creating tasks."""
    new_task = {
        'id': len(test_data_tasks) + 1,
        'title': 'Test task\'s title',
        'description': 'Test task\'s description',
        'done': False
    }
    response = client.post('/todo/api/v1.0/tasks', json=new_task)
    data = response.get_json()

    assert response.status_code == 201
    assert 'task' in data
    assert data['task'] == test_data_tasks[-1]

    # test task without title
    bad_task_1 = {
        'id': len(test_data_tasks) + 1,
        'description': 'Test task\'s description',
        'done': False
    }
    response = client.post('/todo/api/v1.0/tasks', json=bad_task_1)
    data = response.get_json()

    assert response.status_code == 400
    assert 'error' in data
    assert data['error'] == error_messages[response.status_code]

    # test task without json data
    bad_task_2 = [
        ('id', len(test_data_tasks) + 1),
        ('description', 'Test task\'s description'),
        ('done', False)
    ]
    response = client.post('/todo/api/v1.0/tasks', json=bad_task_2)
    data = response.get_json()
    assert response.status_code == 400
    assert 'error' in data
    assert data['error'] == error_messages[response.status_code]


def test_get_tasks():
    """test getting all the tasks."""
    print(f'test_data_tasks = {test_data_tasks}')
    response = client.get('/todo/api/v1.0/tasks')
    data = response.get_json()
    assert response.status_code == 200
    assert 'tasks' in data
    assert data['tasks'] == test_data_tasks


def test_get_task():
    """test getting task by ID."""
    for task_id in (1, 2):
        response = client.get(f'/todo/api/v1.0/tasks/{task_id}')
        data = response.get_json()
        assert response.status_code == 200
        assert 'task' in data
        assert data['task'] == test_data_tasks[task_id - 1]

    # test non-existent task
    non_existent_task_id = 100
    response = client.get(f'/todo/api/v1.0/tasks/{non_existent_task_id}')
    data = response.get_json()
    assert response.status_code == 404
    assert 'error' in data
    assert data['error'] == error_messages[response.status_code]


def test_update_task():
    """Test updating tasks."""
    task_to_update = {
        'title': 'Updated title',
        'description': 'Updated items',
        'done': False
    }
    right_updated_task = {
        'id': 1,
        'title': 'Updated title',
        'description': 'Updated items',
        'done': False
    }
    response = client.put('/todo/api/v1.0/tasks/1', json=task_to_update)
    data = response.get_json()

    assert response.status_code == 200
    assert 'task' in data
    assert data['task'] == right_updated_task
    assert (right_updated_task ==
            client.get('/todo/api/v1.0/tasks/1').get_json()['task'])

    # test non-existent task
    task_id = 45
    response = client.put(f'/todo/api/v1.0/tasks/{task_id}',
                          json=task_to_update)
    data = response.get_json()

    assert response.status_code == 404
    assert 'error' in data
    assert data['error'] == error_messages[response.status_code]

    # test task with bad data
    bad_task = [
        'id', 3, 'description', 'Test', False
    ]
    response = client.put('/todo/api/v1.0/tasks/1', json=bad_task)
    data = response.get_json()

    assert response.status_code == 400
    assert 'error' in data
    assert data['error'] == error_messages[response.status_code]


def test_delete_task():
    """Test deleting tasks."""
    task_id = 1
    task_to_delete = test_data_tasks[0]
    response = client.delete(f'/todo/api/v1.0/tasks/{task_id}')
    data = response.get_json()

    assert response.status_code == 200
    assert 'result' in data
    assert data['result']
    assert task_to_delete not in test_data_tasks

    # test deleting non-existing task
    task_id = 300
    response = client.delete(f'/todo/api/v1.0/tasks/{task_id}')
    data = response.get_json()

    assert response.status_code == 404
    assert 'error' in data
    assert data['error'] == error_messages[response.status_code]
