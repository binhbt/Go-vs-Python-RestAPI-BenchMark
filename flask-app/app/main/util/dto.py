from flask_restplus import Namespace, fields


class TestDto:
    api = Namespace('test', description='authentication related operations')
    user = api.model('test', {
        'id': fields.Integer(description='account id'),
        'email': fields.String(required=True, description='The email address'),
        'role': fields.String(required=True, description='The user password '),
    })
