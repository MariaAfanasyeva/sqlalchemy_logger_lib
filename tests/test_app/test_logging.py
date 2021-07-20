import json

import pytest
import logging

from tests.test_app.testing_app import app, db
from tests.test_app.models import Bot


@pytest.fixture
def client():
    app.config["TESTING"] = True
    with app.app_context():
        with app.test_client() as client:
            yield client


def test_create_function(client, caplog):
    response = client.post('/bot', data=json.dumps(dict(name="Harry Potter")), content_type='application/json')
    last_bot = Bot.query.order_by(Bot.id.desc()).first()
    caplog.set_level(logging.INFO)
    db.engine.execute(f"DELETE FROM bot WHERE id={last_bot.id}")
    assert f'INFO     tests.test_app.testing_app:logger.py:6 User with id=None has started creating model bot ' \
           f'(raw ID=None)' in caplog.text
    assert f'INFO     tests.test_app.testing_app:logger.py:12 User with id=None has finished creating model bot ' \
           f'(raw ID={last_bot.id})' in caplog.text
    assert response.status_code == 201


def test_delete_function(client, caplog):
    db.engine.execute("INSERT INTO bot VALUES (30, 'WandaVision')")
    last_bot = Bot.query.order_by(Bot.id.desc()).first()
    response = client.delete(f'/bot/{last_bot.id}')
    caplog.set_level(logging.INFO)
    assert f'INFO     tests.test_app.testing_app:logger.py:6 User with id=None has started deleting model bot ' \
           f'(raw ID={last_bot.id})' in caplog.text
    assert f'INFO     tests.test_app.testing_app:logger.py:12 User with id=None has finished deleting model bot ' \
           f'(raw ID={last_bot.id})' in caplog.text
    assert response.status_code == 204


def test_update_function(client, caplog):
    db.engine.execute("INSERT INTO bot VALUES (30, 'WandaVision')")
    last_bot = Bot.query.order_by(Bot.id.desc()).first()
    response = client.put(f'/bot/{last_bot.id}', data=json.dumps(dict(name="Harry Potter")),
                          content_type='application/json')
    caplog.set_level(logging.INFO)
    db.engine.execute(f"DELETE FROM bot WHERE id={last_bot.id}")
    assert f'INFO     tests.test_app.testing_app:logger.py:6 User with id=None has started updating model bot ' \
           f'(raw ID={last_bot.id})' in caplog.text
    assert f'INFO     tests.test_app.testing_app:logger.py:12 User with id=None has finished updating model bot ' \
           f'(raw ID={last_bot.id})' in caplog.text
    assert last_bot.name == "Harry Potter"


def test_update_delete_function(client, caplog):
    db.engine.execute("INSERT INTO bot VALUES (30, 'WandaVision')")
    db.engine.execute("INSERT INTO bot VALUES (31, 'Captain America')")
    response = client.get('/test')
    caplog.set_level(logging.INFO)
    db.engine.execute(f"DELETE FROM bot WHERE id=31")
    assert f'INFO     tests.test_app.testing_app:logger.py:6 User with id=None has started updating model bot ' \
           f'(raw ID=31)' in caplog.text
    assert f'INFO     tests.test_app.testing_app:logger.py:6 User with id=None has started deleting model bot ' \
           f'(raw ID=30)' in caplog.text
    assert f'INFO     tests.test_app.testing_app:logger.py:12 User with id=None has finished updating model bot ' \
           f'(raw ID=31)' in caplog.text
    assert f'INFO     tests.test_app.testing_app:logger.py:12 User with id=None has finished deleting model bot ' \
           f'(raw ID=30)' in caplog.text
