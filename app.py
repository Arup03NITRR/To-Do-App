# Import necessary modules from Flask
from flask import Flask, render_template, url_for, request, redirect
from flask_sqlalchemy import SQLAlchemy
import os

# Initialize the Flask application
app = Flask(__name__)

# Configuring Database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Creating object for database
db = SQLAlchemy(app)

# Creating table Todo
class Todo(db.Model):
    task_id = db.Column(db.Integer, primary_key = True)
    task_name = db.Column(db.String(100))
    task_status = db.Column(db.Boolean)

# Define a route for the homepage
@app.route('/')
def homepage():
    todo_list = Todo.query.all()
    # Render the "index.html" template when this route is accessed
    return render_template("index.html", todo_list=todo_list)

# Defining method for adding
@app.route('/add', methods=["POST"])
def add():
    task = request.form.get("task-name")
    newTask = Todo(task_name = task, task_status = False)
    db.session.add(newTask)
    db.session.commit()
    return redirect(url_for("homepage"))

# Defining method for update
@app.route('/update/<int:todo_id>')
def update(todo_id):
    todo = Todo.query.get(todo_id)
    todo.task_status = not todo.task_status
    db.session.commit()
    return redirect(url_for("homepage"))

# Defining method for delete
@app.route('/delete/<int:todo_id>')
def delete(todo_id):
    todo = Todo.query.get(todo_id)
    db.session.delete(todo)
    db.session.commit()
    return redirect(url_for("homepage"))

# Run the application if this script is executed directly
if __name__ == "__main__":
    # Enable debug mode for easier development and debugging
    app.run(debug=True)
