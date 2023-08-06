# Copyright © 2020 Noel Kaczmarek
from spyne.model.fault import Fault


class PublicKeyError(Fault):
    __namespace__ = 'cloud'

    def __init__(self, value):
        super(PublicKeyError, self).__init__(faultstring='Value %r not found' % value)


class AuthenticationError(Fault):
    __namespace__ = 'cloud'

    def __init__(self, username):
        # TODO: self.transport.http.resp_code = HTTP_401

        super(AuthenticationError, self).__init__(
                faultcode='Client.AuthenticationError',
                faultstring='Invalid authentication request for %r' % username)


class AuthorizationError(Fault):
    __namespace__ = 'cloud'

    def __init__(self):
        # TODO: self.transport.http.resp_code = HTTP_401

        super(AuthorizationError, self).__init__(
                   faultcode='Client.AuthorizationError',
                   faultstring='You are not authozied to access this resource.')