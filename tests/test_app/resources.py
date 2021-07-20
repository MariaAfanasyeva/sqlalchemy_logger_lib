from .models import Bot, User
from flask_restful import Resource
from flask import request
from .testing_app import db
from .schemas import bot_schema, user_schema


class BotResource(Resource):
    def get(self, id):
        bot = Bot.query.get_or_404(id)
        return bot_schema.dump(bot)

    def put(self, id):
        bot = Bot.query.get_or_404(id)
        bot.name = request.json["name"]
        db.session.commit()
        return bot_schema.dump(bot)

    def delete(self, id):
        bot = Bot.query.get_or_404(id)
        db.session.delete(bot)
        db.session.commit()
        return "", 204


class SignUpUser(Resource):
    def post(self):
        username = request.json["username"]
        password = request.json["password"]
        new_user = User(username=username, password=password)
        db.session.add(new_user)
        db.session.commit()
        return user_schema.dump(new_user), 201


class BotCreateResource(Resource):
    def post(self):
        name = request.json["name"]
        new_bot = Bot(
            name=name,
        )
        db.session.add(new_bot)
        db.session.commit()
        return bot_schema.dump(new_bot), 201


class BotTestResource(Resource):
    def get(self):
        bot1 = Bot.query.get_or_404(30)
        bot2 = Bot.query.get_or_404(31)
        bot2.name = "Harry James Potter"
        db.session.delete(bot1)
        db.session.commit()
        return bot_schema.dump(bot2)
