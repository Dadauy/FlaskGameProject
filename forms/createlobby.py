from flask_wtf import FlaskForm
from wtforms import SubmitField


class CreateLobby(FlaskForm):
    """форма для создания игры"""
    submit = SubmitField('Создать игру')
