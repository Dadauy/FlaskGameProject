import datetime
import sqlalchemy
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

from .db_session import SqlAlchemyBase


class User(SqlAlchemyBase, UserMixin):
    """таблица БД для пользователя"""
    __tablename__ = 'users'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)  # id пользователя
    name = sqlalchemy.Column(sqlalchemy.String(), nullable=True)  # ник пользователя
    hashed_password = sqlalchemy.Column(sqlalchemy.String(), nullable=True)  # хэшированый пароль
    created_date = sqlalchemy.Column(sqlalchemy.DateTime, default=datetime.datetime.now)  # дата создания

    def set_password(self, password):
        """хэширование пароля"""
        self.hashed_password = generate_password_hash(password)

    def check_password(self, password):
        """шифрование пароля"""
        return check_password_hash(self.hashed_password, password)
