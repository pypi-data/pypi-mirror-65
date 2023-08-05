import re
import log_request_id
from xmlrpc.client import Transport, SafeTransport, ServerProxy
from base64 import b64encode
from urllib.parse import urljoin
from functools import wraps
from django.http import HttpRequest
from django.conf import settings
from rest_framework.request import Request
from ywkd_tools.inner_service_apis.errors import InnerAPIError
from ywkd_tools.logger import logger
from ywkd_tools.utils import get_request_id


class SpecialTransport(Transport):
    """
    SpecialTransport (http)
    """

    preset_headers = {}

    def set_header(self, key, value):
        if key.lower().startswith('http'):
            key = key[5:]
        if value == None:
            self.preset_headers.pop(key, None)
        else:
            self.preset_headers[key] = value

    def send_headers(self, connection, headers):
        for key, val in self.preset_headers.items():
            connection.putheader(key, val)
        super().send_headers(connection, headers)

    # def send_content(self, connection, request_body):
    #     connection.putheader("Content-Type", "text/xml")
    #     connection.putheader("Content-Length", str(len(request_body)))
    #     connection.endheaders()
    #     if request_body:
    #         connection.send(request_body)


class SpecialSafeTransport(SafeTransport):
    """
    SpecialSafeTransport (https)
    """

    preset_headers = {}

    def set_header(self, key, value):
        if key.lower().startswith('http'):
            key = key[5:]
        if value == None:
            self.preset_headers.pop(key, None)
        else:
            self.preset_headers[key] = value

    def send_headers(self, connection, headers):
        for key, val in self.preset_headers.items():
            connection.putheader(key, val)
        super().send_headers(connection, headers)

    # def send_content(self, connection, request_body):
    #     connection.putheader("Content-Type", "text/xml")
    #     connection.putheader("Content-Length", str(len(request_body)))
    #     connection.endheaders()
    #     if request_body:
    #         connection.send(request_body)


class InnerServices(object):
    """
    InnerServices
    """

    service_name = ''
    base_url = ''
    secret = ''
    inited = False

    def __init__(self):
        raise TypeError('Cannot create "InnerServices" instances.')

    @classmethod
    def setup(cls, service_name, base_url, secret):
        cls.base_url = base_url
        services = [getattr(cls, key) for key in cls.__dict__ if isinstance(getattr(cls, key), InnerService)]
        for service in services:
            service.init(service_name, base_url, secret)
        cls.inited = True

    @classmethod
    def inner(cls, service_cls):
        service = service_cls()
        setattr(cls, service_cls.__name__, service)


class InnerService(object):
    """
    InnerService
    """

    url = None
    client = None
    http_request = None
    request_id = None

    def __init__(self, http_request=None, request_id=None):
        """
            @parms http_request: django.http.HttpRequest 或 rest_framework.request.Request
            @parms request_id: 不指定时 默认使用上下文中的request_id, 建议在Django View 中无特殊需求则无需
                指定 http_request or request_id, 在异步任务中建议指定该值, 保证log日志的完整性
        """
        if not hasattr(self, 'url'):
            raise InnerAPIError('InnerService class "%s" need has a url attr!' %
                                self.__class__.__name__)
        if http_request:
            assert (isinstance(http_request, HttpRequest) or isinstance(http_request, Request)), (
                'The `request` argument must be an instance of '
                '`django.http.HttpRequest` or `rest_framework.request.Request`, not `{}.{}`.'
                .format(http_request.__class__.__module__, http_request.__class__.__name__)
            )
        if http_request:
            self.http_request = http_request
            self.request_id = http_request.id
        if request_id:
            self.request_id = request_id

    def __call__(self, http_request=None, request_id=None):
        new_instance = self.__class__(http_request=http_request, request_id=request_id)
        new_instance.init(self.service_name, self.base_url, self.secret)
        return new_instance

    def get_url(self):
        """获取url"""
        url = self.url
        if not re.match(r'^(http|https)://', self.url, re.I):
            assert (self.base_url != None and re.match(r'^(http|https)://', self.base_url, re.I)), (
                'base_url must not null and start with http or https'
            )
            url = urljoin(self.base_url, self.url)
        return url

    def get_transport(self):
        """获取transport"""
        transport = None
        if self.http_url.startswith('https'):
            transport = SpecialSafeTransport()
        else:
            transport = SpecialTransport()

        # 认证: HTTP_AUTHORIZATION basic xxxxxxxx
        basic_auth_str = '{service_name}:{secret}'.format(**{
            'service_name': self.service_name,
            'secret': self.secret
        })
        header_auth_str = 'basic {}'.format(
            b64encode(bytes(basic_auth_str, 'utf-8')).decode('utf-8'))
        transport.set_header('Authorization', header_auth_str)
        return transport

    def init(self, service_name, base_url, secret):
        # logger.debug('Init inner service: "{}"'.format(self.__class__.__name__))
        self.service_name = service_name
        self.base_url = base_url
        self.secret = secret
        self.http_url = self.get_url()
        self.transport = self.get_transport()
        self.client = ServerProxy(self.http_url, transport=self.transport, allow_none=True, use_datetime=True)

    @property
    def rpc_client(self):
        assert self.client, (
            '"{}" instance not setup yet, please do init first!'
            .format(self.__class__.__name__)
        )

        # 在请求头中添加 request_id
        request_id = None
        if self.request_id:
            request_id = self.request_id
        else:
            request_id = get_request_id()
        # request_id_header = getattr(settings, log_request_id.REQUEST_ID_HEADER_SETTING, 'X-Request-Id')  # bug HTTP_X_REQUEST_ID 不能直接使用
        self.transport.set_header('X-Request-Id', request_id)

        return self.client
