from flask_restful import Api
from .testing_app import app
from .resources import SignUpUser, BotResource, BotCreateResource, BotTestResource

api = Api(app)


api.add_resource(SignUpUser, '/signUp', endpoint='sign_up_user')
api.add_resource(BotResource, '/bot/<int:id>', endpoint='single_bot_resource')
api.add_resource(BotCreateResource, '/bot', endpoint='create_bot')


api.add_resource(BotTestResource, '/test', endpoint='test_resource')
