from flask import Flask, render_template, request, url_for, redirect, session, flash
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime


app = Flask(__name__)
app.config['SECRET_KEY'] = '$asgC*a78njN!mw6'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///todo.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


class Task(db.Model):

    __tablename__ = 'tasks'
    
    id = db.Column(db.Integer(),primary_key=True)
    task = db.Column(db.Text)
    creation_time = db.Column(db.DateTime, nullable=False,default=datetime.utcnow)

    def __repr__(self):
        return f'<task: {self.task[0:20]}...>'



@app.route('/')
def index():
    return redirect(url_for('todo'))


@app.route('/todo', methods=['GET','POST'])
def todo():

    if request.method == 'POST':

        if request.form['text-area']:

            text_area = request.form['text-area']
            task = Task(task=text_area)

            db.session.add(task)
            db.session.commit()

            return redirect(url_for('todo'))
   
    tasks = Task.query.all()
    return render_template('to_do.html', tasks=tasks)


@app.route('/update/<id>', methods=['GET', 'POST'])
def update(id):

    print(id)
    if request.method == 'POST':
        text_area = request.form['text-area']

        update_task = Task.query.filter_by(id=id).first()
        update_task.task = text_area

        db.session.add(update_task)
        db.session.commit()

        flash (f'Tarefa {id} atualizada com sucesso', category='update')
        return(redirect(url_for('todo')))

    task = Task.query.filter_by(id=id).first()
    return render_template('update.html', task=task)


@app.route('/delete/<id>', methods=['GET','POST'])
def delete(id):
    
    delete_task = Task.query.filter_by(id=id).first()
    db.session.delete(delete_task)
    db.session.commit()

    flash (f'Tarefa {id} deletada com sucesso',category='delete')
    return redirect(url_for('todo'))

    
@app.route('/teste')
def teste():
    return render_template('teste.html')




if __name__ == "__main__":
    app.run(debug=True)