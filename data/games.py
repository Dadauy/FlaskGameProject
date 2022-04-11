import sqlalchemy

from .db_session import SqlAlchemyBase


class Game(SqlAlchemyBase):
    __tablename__ = 'games'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)  # id игры
    uuid = sqlalchemy.Column(sqlalchemy.String(), nullable=True)  # uuid игры
    first_name = sqlalchemy.Column(sqlalchemy.String(), nullable=True)  # имя первого игрока(кто создал игру)
    second_name = sqlalchemy.Column(sqlalchemy.String(), nullable=True)  # имя второго игрока(перешедшего по ссылке)

    state = sqlalchemy.Column(sqlalchemy.Boolean, nullable=True)  # кто выиграл, кто проиграл
    doska = sqlalchemy.Column(sqlalchemy.String(), nullable=True)  # как расположенны фигуры
    move = sqlalchemy.Column(sqlalchemy.Boolean, nullable=True)  # чей сейчас ход
