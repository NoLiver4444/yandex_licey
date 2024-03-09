from flask import Flask, render_template
from data import db_session
from data.users import User
from data.jobs import Jobs
import datetime
import sys

app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'


@app.route("/")
def index():
    db_session.global_init("db/mars_explorer.db")
    db_sess = db_session.create_session()
    jobs = db_sess.query(Jobs).all()
    return render_template("job.html", jobs=jobs)


if __name__ == '__main__':
    app.run()
