from .. import db
from datetime import datetime, timedelta
from app.main.model.active_token import ChangePassToken, Device
from app.main.model.user import User
from ..util.token_util import generate_rand_token
from sqlalchemy import and_


def save_pass_token(token, email):
    if not token:
        token = generate_rand_token()
    active_token = ChangePassToken(token=token, email=email)
    try:
        # insert the token
        db.session.add(active_token)
        db.session.commit()
        return True
    except Exception:
        return False


def delete_pass_token(active_token):
    try:
        res = ChangePassToken.query.filter_by(token=str(active_token)).first()
        if res:
            db.session.delete(res)
            db.session.commit()
        return True
    except Exception:
        return False


def check_pass_token(active_token):
    try:
        res = ChangePassToken.query.filter_by(token=str(active_token)).first()
        if res:
            db.session.delete(res)
            db.session.commit()
            return True, res.email
        return False, None
    except Exception:
        return False, None


def build_pass_link(email, token):
    if token:
        return 'Token to change password is '+token
    try:
        res = ChangePassToken.query.filter_by(email=str(email)).first()
        if res:
            return 'Token to change password is '+res.token
        return False, None
    except Exception:
        return False, None


def check_email(email):
    try:
        res = User.query.filter_by(email=email).first()
        if res:
            return True, res.id
        return False, None
    except Exception:
        return False, None

def check_pass(account_id, password):
    try:
        res = User.query.filter_by(id=account_id).first()
        if res and res.check_password(password):
            return True, res.email
        return False, None
    except Exception:
        return False, None
