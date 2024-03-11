from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, DateTimeField, EmailField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired


class JobForm(FlaskForm):
    team_leader = IntegerField('Лидер', validators=[DataRequired()])
    job = StringField('Работа', validators=[DataRequired()])
    work_size = IntegerField('Время', validators=[DataRequired()])
    collaborators = StringField('Коллаборация', validators=[DataRequired()])
    is_finished = BooleanField('Выполнено?')
    submit = SubmitField('Отправить')
