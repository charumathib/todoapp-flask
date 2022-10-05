import os
from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

# create local sqlite database
PROJECT_ROOT = os.path.dirname(os.path.realpath(__file__))
DATABASE = os.path.join(PROJECT_ROOT, 'todo.db')

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:////" + DATABASE
db = SQLAlchemy(app)

# schema for todo item
class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(80))
    complete = db.Column(db.Boolean)

# homepage of the app shows index.html
@app.route("/")
def index():
    todo_list = Todo.query.all()
    return render_template("index.html", todo_list=todo_list)

# endpoint to add a todo
@app.route("/add", methods=["POST"])
def add():
    # get input value from form
    title = request.form.get("title")
    # create a new todo object with the title from above
    new_todo = Todo(title=title, complete=False)
    # add the todo to database and commit the transaction
    db.session.add(new_todo)
    db.session.commit()
    # redirect to homepage
    return redirect(url_for("index"))

# endpoint to mark a todo complete
@app.route("/complete/<string:todo_id>")
def complete(todo_id):
    # get the todo that we want to mark complete by filtering bt its id
    todo = Todo.query.filter_by(id=todo_id).first()
    # toggle complete status
    todo.complete = not todo.complete
    # save changes by committing transaction
    db.session.commit()
    # redirect to homepage
    return redirect(url_for("index"))

# endpoint to delete a todo
@app.route("/delete/<string:todo_id>")
def delete(todo_id):
    # get the todo that we want to mark complete by filtering bt its id
    todo = Todo.query.filter_by(id=todo_id).first()
    # delete the todo
    db.session.delete(todo)
    # save changes by committing transaction
    db.session.commit()
    # redirect to homepage
    return redirect(url_for("index"))


if __name__ == "__main__":
    # create database
    db.create_all()
    # run code
    app.run(debug=True)
