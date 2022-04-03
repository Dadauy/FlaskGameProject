import sqlalchemy

from .db_session import SqlAlchemyBase


class Game(SqlAlchemyBase):
    __tablename__ = 'games'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    uuid = sqlalchemy.Column(sqlalchemy.String(), nullable=True)
    first_name = sqlalchemy.Column(sqlalchemy.String(), nullable=True)
    second_name = sqlalchemy.Column(sqlalchemy.String(), nullable=True)

    state = sqlalchemy.Column(sqlalchemy.Boolean, nullable=True)
    doska = sqlalchemy.Column(sqlalchemy.String(), nullable=True)
    move = sqlalchemy.Column(sqlalchemy.Boolean, nullable=True)
