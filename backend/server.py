from flask import Flask, jsonify, request, render_template
from pymongo import MongoClient
from bson import ObjectId

app = Flask(__name__)
client = MongoClient('localhost', 27017)
db = client.flask_db
todos = db.todos

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/todos', methods=['GET'])
def get_todos():
    result = []
    for todo in todos.find():
        result.append({
            "_id": str(todo["_id"]),
            "task": todo.get("task", ""),
            "completed": todo.get("completed", False)
        })
    return jsonify(result)

@app.route('/todos', methods=['POST'])
def create_todo():
    new_todo = {
        "task": request.json.get("task", ""),
        "completed": request.json.get("completed", False)
    }
    result = todos.insert_one(new_todo)
    new_todo["_id"] = str(result.inserted_id)
    return jsonify(new_todo), 201





if __name__ == '__main__':
    app.run(debug=True)