from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# Configure database connection (replace with your details)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///todos.db'
db = SQLAlchemy(app)

# Define Todo and Subtask models


class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(80), nullable=False)
    isComplete = db.Column(db.Boolean, default=False)
    subtasks = db.relationship('Subtask', backref='todo', lazy='dynamic')


class Subtask(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    parentId = db.Column(db.Integer, db.ForeignKey('todo.id'))
    title = db.Column(db.String(80), nullable=False)
    isCompleted = db.Column(db.Boolean, default=False)

# Create database tables (run once)


@app.before_first_request
def create_tables():
    db.create_all()

# Get all todos


@app.route('/todos', methods=['GET'])
def get_todos():
    todos = Todo.query.all()
    return jsonify([todo.serialize() for todo in todos])

# Get a specific todo by ID


@app.route('/todos/<int:todo_id>', methods=['GET'])
def get_todo(todo_id):
    todo = Todo.query.get(todo_id)
    if todo is None:
        return jsonify({'error': 'Todo not found'}), 404
    return jsonify(todo.serialize())

# Create a new todo


@app.route('/todos', methods=['POST'])
def create_todo():
    data = request.get_json()
    if not data or not data.get('title'):
        return jsonify({'error': 'Missing required fields'}), 400
    new_todo = Todo(title=data['title'],
                    isComplete=data.get('isComplete', False))
    subtasks = data.get('subtasks', [])
    for subtask in subtasks:
        new_subtask = Subtask(
            parentId=new_todo.id, title=subtask['title'], isCompleted=subtask.get('isCompleted', False))
        new_todo.subtasks.append(new_subtask)
    db.session.add(new_todo)
    db.session.commit()
    return jsonify(new_todo.serialize()), 201

# Update a todo


@app.route('/todos/<int:todo_id>', methods=['PUT'])
def update_todo(todo_id):
    data = request.get_json()
    if not data:
        return jsonify({'error': 'Missing data'}), 400
    todo = Todo.query.get(todo_id)
    if todo is None:
        return jsonify({'error': 'Todo not found'}), 404
    todo.title = data.get('title', todo.title)
    todo.isComplete = data.get('isComplete', todo.isComplete)
    db.session.add(todo)
    db.session.commit()
    return jsonify(todo.serialize())

# Delete a todo


@app.route('/todos/<int:todo_id>', methods=['DELETE'])
def delete_todo(todo_id):
    todo = Todo.query.get(todo_id)
    if todo is None:
        return jsonify({'error': 'Todo not found'}), 404
    db.session.delete(todo)
    db.session.commit()
    return jsonify({'message': 'Todo deleted'})

# Helper method to serialize todo objects


def serialize_todo(todo):
    return {
        'id': todo.id,
        'title': todo.title,
        'isComplete': todo.isComplete,
        'subtasks': [serialize_subtask(subtask) for subtask in todo.subtasks]
    }

# Helper method to serialize subtask objects


def serialize_subtask(subtask):
    return {
        'id': subtask.id,
        'parentId': subtask.parentId,
        'title': subtask.title,
        'isCompleted': subtask.isCompleted
    }
