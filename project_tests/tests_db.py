import os
import sys
import unittest

sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))
from app.routes import app, connection_to_db

test_data = [
    {'id': 1, 'title': 'Test Task #1',
     'description': 'Test Description #1', 'done': False},
    {'id': 2, 'title': 'Test Task #2',
     'description': 'What?', 'done': False},
    {'id': 3, 'title': 'Test Task #3',
     'description': 'Already done', 'done': True}
]


class TestApp(unittest.TestCase):
    """Testing class."""

    def setUp(self):
        """ Setting up db and conn before each test method."""
        self.app = app.test_client()
        self.connection = connection_to_db()
        self.cursor = self.connection.cursor()
        self.cursor.execute(
            """CREATE TABLE IF NOT EXISTS tasks
                    (id INTEGER PRIMARY KEY AUTOINCREMENT,
                    title TEXT NOT NULL,
                    description TEXT,
                    done BOOLEAN DEFAULT 0)
            """
        )

    def fill_bd(self):
        """Fill the database by test data."""
        for task in test_data:
            self.app.post('/todo/api/v1.0/tasks', json=task)

    def tearDown(self):
        """Runs after each individual test method."""
        self.cursor.execute("DROP TABLE IF EXISTS tasks")
        self.connection.close()

    def test_create_task(self):
        """Test creating tasks."""

        self.fill_bd()

        test_task = {'title': 'Test Task #4',
                     'description': 'A new task', 'done': True}
        response = self.app.post('/todo/api/v1.0/tasks', json=test_task)
        data = response.get_json()['task']
        task = self.cursor.execute(
            "SELECT * FROM tasks ORDER BY id DESC").fetchone()
        task = {'id': task[0], 'title': task[1],
                'description': task[2], 'done': task[3]}

        self.assertEqual(response.status_code, 201)
        self.assertEqual(task['title'], data['title'])
        self.assertEqual(task['description'], data['description'])
        self.assertEqual(task['done'], data['done'])

        # test task without title
        bad_task_1 = {
            'id': 2,
            'description': 'Test task\'s description',
            'done': False
        }
        response = self.app.post('/todo/api/v1.0/tasks', json=bad_task_1)
        data = response.get_json()

        self.assertEqual(response.status_code, 400)
        self.assertIn('error', data)
        self.assertEqual(data['error'], 'Bad request')

        # test task without json data
        bad_task_2 = [
            ('description', 'Test task\'s description'),
            ('done', False)
        ]
        response = self.app.post('/todo/api/v1.0/tasks', json=bad_task_2)
        data = response.get_json()

        self.assertEqual(response.status_code, 400)
        self.assertIn('error', data)
        self.assertEqual(data['error'], 'Bad request')

    def test_get_tasks(self):
        """test getting all the tasks."""

        response = self.app.get('/todo/api/v1.0/tasks')
        data = response.get_json()

        self.assertEqual(response.status_code, 200)
        self.assertIn('empty', data)
        self.assertTrue(data['empty'])

        self.fill_bd()
        response = self.app.get('/todo/api/v1.0/tasks')
        data = response.get_json()

        self.assertEqual(response.status_code, 200)
        self.assertIn('tasks', data)
        self.assertEqual(data['tasks'], test_data)

    def test_get_task(self):
        """test getting task by ID."""

        self.fill_bd()
        for task_id in range(1, 4):
            response = self.app.get(f'/todo/api/v1.0/tasks/{task_id}')
            data = response.get_json()

            self.assertEqual(response.status_code, 200)
            self.assertIn('task', data)
            self.assertEqual(data['task'], test_data[task_id - 1])

        # test non-existent task
        non_existent_task_id = 100
        response = self.app.get(f'/todo/api/v1.0/tasks/{non_existent_task_id}')
        data = response.get_json()

        self.assertEqual(response.status_code, 404)
        self.assertIn('error', data)
        self.assertEqual(data['error'], 'Not found')

    def test_update_task(self):
        """Test updating tasks."""

        self.fill_bd()
        task_to_update = {
            'title': 'Updated title!',
        }
        right_updated_task = {
            'id': 2,
            'title': 'Updated title!',
            'description': 'What?',
            'done': False
        }
        response = self.app.put('/todo/api/v1.0/tasks/2', json=task_to_update)
        data = response.get_json()

        self.assertEqual(response.status_code, 200)
        self.assertIn('task', data)
        self.assertEqual(data['task'], right_updated_task)
        updated_task = self.app.get('/todo/api/v1.0/tasks/2') \
            .get_json()['task']
        self.assertEqual(updated_task, right_updated_task)

        # test non-existent task
        task_id = 45
        response = self.app.put(f'/todo/api/v1.0/tasks/{task_id}',
                                json=task_to_update)
        data = response.get_json()

        self.assertEqual(response.status_code, 404)
        self.assertIn('error', data)
        self.assertEqual(data['error'], 'Not found')

        # test task with bad data
        bad_task = [
            'id', 3, 'description', 'Test', False
        ]
        response = self.app.put('/todo/api/v1.0/tasks/1', json=bad_task)
        data = response.get_json()

        self.assertEqual(response.status_code, 400)
        self.assertIn('error', data)
        self.assertEqual(data['error'], 'Bad request')

    def test_delete_task(self):
        """Test deleting tasks."""

        self.fill_bd()
        task_to_delete = test_data[0]
        task_id = task_to_delete['id']
        response = self.app.delete(f'/todo/api/v1.0/tasks/{task_id}')
        data = response.get_json()

        self.assertEqual(response.status_code, 200)
        self.assertIn('result', data)
        self.assertTrue(data['result'])
        tasks = self.app.get('/todo/api/v1.0/tasks').get_json()['tasks']
        self.assertNotIn(task_to_delete, tasks)

        # test deleting non-existing task
        task_id = 300
        response = self.app.delete(f'/todo/api/v1.0/tasks/{task_id}')
        data = response.get_json()

        self.assertEqual(response.status_code, 404)
        self.assertIn('error', data)
        self.assertEqual(data['error'], 'Not found')


if __name__ == '__main__':
    unittest.main()
