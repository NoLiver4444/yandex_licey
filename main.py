from flask import Flask, redirect, render_template, request, make_response, session
from data import db_session
from flask_login import LoginManager, current_user, login_user, login_required, logout_user
from data.users import User
from data.jobs import Jobs
import datetime
from forms.LoginForm import LoginForm
from forms.JobForm import JobForm
from forms.RegistForm import RegistForm

app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'
app.config['PERMANENT_SESSION_LIFETIME'] = datetime.timedelta(
    days=365)
login_manager = LoginManager()
login_manager.init_app(app)

db_session.global_init("db/mars_explorer.db")


@app.route("/")
def index():
    db_sess = db_session.create_session()
    jobs = db_sess.query(Jobs).all()
    return render_template("jobs.html", jobs=jobs)


@login_manager.user_loader
def load_user(user_id):
    db_sess = db_session.create_session()
    return db_sess.query(User).get(user_id)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        user = db_sess.query(User).filter(User.email == form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            return redirect("/")
        return render_template('login.html',
                               message="Неправильный логин или пароль",
                               form=form)
    return render_template('login.html', title='Авторизация', form=form)


@app.route("/job", methods=['GET', 'POST'])
@login_required
def job():
    form = JobForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        jobs = Jobs()
        jobs.team_leader = form.team_leader.data
        jobs.job = form.job.data
        jobs.work_size = form.work_size.data
        jobs.collaborators = form.collaborators.data
        jobs.start_date = datetime.datetime.now()
        jobs.is_finished = form.is_finished.data
        db_sess.add(jobs)
        db_sess.commit()
        return redirect('/')
    return render_template('job.html', title='Работа', form=form)


@app.route("/register", methods=['GET', 'POST'])
def register():
    form = RegistForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        user = User()
        user.surname = form.surname.data
        user.name = form.name.data
        user.age = form.age.data
        user.position = form.position.data
        user.speciality = form.speciality.data
        user.address = form.address.data
        user.email = form.email.data
        user.hashed_password = form.password.data
        db_sess.add(user)
        db_sess.commit()
        login_user(user, remember=form.remember_me.data)
        return redirect('/')
    return render_template('regist.html', title='Регистрация', form=form)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect("/")


if __name__ == '__main__':
    app.run()
