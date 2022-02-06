from flask import Flask, render_template, url_for, request
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

from werkzeug.utils import redirect

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///test.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)


class Todo(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    completed = db.Column(db.Integer, default=0)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)
    date = db.Column(db.DateTime, default=datetime.utcnow)
    username = db.Column(db.String, default="mgreco")
    issue = db.Column(db.Integer)
    spent = db.Column(db.Float, default=8)
    burnt = db.Column(db.Float, default=8)
    description = db.Column(db.String(200), nullable=False)

    def __repr__(self):
        return '<Task %r>' % self.issue


def form2task(form, task):
    task.date = datetime.strptime(form['date'], "%Y-%m-%d")
    task.username = form['username']
    task.issue = int(form['issue'])
    task.spent = float(form['spent'])
    task.burnt = float(form['burnt'])
    task.description = form['description']
    return task



@app.route('/', methods=['POST', 'GET'])
def index(db=db):
    if request.method == "POST":
        new_task = form2task(request.form, Todo())

        try:
            db.session.add(new_task)
            db.session.commit()
            return redirect('/')
        except Exception:
            return "There was an error adding your task."

    else:
        tasks = Todo.query.order_by(Todo.date).all()
        today = datetime.utcnow()
        return render_template('index.html', tasks=tasks, today=today)


@app.route("/delete/<int:id>")
def delete(id, db=db):

    task_to_delete = Todo.query.get_or_404(id)

    try:
        db.session.delete(task_to_delete)
        db.session.commit()
        return redirect("/")
    except Exception:
        return "Something was wrong!"


@app.route("/update/<int:id>", methods=['GET', 'POST'])
def update(id, db=db):
    task = Todo.query.get_or_404(id)

    if request.method == "POST":
        task = form2task(request.form, task)
        try:
            db.session.commit()
            return redirect('/')
        except Exception:
            return "There was an issue updating your task."
    else:
        return render_template('update.html', task=task)


if __name__ == "__main__":
    app.run(debug=True)
