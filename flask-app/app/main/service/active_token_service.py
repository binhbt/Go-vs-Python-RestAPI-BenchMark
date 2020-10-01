from .. import db
from datetime import datetime, timedelta
from app.main.model.active_token import ActiveToken, Device
from ..util.token_util import generate_rand_token
from sqlalchemy import and_


def save_token(token, email):
    active_token = ActiveToken(token=token, email=email)
    try:
        # insert the token
        db.session.add(active_token)
        db.session.commit()
        return True
    except Exception:
        return False


def delete_token(active_token):
    try:
        res = ActiveToken.query.filter_by(token=str(active_token)).first()
        if res:
            db.session.delete(res)
            db.session.commit()
        return True
    except Exception:
        return False


def check_token(active_token):
    try:
        res = ActiveToken.query.filter_by(token=str(active_token)).first()
        if res:
            db.session.delete(res)
            db.session.commit()
            return True, res.email
        return False, None
    except Exception:
        return False, None


def build_active_link(email, token):
    if token:
        return 'Please click this link to active your account <a href="https://kong.sigma-solutions.vn/api/v1/auth/active/'+token+'">active link</a>'
    try:
        res = ActiveToken.query.filter_by(email=str(email)).first()
        if res:
            return 'Please click this link to active your account <a href="https://kong.sigma-solutions.vn/api/v1/auth/active/'+res.token+'">active link</a>'
        return False, None
    except Exception:
        return False, None


def save_refresh_token(user_id, device_id, device_name, device_model):
    if not device_id:
        return False, 'Device Id must not null'
    try:
        res = Device.query.filter(
            and_(Device.user_id == user_id, Device.device_id == device_id)).first()
        if res:
            return True, res.refresh_token
    except Exception as e:
        return False, e
    dt = datetime.now()
    td = timedelta(days=400)
    expired_time = dt + td
    refresh_token = generate_rand_token()
    device = Device(user_id, device_id, device_name,
                          device_model, refresh_token, expired_time)
    try:
        # insert the token
        db.session.add(device)
        db.session.commit()
        return True, refresh_token
    except Exception as e:
        return False, e
def get_device(device_id, refresh_token):
    if not device_id:
        return None, 'Device Id must not null'
    if not refresh_token:
        return None, 'please provide refresh token'
    try:
        res = Device.query.filter(
            and_(Device.device_id == device_id, Device.refresh_token == refresh_token)).first()
        if res:
            return res, 'success'
    except Exception as e:
        return None, e
def delete_device(user_id, device_id):
    try:
        res = Device.query.filter(
            and_(Device.user_id == user_id, Device.device_id == device_id)).first()
        if res:
            db.session.delete(res)
            db.session.commit()
        return True
    except Exception:
        return False
def delete_all_device_by_user(user_id):
    try:
        Device.query.filter_by(user_id=user_id).delete()
        return True
    except Exception:
        return False