import sqlite3

from app.models import Task


def create_table(conn):
    """Create task table."""

    curs = conn.cursor()
    try:
        curs.execute("SELECT * FROM tasks")
    except sqlite3.OperationalError:
        curs.executescript(
            """
            CREATE TABLE tasks (
                id INTEGER PRIMARY KEY,
                title TEXT NOT NULL,
                description TEXT,
                done BOOLEAN NOT NULL);
            INSERT INTO tasks (title, description, done) VALUES
            ('Buy groceries', 'Milk, Cheese, Pizza, Fruit, Tylenol', False),
            ('Learn Python', 'Need to find a good Python tutorial on the web',
            False);
            """
        )
        conn.commit()
        conn.close()


def sql_to_task(data):
    """Return Task object from database response."""

    return Task(id=data[0],
                title=data[1],
                description=data[2],
                done=data[3])


def create_task(new_task, conn):
    """Create a new task and add it to db."""

    curs = conn.cursor()
    curs.execute("""
    INSERT INTO tasks (title, description, done) VALUES (?, ?, ?)
    """, (new_task['title'], new_task['description'], new_task['done']))
    conn.commit()
    task_id = curs.lastrowid
    created_task = get_task(task_id, conn)
    conn.close()

    return created_task


def get_tasks(conn):
    """Get all the tasks from db."""

    curs = conn.cursor()
    curs.execute("SELECT * FROM tasks;")
    tasks_data = curs.fetchall()
    conn.close()

    tasks = list(map(sql_to_task, tasks_data))
    return tasks


def get_task(task_id, conn):
    """Get a specific task by its ID from db."""

    curs = conn.cursor()
    curs.execute("SELECT * from tasks WHERE id=?", (task_id,))
    task_data = curs.fetchone()
    conn.close()

    if task_data:
        return sql_to_task(task_data)
    else:
        return None


def update_task(task_id, updated_data, conn):
    """Update a specific task by its ID in the database."""

    curs = conn.cursor()
    params = []
    for key in updated_data:
        params.append(f'{key}=?')

    # build a query based on the number of parameters
    query = f"UPDATE tasks SET {', '.join(params)} WHERE id=?"
    curs.execute(
        query,
        (*tuple(updated_data.values()),
         task_id)
    )
    conn.commit()
    return get_task(task_id, conn)


def delete_task(task_id, conn):
    """Delete a specific task from db."""

    curs = conn.cursor()
    curs.execute("DELETE FROM tasks WHERE id=?", (task_id,))
    conn.commit()
    conn.close()
