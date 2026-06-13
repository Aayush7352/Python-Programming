"""
Flask web application demonstration.

Requires: pip install flask
"""
import sys


def main():
    """Flask demo showing a simple REST API."""
    try:
        from flask import Flask, jsonify, request, abort
    except ImportError:
        print("Flask is not installed.")
        print("Install with: pip install flask")
        print("\nThis file demonstrates Flask patterns.")
        print("Run this file to start the server.")
        sys.exit(1)

    app = Flask(__name__)

    # In-memory data store
    tasks = [
        {"id": 1, "title": "Learn Python", "done": False},
        {"id": 2, "title": "Build a project", "done": False},
        {"id": 3, "title": "Write tests", "done": False},
    ]
    next_id = 4

    @app.route("/")
    def index():
        return jsonify({
            "app": "Flask Todo API",
            "version": "1.0",
            "endpoints": {
                "GET /tasks": "List all tasks",
                "GET /tasks/<id>": "Get a task",
                "POST /tasks": "Create a task",
                "PUT /tasks/<id>": "Update a task",
                "DELETE /tasks/<id>": "Delete a task",
            }
        })

    @app.route("/tasks", methods=["GET"])
    def get_tasks():
        return jsonify({"tasks": tasks, "count": len(tasks)})

    @app.route("/tasks/<int:task_id>", methods=["GET"])
    def get_task(task_id: int):
        task = next((t for t in tasks if t["id"] == task_id), None)
        if task is None:
            abort(404, description=f"Task {task_id} not found")
        return jsonify({"task": task})

    @app.route("/tasks", methods=["POST"])
    def create_task():
        nonlocal next_id
        data = request.get_json()
        if not data or "title" not in data:
            abort(400, description="Title is required")

        task = {
            "id": next_id,
            "title": data["title"],
            "done": data.get("done", False),
        }
        tasks.append(task)
        next_id += 1
        return jsonify({"task": task, "message": "Task created"}), 201

    @app.route("/tasks/<int:task_id>", methods=["PUT"])
    def update_task(task_id: int):
        task = next((t for t in tasks if t["id"] == task_id), None)
        if task is None:
            abort(404, description=f"Task {task_id} not found")

        data = request.get_json()
        if "title" in data:
            task["title"] = data["title"]
        if "done" in data:
            task["done"] = data["done"]

        return jsonify({"task": task, "message": "Task updated"})

    @app.route("/tasks/<int:task_id>", methods=["DELETE"])
    def delete_task(task_id: int):
        task = next((t for t in tasks if t["id"] == task_id), None)
        if task is None:
            abort(404, description=f"Task {task_id} not found")
        tasks.remove(task)
        return jsonify({"message": "Task deleted", "id": task_id})

    @app.errorhandler(404)
    def not_found(error):
        return jsonify({"error": str(error)}), 404

    @app.errorhandler(400)
    def bad_request(error):
        return jsonify({"error": str(error)}), 400

    print("=== Flask Todo API Demo ===")
    print("  This file defines a Flask application.")
    print("  Run with: python 66_flask.py")
    print("  Or start the server programmatically:")

    # Start the server for testing
    print("\n  Starting Flask test server on http://127.0.0.1:5000")
    print("  Press Ctrl+C to stop\n")

    import threading
    server = threading.Thread(
        target=app.run,
        kwargs={"host": "127.0.0.1", "port": 5000, "debug": False},
        daemon=True
    )
    server.start()

    import time
    time.sleep(1)

    # Test the API
    import urllib.request
    import json

    try:
        # GET index
        response = urllib.request.urlopen("http://127.0.0.1:5000/")
        print(f"  GET /: {json.loads(response.read())}")

        # GET tasks
        response = urllib.request.urlopen("http://127.0.0.1:5000/tasks")
        print(f"  GET /tasks: {json.loads(response.read())}")

        print("\n  Server is running. Test with:")
        print("    curl http://127.0.0.1:5000/tasks")
        print("    curl http://127.0.0.1:5000/tasks/1")

    except Exception as e:
        print(f"  Test error: {e}")

    print("\n  (Server will stop when this script exits)")


if __name__ == "__main__":
    main()
