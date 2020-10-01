
from .. import db

from app.main.model.models import TestTable


def save_record(data):
    blacklist_token = TestTable(data['token'], data['email'])
    try:
        # insert the token
        db.session.add(blacklist_token)
        db.session.commit()
        response_object = {
            'status': 'success',
            'message': 'Successfully.'
        }
        return response_object, 201
    except Exception as e:
        response_object = {
            'status': 'fail',
            'message': e
        }
        return response_object, 500
