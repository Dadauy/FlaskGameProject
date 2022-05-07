from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired


class MoveForm(FlaskForm):
    """форма для хода"""
    here = StringField('откуда', validators=[DataRequired()])
    there = StringField('куда', validators=[DataRequired()])
    submit = SubmitField('Сходить')
