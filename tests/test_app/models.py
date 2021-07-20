from .testing_app import db, app
from sqlalchemy_logger.logger import Logger


class User(db.Model):
    __tablename__ = "user"
    id = db.Column(db.Integer, primary_key=True)
    password = db.Column(db.String(100), nullable=False)
    username = db.Column(db.String(100), nullable=False, unique=True)

    def __str__(self):
        return f"{self.username}"

    def __repr__(self):
        return self.__str__()


class Bot(db.Model):
    __tablename__ = "bot"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)

    def __str__(self):
        return f"{self.name}"

    def __repr__(self):
        return self.__str__()

logger = Logger(app)
logger.listen_after_flush()
logger.listen_before_flush()
logger.listen_after_rollback()
