# Copyright © 2020 Noel Kaczmarek
from suds.client import Client


class Network(object):
    def __init__(self, host, port, **kwargs):
        self.administration_service = administration
        self._administration = Client('http://%s:8000/?wsdl' % self.administration_service)
        self.authentication_service = self.administration.getService(2)
        self.resource_service = self.administration.getService(3)
        self._authentication = Client('http://%s:%d/?wsdl' % (self.authentication_service.host, self.authentication_service.type.port))
        self._resource = Client('http://%s:%d/?wsdl' % (self.resource_service.host, self.resource_service.type.port))

    @property
    def administration(self):
        return self._administration.service

    @property
    def authentication(self):
        return self._authentication.service

    @property
    def resource(self):
        return self._resource.service