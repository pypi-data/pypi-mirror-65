# rest-framework 自定义认证

import traceback
from base64 import b64decode
from rest_framework import authentication, exceptions
from ywkd_tools.inner_service_apis import InnerServices
from ywkd_tools.logger import logger


class Auth(object):
    """
    Auth
    """

    service_name = None
    rpc_base_url = None
    rpc_secret = None
    inited = False

    def __init__(self):
        raise TypeError('Cannot create "Auth" instances.')

    @classmethod
    def setup(cls, service_name=None, rpc_base_url=None, rpc_secret=None):
        cls.service_name = service_name
        cls.rpc_base_url = rpc_base_url
        cls.rpc_secret = rpc_secret

        if InnerServices.inited:
            cls.service_name = InnerServices.service_name
            cls.rpc_base_url = InnerServices.base_url
            cls.rpc_secret = InnerServices.secret
        elif service_name and rpc_base_url:
            InnerServices.setup(service_name=service_name,
                                base_url=rpc_base_url,
                                secret=rpc_secret)
        cls.inited = True

    @classmethod
    def inner(cls, authentication_class):
        authentication_class.auth_class = cls
        setattr(cls, authentication_class.__name__, authentication_class)


@Auth.inner
class RPCBasciAuthentication(object):
    """
    RPC 认证 (只能用于RPC)
        headers:
            HTTP_AUTHORIZATION=basci [username]:[password]
    """

    auth_class = None

    def do_check(self, request, username, password):
        if password != self.auth_class.rpc_secret:
            logger.info('密码/用户错误')
            return False
        return True

    def authenticate(self, request):
        if not self.auth_class.inited:
            raise Exception('Auth not setup yet, please do this first!')

        # 没有设置 rpc sercret 则忽略认证
        if not self.auth_class.rpc_secret:
            return True

        username = password = None
        basic_auth = request.META.get('HTTP_AUTHORIZATION')
        if not basic_auth:
            logger.info('缺少 basci authrization')
            return False

        try:
            auth_method, auth_string = basic_auth.split(' ', 1)
        except Exception:
            logger.info('http头部 HTTP_AUTHORIZATION 格式错误')
            return False

        if auth_method.lower() == 'basic':
            try:
                auth_string = b64decode(auth_string.strip())
                username, password = auth_string.decode().split(':', 1)
            except Exception:
                logger.info('错误的 Basic 格式')
                return False
        else:
            logger.info('需要 basic authrization')
            return False

        res = self.do_check(request, username, password)
        if not res:
            return False
        return  True


@Auth.inner
class RSTFBasciAuthentication(authentication.BaseAuthentication):
    """
    Django rest_framework Basci 认证: (只能用于Django rest_framework)
        headers:
            HTTP_AUTHORIZATION=basci [user_id]:[token]
    """

    auth_class = None

    def do_check(self, request, user_id, token):
        service_name = self.auth_class.service_name
        api_name = request.resolver_match.url_name
        operator_type = request.method

        # 检测接口访问权限
        res = None
        try:
            res = InnerServices.Cperm().check_api_operate_perms(
                user_id=user_id,
                token=token,
                service_name=service_name,
                api_name=api_name,
                operator_type=operator_type)
        except Exception as e:
            traceback.print_exc()
            raise exceptions.AuthenticationFailed('与认证服务cperm通信失败')

        if res['code'] != 0:
            raise exceptions.AuthenticationFailed(res['codemsg'])

        # 获取用户信息
        user = InnerServices.Cperm().get_user(user_id)
        user['token'] = request.token
        user['basic_auth'] = request.basic_auth
        return user

    def authenticate(self, request):
        if not self.auth_class.inited:
            raise Exception('Auth not setup yet, please do this first!')

        user_id = token = None
        basic_auth = request.META.get('HTTP_AUTHORIZATION')
        if not basic_auth:
            raise exceptions.AuthenticationFailed('缺少 basci authrization')

        try:
            auth_method, auth_string = basic_auth.split(' ', 1)
        except Exception:
            raise exceptions.AuthenticationFailed('http头部 HTTP_AUTHORIZATION 格式错误')

        if auth_method.lower() == 'basic':
            try:
                auth_string = b64decode(auth_string.strip())
                user_id, token = auth_string.decode().split(':', 1)
            except Exception:
                traceback.print_exc()
                raise exceptions.AuthenticationFailed('错误的 Basic 格式')
        else:
            raise exceptions.AuthenticationFailed('需要 basic authrization')

        request.token = token
        request.basic_auth = basic_auth
        res = self.do_check(request, user_id, token)
        return (res, None)
