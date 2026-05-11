from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
from flask_socketio import SocketIO
from config import Config
from datetime import datetime

app = Flask(__name__)
app.config.from_object(Config)

db = SQLAlchemy(app)
socketio = SocketIO(app)

login_manager = LoginManager()
login_manager.init_app(app)

# USER MODEL
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100))
    email = db.Column(db.String(100))
    password = db.Column(db.String(100))

# TASK MODEL
class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200))
    description = db.Column(db.String(500))
    priority = db.Column(db.String(50))
    status = db.Column(db.String(50))
    created_date = db.Column(db.DateTime, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# HOME
@app.route('/')
def home():
    return redirect('/login')

# REGISTER
@app.route('/register', methods=['GET', 'POST'])
def register():

    if request.method == 'POST':

        user = User(
            username=request.form['username'],
            email=request.form['email'],
            password=request.form['password']
        )

        db.session.add(user)
        db.session.commit()

        return redirect('/login')

    return render_template('register.html')

# LOGIN
@app.route('/login', methods=['GET', 'POST'])
def login():

    if request.method == 'POST':

        user = User.query.filter_by(
            email=request.form['email'],
            password=request.form['password']
        ).first()

        if user:
            login_user(user)
            return redirect('/dashboard')

    return render_template('login.html')

# LOGOUT
@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect('/login')

# DASHBOARD
@app.route('/dashboard')
@login_required
def dashboard():

    tasks = Task.query.filter_by(user_id=current_user.id).all()

    total_tasks = len(tasks)

    completed_tasks = len(
        [task for task in tasks if task.status == 'Completed']
    )

    pending_tasks = total_tasks - completed_tasks

    completion_percentage = 0

    if total_tasks > 0:
        completion_percentage = round(
            (completed_tasks / total_tasks) * 100, 2
        )

    return render_template(
        'dashboard.html',
        tasks=tasks,
        total_tasks=total_tasks,
        completed_tasks=completed_tasks,
        pending_tasks=pending_tasks,
        completion_percentage=completion_percentage
    )

# ADD TASK
@app.route('/add-task', methods=['POST'])
@login_required
def add_task():

    task = Task(
        title=request.form['title'],
        description=request.form['description'],
        priority=request.form['priority'],
        status=request.form['status'],
        user_id=current_user.id
    )

    db.session.add(task)
    db.session.commit()

    socketio.emit('task_update', {
        'message': 'New Task Added'
    })

    return redirect('/dashboard')
    # UPDATE TASK
@app.route('/update-task/<int:id>', methods=['GET', 'POST'])
@login_required
def update_task(id):

    task = Task.query.get(id)

    if request.method == 'POST':

        task.title = request.form['title']
        task.description = request.form['description']
        task.priority = request.form['priority']
        task.status = request.form['status']

        db.session.commit()

        return redirect('/dashboard')

    return render_template('update_task.html', task=task)

# DELETE TASK
@app.route('/delete-task/<int:id>')
@login_required
def delete_task(id):

    task = Task.query.get(id)

    db.session.delete(task)
    db.session.commit()

    return redirect('/dashboard')

if __name__ == '__main__':

    with app.app_context():
        db.create_all()

socketio.run(app, host="0.0.0.0", port=5000, debug=True)