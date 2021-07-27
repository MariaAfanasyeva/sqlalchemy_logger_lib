from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class Bot(Base):
    __tablename__ = "bot"
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)

    def __init__(self, name):
        self.name = name

    def __str__(self):
        return f"{self.name}"

    def __repr__(self):
        return self.__str__()
