# Copyright © 2020 Noel Kaczmarek


class ServiceError(Exception):
    def __init__(self, message):
        super().__init__(message)


class ServiceConnectError(ServiceError):
    def __init__(self):
        super().__init__('Connection failed')


class ServiceUndefinedError(ServiceError):
    def __init__(self, service):
        super().__init__('%s service not set' % service)


class ServiceManager(object):
    def __init__(self):
        self._administration = None
        self._authentication = None

    @property
    def administration(self):
        if self._administration:
            return self._administration.service
        raise ServiceUndefinedError('Administration')
    
    @administration.setter
    def administration(self, admin):
        self._administration = admin

    @property
    def authentication(self):
        if self._authentication:
            return self._authentication.service
        raise ServiceUndefinedError('Authentication')

    @authentication.setter
    def authentication(self, auth):
        self._authentication = auth
