from flask import Flask, jsonify, request, render_template, session,redirect,url_for
from pymongo import MongoClient
import os

app = Flask(
    __name__,
    template_folder="templates",
    static_folder="static"
)

# Secret key is required for using Flask sessions.
# Read from environment for production, fallback to a development key.
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'dev-secret')

mongo_uri = os.getenv('MONGO_URI', 'mongodb://root:pass@localhost:27017/prod-db?authSource=admin')
client = MongoClient(mongo_uri)
db = client['prod-db']
todos = db.todos
users = db.users






@app.route('/')
def login_page():
    return render_template('login.html')



@app.route('/signup', methods=['GET'])
def signup_page():
    return render_template('signup.html')


@app.route('/login', methods=['GET'])
def login_page_get():
    return render_template('login.html')

@app.route('/login', methods=['POST'])
def login():
    email = request.form.get('email')
    password = request.form.get('password')

    user = users.find_one({"email": email, "password": password})
    if user:
        
        user_password = user["password"]

        if user_password == password:
            session['email'] = email
            return render_template('index.html')
        else:
            return render_template('login.html', error="Invalid password")
    else:
        return render_template('login.html', error="User not found")

@app.route('/signup', methods=['POST'])
def signup():
    email = request.form.get('email')
    password = request.form.get('password')

    existing_user = users.find_one({"email": email})
    if existing_user:
        return render_template('signup.html', error="User already exists")

    users.insert_one({"email": email, "password": password})
    return render_template('index.html')


@app.route('/todos', methods=['GET'])
def get_todos():
    result = []
    email = session.get("email")
    todoss = todos.find({"email": email})
    for todo in todoss:
        result.append({
            "_id": str(todo["_id"]),
            "task": todo.get("task", ""),
            "completed": todo.get("completed", False)
        })
    return jsonify(result)

@app.route('/todos', methods=['POST'])
def create_todo():
    new_todo = {
        "email": session.get("email"),
        "task": request.json.get("task", ""),
        "completed": False
    }
    result = todos.insert_one(new_todo)
    new_todo["_id"] = str(result.inserted_id)
    return jsonify(new_todo), 201

@app.route('/todos/<task_name>', methods=['DELETE'])
def delete_todo(task_name):
    myquery = {"task": task_name}
    todos.delete_one(myquery)
    return jsonify({"message": "Todo deleted"}), 200

@app.route('/todos/<task_name>', methods=['PUT'])
def update_todo(task_name):
    updated_task = request.get_json()
    new_boolean = updated_task.get("completed", False)

    result = todos.update_one(
        {"task": task_name},
        {"$set": {"completed": new_boolean}}
    )

    if result.modified_count > 0:
        return jsonify({"message": "Todo updated successfully"}), 200
    else:
        return jsonify({"message": "Todo not found"}), 404

if __name__ == '__main__':
    app.run(host='0.0.0.0')