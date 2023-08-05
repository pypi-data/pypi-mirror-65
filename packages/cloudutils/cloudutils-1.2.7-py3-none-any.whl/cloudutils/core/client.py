# Copyright © 2020 Noel Kaczmarek
from cloudutils.core.utils import timestamp
from suds.client import Client


class Session:
    def __init__(self, id, user, lifetime, timestmp):
        self.id = id
        self.user = user
        self.lifetime = lifetime
        self.timestamp = timestmp
        self.last_refreshed = timestamp()

    def expired(self):
        if self.timestamp + self.lifetime * 60000 > timestamp():
            return False
        return True


class ClientManager:
    def __init__(self, adminHost, *args, **kwargs):
        self.clients = []
        self.cache_lifetime = 5
        self.administrationServiceHost = adminHost
        self._administration = Client('http://%s:8000/?wsdl' % adminHost)
        result = self.administration.getService(2)
        self._authentication = Client('http://%s:%d/?wsdl' % (result.host, result.type.port))

    def check(self, user, sessionID):
        session = None

        for session in self.clients:
            if session.id == sessionID and session.user == user:
                if not session.expired() and session.last_refreshed + self.cache_lifetime * 60000 > timestamp():
                    return True
                else:
                    break
            session = None

        response = self.authentication.authenticate(user, sessionID).integer

        if response:
            if session:
                index = self.clients.index(session)
                self.clients[index].lifetime = response[1]
                self.clients[index].timestamp = response[0]
                self.clients[index].last_refreshed = timestamp()
            else:
                self.clients.append(Session(sessionID, user, response[1], response[0]))
            return True
        else:
            if session:
                self.clients.remove(session)
            return False

    def authorize(self, user, resources, action):
        return self.authentication.authorize(user, resources, action)

    def getRoot(self, userID):
        pass

    @property
    def administration(self):
        return self._administration.service

    @property
    def authentication(self):
        return self._authentication.service
