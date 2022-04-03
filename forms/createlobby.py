from flask_wtf import FlaskForm
from wtforms import SubmitField


class CreateLobby(FlaskForm):
    submit = SubmitField('Создать игру')
