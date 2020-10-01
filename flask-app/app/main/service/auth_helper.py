from common.data_util import get_data, build_json_result
from app.main.model.user import User
from app.main.model.active_token import Device
from ..service.blacklist_service import save_token
from ..service.user_service import update_logged_time
from ..util.token_util import save_token_to_black_list
from ..util.user_util import get_user_profile
import requests
from ..service.user_service import save_new_user, save_new_social_user
from ..service.active_token_service import save_refresh_token, delete_device, get_device
import logging
LOG = logging.getLogger('app')


class Auth:
    @staticmethod
    def login_user(data):
        try:
            # fetch the user data
            user = User.query.filter_by(email=data.get('email')).first()
            if user and user.check_password(data.get('password')):
                if user.account_type == 'facebook':
                    return build_json_result(None, 403, 'You must login by facebook account')
                if user.account_type == 'google':
                    return build_json_result(None, 403, 'You must login by google account')
                isOk, message = save_refresh_token(user.id, get_data(data, 'device_id'), get_data(
                    data, 'device_name'), get_data(data, 'device_model'))
                update_logged_time(user)
                if not user.is_active:
                    return build_json_result(None, 403, 'You need active your account to login')
                auth_token = User.encode_auth_token(
                    user.id, user.role, user.account_type)
                if auth_token:
                    response_object = {
                        'user_id': user.id,
                        'refresh_token': message,
                        'token': auth_token.decode()
                    }
                    # return response_object, 200
                    return build_json_result(response_object, 200, 'Successfully logged in.')
            else:
                return build_json_result(None, 401, 'email or password does not match.')

        except Exception as e:
            print(e)
            return build_json_result(None, 500, 'Try again')

    @staticmethod
    def logout_user(data, user_id, device_id):
        if data:
            auth_token = data.split(" ")[1]
        else:
            auth_token = ''
        if auth_token:
            delete_device(user_id, device_id)
            if save_token_to_black_list(auth_token, user_id):
                return build_json_result(None, 200, 'Successfully logged out.')
            else:
                return build_json_result(None, 500, 'Server has error')
        else:
            return build_json_result(None, 403, 'Provide a valid auth token.')

    @staticmethod
    def get_logged_in_user(new_request):
        # get the auth token
        auth_token = new_request.headers.get('Authorization')
        if auth_token:
            resp = User.decode_auth_token(auth_token)
            if not isinstance(resp, str):
                user = User.query.filter_by(id=resp).first()
                data = {
                    'user_id': user.id,
                    'email': user.email,
                    'admin': user.admin,
                    'registered_on': str(user.registered_on)
                }
                return build_json_result(data, 200) 
            return build_json_result(None, 401, resp)
        else:
            return build_json_result(None, 401, 'Provide a valid auth token.')

    @staticmethod
    def login_facebook_user(post_data):
        try:
            if not 'token' in post_data:
                return build_json_result(None, 404, 'You need give me your facebook token')
            else:
                fb_token = post_data['token']
                response = requests.get("https://graph.facebook.com/v3.3/me",
                                        params={'fields': 'id, name, email',
                                                'access_token': fb_token},
                                        headers=None)
                data = response.json()
                LOG.info(data)
                user_data = {}
                if data and not 'error' in data:
                    fb_id = data['id']
                    fb_name = data['name']
                    if 'email' in data:
                        fb_email = data['email']
                    else:
                        fb_email = fb_id+'@facebook.com'

                    user = User.query.filter_by(facebook_id=fb_id).first()
                    LOG.info(user)
                    # login success
                    if user:
                        auth_token = User.encode_auth_token(
                            user.id, user.role, user.account_type)
                        isOk, message = save_refresh_token(user.id, get_data(post_data, 'device_id'), get_data(
                            post_data, 'device_name'), get_data(post_data, 'device_model'))
                        if auth_token:
                            # profile = get_user_profile(user.id, user.account_type)
                            response_object = {
                                "user_id": user.id,
                                # 'profile':profile,
                                # 'status': 'success',
                                # 'message': 'Successfully logged in.',
                                'token': auth_token.decode(),
                                'refresh_token': message
                            }
                            return build_json_result(response_object, 200, 'Successfully logged in.')
                    else:
                        user_data['email'] = fb_email
                        user_data['username'] = fb_email
                        user_data['full_name'] = fb_name
                        user_data['facebook_id'] = fb_id
                        user_data['role'] = 'user'
                        user_data['account_type'] = 'facebook'
                        user_data['password'] = 's3cr3tk3y'
                        user_data['avatar'] = 'http://graph.facebook.com/' + \
                            fb_id+'/picture?type=square'
                        result = save_new_social_user(data=user_data)
                        isOk, message = save_refresh_token(get_data(result, 'user_id'), get_data(
                            post_data, 'device_id'), get_data(post_data, 'device_name'), get_data(post_data, 'device_model'))
                        result[0]['resfresh_token'] = message
                        # profile = get_user_profile(
                        #     get_data(result, 'user_id'), user_data['account_type'])
                        # result[0]['profile'] = profile
                        return result
                else:
                    return build_json_result(None, 401, 'Your token is not valid')

        except Exception as e:
            LOG.info(e)
            return build_json_result(None, 500, 'Try again')

    @staticmethod
    def login_google_user(post_data):
        try:
            if not 'token' in post_data:
                return build_json_result(None, 404, 'You need give me your facebook token')
            else:
                gg_token = post_data['token']
                headers = {'Authorization': 'OAuth '+gg_token}
                response = requests.get("https://www.googleapis.com/oauth2/v1/userinfo", None,
                                        headers=headers)
                data = response.json()
                LOG.info(data)
                user_data = {}
                if data and not 'error' in data:
                    gg_id = data['id']
                    gg_name = data['name']
                    gg_avatar = data['picture']
                    if 'email' in data:
                        gg_email = data['email']
                    else:
                        gg_email = gg_id+'@google.com'

                    user = User.query.filter_by(google_id=gg_id).first()
                    LOG.info(user)
                    # login success
                    if user:
                        auth_token = User.encode_auth_token(
                            user.id, user.role, user.account_type)
                        isOk, message = save_refresh_token(user.id, get_data(post_data, 'device_id'), get_data(
                            post_data, 'device_name'), get_data(post_data, 'device_model'))

                        if auth_token:
                            response_object = {
                                "user_id": user.id,
                                # 'status': 'success',
                                # 'message': 'Successfully logged in.',
                                'token': auth_token.decode(),
                                'resfresh_token': message
                            }
                            return build_json_result(response_object, 200, 'Successfully logged in.')
                    else:
                        user_data['email'] = gg_email
                        user_data['username'] = gg_email
                        user_data['full_name'] = gg_name
                        user_data['google_id'] = gg_id
                        user_data['role'] = 'user'
                        user_data['account_type'] = 'google'
                        user_data['password'] = 's3cr3tk3y'
                        user_data['avatar'] = gg_avatar
                        result = save_new_social_user(data=user_data)
                        LOG.info(result)
                        if result[0]['status'] == 'fail':
                            return build_json_result(None, 409, 'Your email is used')
                        isOk, message = save_refresh_token(get_data(result, 'user_id'), get_data(
                            post_data, 'device_id'), get_data(post_data, 'device_name'), get_data(post_data, 'device_model'))
                        LOG.info(result)
                        result[0]['resfresh_token'] = message
                        return result
                else:
                    return build_json_result(None, 401, 'Your token is not valid')

        except Exception as e:
            LOG.info(e)
            return build_json_result(None, 500, 'Try again')

    def renew_token(device_id, refresh_token):
        if device_id and refresh_token:
            LOG.info(device_id)
            device, status = get_device(device_id, refresh_token)
            LOG.info(device)
            # LOG.info(device)
            if device:
                user = User.query.filter_by(id=device.user_id).first()
                if user:
                    auth_token = User.encode_auth_token(
                        user.id, user.role, user.account_type)
                    response_object = {
                        # 'status': 'success',
                        # 'message': 'Successfully renew token',
                        'token': auth_token.decode()
                    }
                    return build_json_result(response_object, 200, 'Successfully renew token')
                else:
                    return build_json_result(None, 500, 'Can not renew')
            else:
                return build_json_result(None, 500, 'Can not renew')
        else:
            return build_json_result(None, 403, 'Provide a valid refresh token.')
