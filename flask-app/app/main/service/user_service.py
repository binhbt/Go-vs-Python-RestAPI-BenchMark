import uuid
import datetime
import logging

from .. import db
from app.main.model.user import User
from app.main.model.active_token import Device
from common.validate_util import check_owner_resource
from .active_token_service import delete_all_device_by_user
LOG = logging.getLogger('app')
from common.data_util import get_data, build_json_result
# TODO: add db.session.rollback() when add or update database

def save_new_user(data):
    user = User.query.filter_by(email=data['email']).first()
    if not user or not user.is_active:
        if user and not user.is_active:
            Device.query.filter_by(user_id=user.id).delete()
            User.query.filter_by(email=data['email']).delete()
        facebook_id = None
        google_id = None
        full_name = None
        avatar = None
        if 'facebook_id' in data:
            facebook_id = data['facebook_id']
        if 'google_id' in data:
            google_id = data['google_id']
        if 'full_name' in data:
            full_name = data['full_name']
        if 'avatar' in data:
            avatar = data['avatar']
        if 'avatar' in data:
            avatar = data['avatar']
        new_user = User(
            email=data['email'],
            username=data['username'],
            password=data['password'],
            registered_on=datetime.datetime.utcnow(),
            last_logged = datetime.datetime.utcnow(),
            role=data['role'],
            account_type=data['account_type'],
            facebook_id=facebook_id,
            google_id=google_id,
            full_name=full_name,
            avatar=avatar
        )
        result = save_changes(new_user)
        if not result:
            return generate_token(new_user)
        else:
            return build_json_result(None, 500, result)
    else:
        response_object = {
            'user_id':user.id,
            # 'status': 'fail',
            # 'message': 'User already exists. Please Log in.',
        }
        return build_json_result(response_object, 409, 'User already exists. Please Log in.')
def save_new_social_user(data):
    user = User.query.filter_by(email=data['email']).first()
    if not user:
        facebook_id = None
        google_id = None
        full_name = None
        avatar = None
        if 'facebook_id' in data:
            facebook_id = data['facebook_id']
        if 'google_id' in data:
            google_id = data['google_id']
        if 'full_name' in data:
            full_name = data['full_name']
        if 'avatar' in data:
            avatar = data['avatar']
        if 'avatar' in data:
            avatar = data['avatar']
        new_user = User(
            email=data['email'],
            username=data['username'],
            password=data['password'],
            registered_on=datetime.datetime.utcnow(),
            last_logged = datetime.datetime.utcnow(),
            role=data['role'],
            account_type=data['account_type'],
            facebook_id=facebook_id,
            google_id=google_id,
            full_name=full_name,
            avatar=avatar,
            is_active=True,
            active_on = datetime.datetime.utcnow(),
        )
        result = save_changes(new_user)
        if not result:
            return generate_token(new_user)
        else:
            return build_json_result(None, 500, result)
    else:
        response_object = {
            # 'status': 'fail',
            'user_id':user.id,
            # 'message': 'User already exists. Please Log in.',
        }
        return build_json_result(response_object, 409, 'User already exists. Please Log in.')

def get_all_users():
    return User.query.all()


def get_a_user(id):
    return User.query.filter_by(id=id).first()

def get_user_by_email(email):
    return User.query.filter_by(email=email).first()

def generate_token(user):
    try:
        # generate the auth token
        auth_token = User.encode_auth_token(user.id, user.role)
        response_object = {
            'user_id':user.id,
            # 'status': 'success',
            # 'message': 'Successfully registered.',
            'token': auth_token.decode()
        }
        return build_json_result(response_object, 201, 'Successfully registered.')
    except Exception as e:
        return build_json_result(None, 401, 'Some error occurred. Please try again.')


def save_changes(data):
    try:
        db.session.add(data)
        db.session.commit()
        return None
    except Exception as e:
        LOG.exception(e)
        db.session.rollback()
        return e.args

def active_user(email):
    try:
        user = get_user_by_email(email)
        if user:
            user.is_active = True
            user.active_on = datetime.datetime.utcnow()
            db.session.commit()
            return True, 'Your account is activated!'
        else:
            return False, 'Account is not exist!'
    except Exception as e:
        LOG.exception(e)
        db.session.rollback()
        return False, e.args
def update_logged_time(user):
    try:
        if user:
            user.last_logged = datetime.datetime.utcnow()
            db.session.commit()
            return True, 'Logged time updated'
        else:
            return False, 'Account is not exist!'
    except Exception as e:
        LOG.exception(e)
        db.session.rollback()
        return False, e.args
def update_password(email, password):
    try:
        user = get_user_by_email(email)
        if user:
            user.password = password
            db.session.commit()
            return True, 'Your password has updated'
        else:
            return False, 'Account is not exist!'
    except Exception as e:
        LOG.exception(e)
        db.session.rollback()
        return False, e.args

def delete_account_by_id(id):
    try:
        profile = User.query.filter_by(id=id).first()
        if profile:
            if not check_owner_resource(id):
                return build_json_result(None, 401, 'You have not permission to access this api')
            delete_all_device_by_user(id)
            db.session.delete(profile)
            db.session.commit()
            return build_json_result(None, 200, 'Profile deleted')
        else:
            return build_json_result(None, 404, 'Profile not found')
    except Exception as e:
        LOG.exception(e)
        db.session.rollback()
        return build_json_result(None, 500, e.args)