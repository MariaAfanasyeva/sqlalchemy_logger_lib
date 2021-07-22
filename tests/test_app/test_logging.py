import logging

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy_logger.logger import Logger

from .models import Bot, Base


def make_engine():
    engine = create_engine("postgresql://postgres:root@localhost:5432/test_lib")
    Session = sessionmaker(bind=engine)
    session = Session()
    Base.metadata.create_all(engine)
    return session


def create_bot():
    session = make_engine()
    logger = Logger()
    logger.listen_after_flush()
    logger.listen_before_flush()
    logger.listen_after_rollback()
    session.add(Bot('Gachi'))
    last_bot = session.query(Bot).order_by(Bot.id.desc()).first()
    last_bot_id = last_bot.id
    session.commit()
    session.close()
    return last_bot_id


def test_create_bot(caplog):
    caplog.set_level(logging.INFO)
    bot = create_bot()
    assert f'INFO     sqlalchemy_logger.logger:logger.py:9 User with id=None has started creating model bot ' \
                   f'(raw ID=None)' in caplog.text
    assert f'INFO     sqlalchemy_logger.logger:logger.py:15 User with id=None has finished creating model bot ' \
               f'(raw ID={bot})' in caplog.text


def update_bot():
    session = make_engine()
    logger = Logger()
    logger.listen_after_flush()
    logger.listen_before_flush()
    logger.listen_after_rollback()
    bot = session.query(Bot).get(1)
    bot.name = "Android"
    session.commit()
    session.close()


def test_update_bot(caplog):
    caplog.set_level(logging.INFO)
    update_bot()
    assert f'INFO     sqlalchemy_logger.logger:logger.py:9 User with id=None has started updating model bot ' \
                   f'(raw ID=1)' in caplog.text
    assert f'INFO     sqlalchemy_logger.logger:logger.py:15 User with id=None has finished updating model bot ' \
               f'(raw ID=1)' in caplog.text


def delete_bot():
    session = make_engine()
    logger = Logger()
    logger.listen_after_flush()
    logger.listen_before_flush()
    logger.listen_after_rollback()
    last_bot = session.query(Bot).order_by(Bot.id.desc()).first()
    last_bot_id = last_bot.id
    session.delete(last_bot)
    session.commit()
    session.close()
    return last_bot_id


def test_delete_bot(caplog):
    caplog.set_level(logging.INFO)
    bot_id = delete_bot()
    assert f'INFO     sqlalchemy_logger.logger:logger.py:9 User with id=None has started deleting model bot ' \
                   f'(raw ID={bot_id})' in caplog.text
    assert f'INFO     sqlalchemy_logger.logger:logger.py:15 User with id=None has finished deleting model bot ' \
               f'(raw ID={bot_id})' in caplog.text


def create_update_delete_bot():
    session = make_engine()
    logger = Logger()
    logger.listen_after_flush()
    logger.listen_before_flush()
    logger.listen_after_rollback()
    session.add(Bot('Harry Potter'))
    last_bot = session.query(Bot).order_by(Bot.id.desc()).first()
    bot_to_update = session.query(Bot).get(3)
    last_bot_id = last_bot.id
    bot_to_update.name = 'Ronald Weasley'
    session.delete(last_bot)
    session.commit()
    session.close()
    return last_bot_id


def test_create_update_delete_bot(caplog):
    caplog.set_level(logging.INFO)
    bot_id = create_update_delete_bot()
    assert f'INFO     sqlalchemy_logger.logger:logger.py:9 User with id=None has started creating model bot ' \
                   f'(raw ID=None)' in caplog.text
    assert f'INFO     sqlalchemy_logger.logger:logger.py:15 User with id=None has finished creating model bot ' \
               f'(raw ID={bot_id})' in caplog.text
    assert f'INFO     sqlalchemy_logger.logger:logger.py:9 User with id=None has started updating model bot ' \
                   f'(raw ID=3)' in caplog.text
    assert f'INFO     sqlalchemy_logger.logger:logger.py:15 User with id=None has finished updating model bot ' \
               f'(raw ID=3)' in caplog.text
    assert f'INFO     sqlalchemy_logger.logger:logger.py:9 User with id=None has started deleting model bot ' \
                   f'(raw ID={bot_id})' in caplog.text
    assert f'INFO     sqlalchemy_logger.logger:logger.py:15 User with id=None has finished deleting model bot ' \
               f'(raw ID={bot_id})' in caplog.text