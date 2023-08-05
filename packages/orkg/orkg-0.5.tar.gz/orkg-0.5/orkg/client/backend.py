import hammock
from .resources import ResourcesClient
from .predicates import PredicatesClient
from .classes import ClassesClient
from .literals import LiteralsClient
from .stats import StatsClient
from .statements import StatementsClient
from .papers import PapersClient


class ORKG(object):

    def __init__(self, host=None, creds=None, **kwargs):
        if host is not None and not host.startswith('http'):
            raise ValueError('host must begin with http or https')
        self.host = host if host is not None else 'http://127.0.0.1:8000'
        self.core = hammock.Hammock(self.host)
        self.token = None
        if creds is not None and len(creds) == 2:
            self.__authenticate(creds[0], creds[1])
        self.backend = self.core.api
        self.resources = ResourcesClient(self)
        self.predicates = PredicatesClient(self)
        self.classes = ClassesClient(self)
        self.literals = LiteralsClient(self)
        self.stats = StatsClient(self)
        self.statements = StatementsClient(self)
        self.papers = PapersClient(self)

    def __authenticate(self, email, password):
        data = {
            'username': email,
            'grant_type': 'password',
            'client_id': 'orkg-client',
            'password': password
        }
        resp = self.core.oauth.token.POST(data=data, headers={'Authorization': 'Basic b3JrZy1jbGllbnQ6c2VjcmV0'})
        if resp.status_code == 200:
            self.token = resp.json()['access_token']
        else:
            raise IOError(f"Please check the credentials provided!, got the error {resp.content}")


    def ping(self):
        pass  # TODO: see how to ping ORKG host to know if it is alive
