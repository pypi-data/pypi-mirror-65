from datalogue.clients.http import _HttpClient, Union, Optional, HttpMethod
from datalogue.clients.jobs import _JobsClient
from datalogue.clients.datastore_collections import _DatastoreCollectionClient
from datalogue.clients.stream_collection import _StreamCollectionClient
from datalogue.clients.credentials import _CredentialsClient
from datalogue.clients.datastore import _DatastoreClient
from datalogue.clients.organization import _OrganizationClient
from datalogue.clients.group import _GroupClient
from datalogue.clients.user import _UserClient
from datalogue.clients.metrics import _MetricsClient
from datalogue.clients.ontology import _OntologyClient
from datalogue.clients.training import _TrainingClient, _DeploymentClient
from datalogue.clients.automation import _AutomationClient
from datalogue.errors import DtlError

from urllib.parse import urlparse

from datalogue.models.organization import User
from datalogue.models.version import Version


class DtlCredentials:
    """
    Information to be able to connect to the platform

    :param username: username to be used to login on the platform
    :param password: password to be used to login on the platform
    :param uri: root url where the system lives ie: https://test.datalogue.io/api
    :param ca_certificate: (Optional) path to the CA Certificate
    """

    def __init__(self, username: str, password: str, uri: str, ca_certificate: Optional[str] = None):
        self.username = username.strip()
        self.password = password.strip()
        self.ca_certificate = ca_certificate

        uri = uri.strip()

        if self.validate_url(uri) is not True:
            raise DtlError("The URL you provided is invalid")

        if not uri.endswith("/api"):
            raise DtlError("The URL you provided doesn't end with '/api' it is most likely invalid")

        self.uri = uri

    def validate_url(self, uri: str) -> bool:
        parsed_url = urlparse(uri)
        return all([parsed_url.scheme, parsed_url.netloc])

    def __repr__(self):
        res = f'{self.__class__.__name__}(username: {self.username!r}, password: ****, uri: {self.uri!r})'
        if self.ca_certificate is None:
            return res
        else:
            return res[:-1] + f', ca_certificate: {self.ca_certificate!r})'


class Dtl:
    """
    Root class to be built to interact with all the services

    :param credentials: contains the information to connect
    """

    def __init__(self, credentials: DtlCredentials):
        self.uri = credentials.uri
        self.username = credentials.username
        self.http_client = _HttpClient(credentials.uri)

        login_res = self.http_client.login(credentials.username, credentials.password, credentials.ca_certificate)
        if isinstance(login_res, DtlError):
            raise login_res

        self.group = _GroupClient(self.http_client)
        """Client to interact with the groups"""
        self.user = _UserClient(self.http_client)
        """Client to interact with the users"""
        self.organization = _OrganizationClient(self.http_client)
        """Client to interact with the organization part of the stack"""
        self.streams = _StreamCollectionClient(self.http_client)
        """Client to interact with the streams"""
        self.jobs = _JobsClient(self.http_client)
        """Client to interact with the jobs"""
        self.datastore_collection = _DatastoreCollectionClient(self.http_client)
        """Client to interact with the datastore collections"""
        self.datastore = _DatastoreClient(self.http_client)
        """Client to interact with the datastores"""
        self.credentials = _CredentialsClient(self.http_client)
        """Client to interact with credentials"""
        self.stream_collection = _StreamCollectionClient(self.http_client)
        """Client to interact with the stream collections"""
        self.metrics = _MetricsClient(self.http_client)
        """Client to interact with metrics uploads"""
        self.ontology = _OntologyClient(self.http_client)
        """Client to interact with ontologies"""
        self.training = _TrainingClient(self.http_client)
        """Client to interact with training"""
        self.deployment = _DeploymentClient(self.http_client)
        """Client to interact with deployment"""
        self.automation = _AutomationClient(self.http_client, self.ontology)
        """Client to interact with regexes"""

    def __repr__(self):
        return f'Logged in {self.uri!r} with {self.username!r} account.'

    @staticmethod
    def signup(uri='', first_name='', last_name='', email='', password='', accept_terms=True,
               ca_certificate: Optional[str] = None) -> Union[DtlError, User]:
        """
        Perform signup of user
        :param uri: The target URI where the user data will be associated in
        :param accept_terms: Whether the user accept the following terms : https://www.datalogue.io/pages/terms-of-service
        :param ca_certificate: (Optional) path to the CA Certificate
        :return: User object if successful, else return DtlError
        """
        http_client = _HttpClient(uri)
        http_client.get_csrf()
        registered_user = http_client.signup(first_name, last_name, email, password, accept_terms, ca_certificate)
        return registered_user

    def version(self) -> Union[DtlError, Version]:
        """
        Get version number of SDK, platform, and the platform's services'
        :return: Version object containing version number of SDK, platform, and the platform's services'
        """
        res = self.http_client.make_authed_request("/version", HttpMethod.GET)
        if isinstance(res, DtlError):
            return res
        return Version.from_payload(res)


