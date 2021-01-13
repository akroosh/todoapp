from app import app, db
from flask import render_template, request, redirect, url_for
from models import Task, Desk
from datetime import datetime
from sqlalchemy import asc, desc


@app.route('/', methods=["GET"])
def homepage():
    desk_list = Desk.query.all()
    return render_template("home.html", desk_list=desk_list)


@app.route('/create_desk', methods=["POST", "GET"])
def create_desk():
    title = request.form.get("title")
    if title:
        publish_date = datetime.now()
        new_desk = Desk(title=title, publish_date=publish_date)
        db.session.add(new_desk)
        db.session.commit()
        return redirect('/')
    return render_template('create.html', is_desk = True)


@app.route('/desk/<string:desk_title>/create_task', methods=["POST", "GET"])
def create_task(desk_title):
    desk = Desk.query.filter_by(title=desk_title).first()
    title = request.form.get("title")
    description = request.form.get("description")
    if title:
        publish_date = datetime.now()
        status = bool(request.form.get("status"))
        desk_id = desk.id
        new_task = Task(title=title, description = description, publish_date=publish_date, desk_id=desk_id, status=status)
        db.session.add(new_task)
        desk.tasks.append(new_task)
        db.session.commit()
        return redirect('/')
    return render_template('create.html', is_desk = False, desk=desk)


@app.route('/update_desk/<int:id>', methods=['GET', 'POST'])
def update_desk(id):
    desk = Desk.query.filter_by(id=id).first()
    if request.method == 'POST':
        desk.title = request.form.get('title')
        desk.changed_date = datetime.now()
        try:
            db.session.commit()
            return redirect('/')
        except:
            return "There was a problem updating data."

    else:
       title = "Update Desk"
       return render_template('update.html', title=title, desk=desk, is_desk = True)


@app.route('/update_task/<int:id>', methods=['GET', 'POST'])
def update_task(id):
    task = Task.query.filter_by(id=id).first()
    if request.method == 'POST':
        task.title = request.form.get('title', default="task.title")
        task.description = request.form.get("description", default="task.description")
        task.status = bool(request.form.get("status"))
        task.changed_date = datetime.now()

        try:
            db.session.commit()
            return redirect('/')
        except:
            return "There was a problem updating data."

    else:
       title = "Update Desk"
       return render_template('update.html', title=title, task = task, is_desk = False)


@app.route('/delete_desk/<int:id>', methods=["GET", "POST"])
def delete_desk(id):
    desk = Desk.query.filter_by(id=id).first()
    db.session.delete(desk)
    db.session.commit()
    return redirect(url_for('homepage'))

@app.route('/delete_task/<int:id>', methods=["GET", "POST"])
def delete_task(id):
    task = Task.query.filter_by(id=id).first()
    db.session.delete(task)
    db.session.commit()
    return redirect(url_for('homepage'))

@app.route('/desk/<string:title>')
def desk_detail(title):
    desk = Desk.query.filter_by(title=title).first()
    tasks = Task.query.filter_by(desk_id = desk.id).order_by(asc('title'))
    tasks1 = Task.query.filter_by(desk_id = desk.id).order_by(desc('title'))
    return render_template('desk_detail.html', desk=desk, tasks=tasks, tasks1=tasks1)

@app.route('/task/<string:title>')
def task_detail(title):
    task = Task.query.filter_by(title=title).first()
    return render_template('task_detail.html', task=task)