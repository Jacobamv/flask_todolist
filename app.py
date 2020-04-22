from flask import Flask, render_template, json, request, session, redirect, url_for
from config import Config
from peewee import *

app = Flask(__name__)
app.config.from_object(Config)
db = SqliteDatabase('tasks.db')

class Task(Model):
	id = IntegerField(primary_key=True)
	name = CharField()
	iscomplete = BooleanField(default=False)
	class Meta:
		database = db


@app.route('/')
def index():
	return render_template("index.html", tasks=Task.select())

@app.route('/add',methods=['GET', 'POST'])
def add():
	_name = request.form['name']
	task = Task(name=_name, iscomplete=False)
	task.save()
	return redirect('/')


@app.route('/changecomp/<id>')
def change(id):
	task = Task.get(Task.id == id)
	if task.iscomplete == True:
		task.iscomplete = False
	else:
		task.iscomplete=True
	task.save()
	return redirect('/', code=302)

@app.route('/delete/<id>')
def delete(id):
	task = Task.get(Task.id == id)
	task.delete_instance()
	return redirect('/', code = 302)