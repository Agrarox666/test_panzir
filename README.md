# It's a test code for scientific research company "Panzir".

## Todo API Documentation
## Contents
- [Introduction](#introduction)
- [Endpoints](#endpoints)
- [Installation](#installation)
- [Makefile](#makefile)
- [Authentication](#authentication)
- [Error Handling](#error-handling)

## Introduction
Welcome to the Todo API documentation. This API allows you to manage tasks in a simple todo list. It provides endpoints for creating, retrieving, updating, and deleting tasks.

## Endpoints
1. Create a task.
-   **Endpoint:** `/todo/api/v1.0/tasks`
-   **Method:** `POST`
-   **Description:** Create a new task with the provided data.
-   **Request Format:**
```json
{
  "title": "Task Title",
  "description": "Task Description",
  "done": false
}
```
-    **Response Format:**
```json 
{
  "task": {
    "id": 1,
    "title": "Task Title",
    "description": "Task Description",
    "done": false
  }
}
```
-   **Status Codes:**
    -   `201 Created`: Task successfully created.
    -   `400 Bad Request`: Invalid request format.

2. Get all the tasks.
-   **Endpoint:** `/todo/api/v1.0/tasks`
-   **Method:** `GET`
-   **Description:** Retrieve a list of all tasks.
-   **Response Format:**
```json
{
  "tasks": [
    {
      "id": ...,
      "title": ...,
      "description": ...,
      "done": ...
    },
    // Other tasks...
  ]
}
```
-   **Status Codes:**
     -   `200 OK`: Tasks successfully retrieved or got response with `{'empty': True}`.
    
3. Get specific task by its ID.
-   **Endpoint:** `/todo/api/v1.0/tasks/<int:task_id>`
-   **Method:** `GET`
-   **Description:** Retrieve details of a specific task.
-   **Response Format:**
```json
{
  "task": {
    "id": 1,
    "title": "Task Title",
    "description": "Task Description",
    "done": false
}
```
- Status Codes:
     -   `200 OK`: Task details successfully retrieved.
     -   `404 Not Found`: Task not found.
  
4. Update a task.
-   **Endpoint:** `/todo/api/v1.0/tasks/<int:task_id>`
-   **Method:** `PUT`
-   **Description:** Update the details of a specific task.
-   **Request Format:**
```json
{
  "title": "Updated Task Title",
  "description": "Updated Task Description",
  "done": true
}
```
-   **Response Format:**
```json
{
  "task": {
    "id": 1,
    "title": "Updated Task Title",
    "description": "Updated Task Description",
    "done": true
  }
}
```
- Status Codes:
     -   `200 OK`: Task successfully updated.
     -   `400 Bad Request`: Invalid request format.
     -   `404 Not Found`: Task not found.
5. Delete a task.
-   **Endpoint:** `/todo/api/v1.0/tasks/<int:task_id>`
-   **Method:** `DELETE`
-   **Description:** Delete a specific task.
-   **Response Format:**
```json
{
  "result": true
}
```
- Status Codes:
     -   `200 OK`: Task successfully deleted.
     -   `404 Not Found`: Task not found.
## Installation
```bash
	1. Clone the repository to your computer:
	git clone git@github.com:Agrarox666/test_panzir.git
	2. Install dependencies:
	make install
	3. Ready to use! You may use all of Make commands.
``` 
## Makefile
```bash
1. make lint #runs flake8 
2. make tests_no_db # runs tests for first version of API (wording on Python list, not database)
3. make tests_db # runs tests for second version of API with database
4. make run_no_db # runs development server (first version)
5. make run # runs development server (second version)
```
## Authentication

This API does not currently require authentication.

## Error Handling
In case of an error, the API will respond with a JSON object containing an "error" field describing the issue.

Example:
```json
{ "error": "Task not found" }
```
