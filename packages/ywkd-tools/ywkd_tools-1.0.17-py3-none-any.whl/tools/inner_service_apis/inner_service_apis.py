import re
import xmlrpc
from base64 import b64encode
from urllib.parse import urljoin
from .errors import InnerAPIError
from .utils import Singleton


class SpecialTransport(xmlrpc.client.Transport):

    def __init__(self, header_auth_str, *args, **kwargs):
        self.header_auth_str = header_auth_str
        super().__init__(*args, **kwargs)

    def send_headers(self, connection, headers):
        connection.putheader("Authorization", self.header_auth_str)
        super().send_headers(connection, headers)

    # def send_content(self, connection, request_body):
    #     connection.putheader("Content-Type", "text/xml")
    #     connection.putheader("Content-Length", str(len(request_body)))
    #     connection.endheaders()
    #     if request_body:
    #         connection.send(request_body)


class InnerServices(object, metaclass=Singleton):
    """
    InnerServices
    """

    is_inited = False

    def init(self, base_url, username, password):
        self.is_inited = True
        self.base_url = base_url
        basic_auth_str = '{username}:{password}'.format(**{'username': username, 'password': password})
        header_auth_str = 'basic {}'.format(b64encode(bytes(basic_auth_str, 'utf-8')).decode('utf-8'))
        self.transport = SpecialTransport(header_auth_str=header_auth_str)
        services = [getattr(self, key) for key in self.__dict__ if isinstance(getattr(self, key), InnerService)]
        for service in services:
            service.init()

    @classmethod
    def inner(cls, service_cls):
        instance = cls()
        service = service_cls(instance)
        setattr(instance, service_cls.__name__, service)


class InnerService(object):
    """Base Inner Api"""

    def __init__(self, service_interface):
        if not hasattr(self, 'url'):
            raise InnerAPIError('Interface class "%s" need has a url attr!' %
                                self.__class__.__name__)
        self.service_interface = service_interface

    def init(self):
        if not self.service_interface.is_inited:
            raise InnerAPIError('do InnerServices.init() first!')
        print('init innerService: "{}"'.format(self.__class__.__name__))
        url = self.url
        if not re.match(r'^(http|https)://',  self.url, re.I):
            url = urljoin(self.service_interface.base_url, self.url)
        self.client = xmlrpc.client.ServerProxy(url, transport=self.service_interface.transport)
