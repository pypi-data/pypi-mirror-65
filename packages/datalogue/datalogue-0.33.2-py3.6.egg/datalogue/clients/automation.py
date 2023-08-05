from _hashlib import pbkdf2_hmac
from base64 import b64encode
from typing import Optional, Union, List
from uuid import UUID

from pbkdf2 import PBKDF2

from datalogue.errors import DtlError
from datalogue.clients.http import _HttpClient, HttpMethod
from datalogue.models.permission import Permission
from datalogue.models.regex import Regex, SearchOrder, RegexTestSample
from datalogue.models.permission import ObjectType, SharePermission
from datalogue.models.classifier import Classifier, ClassificationMethod
from datalogue.models.scope_level import Scope
from datalogue.models.transformations.obfuscate import EncryptionAlgorithm
from datalogue.utils import _parse_list, is_valid_uuid
from datalogue.clients.ontology import _OntologyClient
from datalogue.models.ontology import OntologyNode


class _RegexClient:
    """
    Client to interact with the Regexes
    """

    def __init__(self, http_client: _HttpClient):
        self.http_client = http_client
        self.service_uri = "/scout"

    def create(self, regex: Regex) -> Union[DtlError, Regex]:
        """
        Creates the Regex as specified.

        :param regex: Regex definition
        :return: Regex reference with more information id, owner, regex test sample statuses
        """
        res = self.http_client.make_authed_request(
            self.service_uri + "/regexes",
            HttpMethod.POST,
            Regex._as_payload(regex))

        if isinstance(res, DtlError):
            return res

        return Regex._from_payload(res)

    def update(self, id: UUID, name: Optional[str] = None, description: Optional[str] = None,
               pattern: Optional[str] = None) -> Union[Regex, DtlError]:
        """
        Update the regex as specified.

        :param id: id of regex to update
        :param name: Updated name of the regex (Optional)
        :param description: Updated description of the regex (Optional)
        :param pattern: Updated pattern of the regex (Optional)
        :return: Regex reference with more information id, owner, regex test sample statuses
        """
        req_body = {}
        if name is not None:
            req_body['name'] = name
        if description is not None:
            req_body['description'] = description
        if pattern is not None:
            req_body['pattern'] = pattern

        res = self.http_client.make_authed_request(
            self.service_uri + "/regexes/" + str(id),
            HttpMethod.PUT,
            req_body)

        if isinstance(res, DtlError):
            return res

        return Regex._from_payload(res)

    def share(self, regex_id: UUID, target_id: UUID, target_type: Scope, permission: Permission) -> Union[
        SharePermission, DtlError]:
        """
        Modify the sharing permission for the given regex. The change can be performed to user, group or organization with the desired permission (Share, Write or Read)
        In order to share, the user needs to have `Share` permission. Regex owners always have `Share` permission for that regex.

        :param regex_id: UUID is the id of the regex that you want to share
        :param target_id: UUID is the id of the User, Group or Organization you want to share with (depending on the target_type param)
        :param target_type: Scope (`Organization`, `Group` or `User`) with whom you want to share the regex. It can be Organization Group or User.
        :param permission: Permission (`Share`, `Write` or `Read`) the permission you want to grant
        :return: If successful returns the permission you granted specifying the `target_id` (UUID),
        the `target_type` (User, Group or Organization) and the `permission` level (Read, Write or Share) you just granted.
        (i.e. {target_id: str, target_type: str, permission: str}),
        else returns :class:`DtlError`.
        """

        url = f"/scout/regexes/{str(regex_id)}/shares?targetType={str(target_type.value)}&targetId={str(target_id)}&permission={str(permission.value)}"

        resp = self.http_client.execute_authed_request(url, HttpMethod.POST)

        if isinstance(resp, DtlError):
            return resp
        elif resp.status_code == 200:
            return SharePermission(object_type=ObjectType.Regex).from_payload(resp.json())
        else:
            return DtlError(resp.text)

    def search(self, name: Optional[str] = None,
               description: Optional[str] = None,
               test_data: Optional[str] = None,
               match: Optional[str] = None,
               owner: Optional[UUID] = None,
               page: int = 1, size: int = 25,
               order: SearchOrder = SearchOrder.created_at_desc) -> Union[List[Regex], DtlError]:
        """
        Search for a regex (full-text search), where defined (non-None) parameters/queries are the search criteria
        joint by AND operator and those not defined are ignored as search criteria.

        :param name: (Optional) Name of regex to be searched for (Optional)
        :param description: (Optional) Description of the regex to be searched for (Optional)
        :param test_data: (Optional) The textual test data of a regex to be searched for (Optional)
        :param match: (Optional) Text that can be pattern matched by the regex to be searched for (Optional)
        :param owner: (Optional) Regexes created by this particular owner
        :param page: The index of the page to get the regexes from. (Optional, defaults to first page index 1)
        :param size: Size per page. (Optional, defaults to 25)
        :param order: The order in which the regexes are sorted, please look into `SearchOrder` class for list of available options.
        Defaults to `("CreatedAt", "Desc")`
        :return: List of regex references
        """
        req_params = {}
        if name is not None:
            req_params['name'] = name
        if description is not None:
            req_params['description'] = description
        if test_data is not None:
            req_params['test_data'] = test_data
        if match is not None:
            req_params['match'] = match
        if owner is not None and isinstance(owner, UUID):
            req_params['owner'] = str(owner)
        if isinstance(page, int):
            req_params['page'] = page
        if isinstance(size, int):
            req_params['item_per_page'] = size
        req_params['sort'] = order.value[0]
        req_params['order'] = order.value[1]
        res = self.http_client.make_authed_request(
            self.service_uri + "/regexes",
            HttpMethod.GET,
            params=req_params)
        if isinstance(res, DtlError):
            return res

        return _parse_list(Regex._from_payload)(res)

    def test(self, id: UUID, data: List[str]) -> Union[List[RegexTestSample], DtlError]:
        """
        Test data against existing regex with given id

        :param id: id of existing regex
        :param data: List of string to verify against existing regex
        :return: data with corresponding statuses if regex with given id exists
        """
        res = self.http_client.make_authed_request(
            self.service_uri + "/regexes/" + str(id) + "/match",
            HttpMethod.PUT, data)
        if isinstance(res, DtlError):
            return res
        return _parse_list(RegexTestSample._from_payload)(res)

    def add_test_data(self, id: UUID, test_data: List[str]) -> Union[Regex, DtlError]:
        """
        Add test data to regex

        :param id: id of regex to update
        :param test_data: list of sentences which will be added as test sample
        :return: Regex reference with more information id, owner, regex test sample statuses
        """
        res = self.http_client.make_authed_request(
            self.service_uri + "/regexes/" + str(id) + "/test-data",
            HttpMethod.PUT, test_data)
        if isinstance(res, DtlError):
            return res

        return Regex._from_payload(res)

    def remove_test_data(self, id: UUID, test_data: List[str]) -> Union[Regex, DtlError]:
        """
        Remove test data from regex

        :param id: id of regex to update
        :param test_data: list of sentences which will be removed from test sample
        :return: Regex reference with more information id, owner, regex test sample statuses
        """
        res = self.http_client.make_authed_request(
            self.service_uri + "/regexes/" + str(id) + "/test-data",
            HttpMethod.DELETE, test_data)
        if isinstance(res, DtlError):
            return res

        return Regex._from_payload(res)

    def get(self, id: Union[str, UUID]) -> Union[DtlError, Regex]:
        """
        Retrieve a regex by its ID.
        :param regex_id: the id of the regex to be retrieved locally
        :return: the regex if successful, or a DtlError if failed
        """
        res = self.http_client.make_authed_request(
            self.service_uri + "/regexes/" + str(id),
            HttpMethod.GET)
        if isinstance(res, DtlError):
            return res

        return Regex._from_payload(res)

    def list(self, page: int = 1, item_per_page: int = 25) -> Union[DtlError, List[Regex]]:
        """
        List all regexes.

        :param page: page to be retrieved
        :param item_per_page: number of items to be put in a page
        :return: Returns a List of all the available regex if successful, or DtlError if failed
        """
        req_params = {}
        if isinstance(page, int):
            req_params['page'] = page
        if isinstance(item_per_page, int):
            req_params['item_per_page'] = item_per_page
        res = self.http_client.make_authed_request(
            self.service_uri + "/regexes",
            HttpMethod.GET,
            params=req_params)
        if isinstance(res, DtlError):
            return res

        return _parse_list(Regex._from_payload)(res)

    def delete(self, regex_id: Union[str, UUID]) -> Union[DtlError, bool]:
        """
        Delete a regex.

        :param regex_id: id of the regex to be deleted
        :return: True if successful, or DtlError if failed
        """

        resp = self.http_client.execute_authed_request(
            self.service_uri + "/regexes/" + str(regex_id),
            HttpMethod.DELETE)

        if isinstance(resp, DtlError):
            return resp
        elif resp.status_code == 200:
            return True
        else:
            return DtlError(resp.text)


class _ClassifierClient:
    """
    Client to interact with the Classifiers
    """

    def __init__(self, http_client: _HttpClient, ontology_client: _OntologyClient):
        self.http_client = http_client
        self.service_uri = "/scout"
        self.ontology_client = ontology_client

    def _fill_domain(self, classifier: Classifier, class_ids: List[str]):
        classifier.domain = []
        for class_id in class_ids:
            res = self.ontology_client.get_class(UUID(class_id))
            if isinstance(res, DtlError):
                res = OntologyNode(
                    name="Permission denied",
                    description="Permission denied",
                    id=UUID(class_id),
                )
            classifier.domain.append(res)

    def create(self, classifier: Classifier) -> Union[DtlError, Classifier]:
        """
        Creates the Classifier as specified.

        :param classifier: Classifier definition
        :return: Classifier reference with more information id, owner, description
        """
        res = self.http_client.make_authed_request(
            self.service_uri + "/classifiers",
            HttpMethod.POST,
            classifier._as_payload())

        if isinstance(res, DtlError):
            return res

        new_classifier = Classifier._from_payload(res)
        self._fill_domain(new_classifier, res.get("classIds"))
        return new_classifier

    def update(self,
               id: UUID,
               name: Optional[str] = None,
               description: Optional[str] = None,
               classification_methods: Optional[List[ClassificationMethod]] = None,
               default_class_id: Optional[UUID] = None) -> Union[
        DtlError, Classifier]:
        """
        Updates the Classifier as specified.

        :param id: id of classifier to update
        :param name: Updated name of the classifier (Optional)
        :param description: Updated description of the classifier (Optional)
        :param classification_methods: Updated classification_methods of the classifier (Optional)
        :param default_class_id: Updated default_class_id of the classifier. If empty string is provided, the default_class_id is set to None. (Optional)
        :return: Regex reference with more information id, owner, regex test sample statuses
        """

        req_body = {}
        if name is not None:
            req_body['name'] = name
        if description is not None:
            req_body['description'] = description
        if classification_methods is not None:
            req_body['classificationMethods'] = list(map(lambda m: m._as_payload(), classification_methods))
        if default_class_id is not None:
            if default_class_id == '' or is_valid_uuid(default_class_id):
                req_body['defaultClassId'] = str(default_class_id)
            else:
                raise DtlError(
                    "default_class_id can either be None, empty string, or in UUID format. Other formats are not allowed.")
            req_body['defaultClassId'] = str(default_class_id)

        res = self.http_client.make_authed_request(
            self.service_uri + "/classifiers/" + str(id),
            HttpMethod.PUT,
            req_body)

        updated_classifier = Classifier._from_payload(res)
        self._fill_domain(updated_classifier, res.get("classIds"))
        return updated_classifier

    def get(self, id: Union[str, UUID]) -> Union[DtlError, Classifier]:
        """
        Retrieve a classifier by its ID.
        :param id: the id of the classifier to be retrieved locally
        :return: the classifier if successful, or a DtlError if failed
        """
        res = self.http_client.make_authed_request(
            self.service_uri + "/classifiers/" + str(id),
            HttpMethod.GET)
        if isinstance(res, DtlError):
            return res

        new_classifier = Classifier._from_payload(res)
        self._fill_domain(new_classifier, res.get("classIds"))
        return new_classifier

    def delete(self, classifier_id: Union[str, UUID]) -> Union[DtlError, bool]:
        """
        Delete a classifier.

        :param classifier_id: id of the classifier to be deleted
        :return: True if successful, or DtlError if failed
        """

        res = self.http_client.make_authed_request(
            self.service_uri + "/classifiers/" + str(classifier_id),
            HttpMethod.DELETE)

        if isinstance(res, DtlError):
            return res

        return True

    def share(self, classifier_id: UUID, target_id: UUID, target_type: Scope, permission: Permission) -> Union[
        SharePermission, DtlError]:
        """
        Modify the sharing permission for the given classifier. The change can be performed to user, group or organization with the desired permission (Share, Write or Read)
        In order to share, the user needs to have `Share` permission. Classifiers owners always have `Share` permission for that classifier.

        :param classifier_id: UUID is the id of the classifier that you want to share
        :param target_id: UUID is the id of the User, Group or Organization you want to share with (depending on the target_type param)
        :param target_type: Scope (`Organization`, `Group` or `User`) with whom you want to share the classifier. It can be Organization Group or User.
        :param permission: Permission (`Share`, `Write` or `Read`) the permission you want to grant
        :return: If successful returns the permission you granted specifying the `target_id` (UUID),
        the `target_type` (User, Group or Organization) and the `permission` level (Read, Write or Share) you just granted.
        (i.e. {target_id: str, target_type: str, permission: str}),
        else returns :class:`DtlError`.
        """

        url = f"/classifiers/{str(classifier_id)}/shares?targetType={str(target_type.value)}&targetId={str(target_id)}&permission={str(permission.value)}"

        resp = self.http_client.execute_authed_request(self.service_uri + url, HttpMethod.POST)

        if isinstance(resp, DtlError):
            return resp
        elif resp.status_code == 200:
            return SharePermission(object_type=ObjectType.Classifier).from_payload(resp.json())
        else:
            return DtlError(resp.text)

    def list(self, page: int = 1, item_per_page: int = 25) -> Union[DtlError, List[Regex]]:
        """
        List all classifiers.

        :param page: page to be retrieved
        :param item_per_page: number of items to be put in a page
        :return: Returns a List of all the available classifiers if successful, or DtlError if failed
        """
        req_params = {}
        if isinstance(page, int):
            req_params['page'] = page
        if isinstance(item_per_page, int):
            req_params['size'] = item_per_page
        res = self.http_client.make_authed_request(
            self.service_uri + "/classifiers",
            HttpMethod.GET,
            params=req_params)
        if isinstance(res, DtlError):
            return res

        return _parse_list(Classifier._from_payload)(res)


class _PasswordClient():
    hardcoded_salt = b'\xc7H\x94\x80l\x9f\x8f\t'

    def generate_key(
            self,
            password: str,
            encryption_algorithm: EncryptionAlgorithm = EncryptionAlgorithm.AES_256
    ) -> Union[DtlError, str]:
        """
          Generate a key usable by an encryption algorithm based on a simple password

          :param password: a simple password that can be used to generate a key appropriate for encryption
          :param encryption_algorithm: the algorithm that will be used along with the encryption key
          :return: an encryption key as a string, if successful, or DtlError if failed
        """
        if not isinstance(password, str):
            return DtlError("Passwords need to be a string type!")
        if encryption_algorithm == EncryptionAlgorithm.AES_256:
            #Because we just want a mapping of password -> key, we use a hardcoded salt. Use of PBKDF2 is retained because of its useful password -> key generation.
            key = PBKDF2(password, self.hardcoded_salt).read(32)
            #We'll have to decode the bytestring in UTF-8,
            return b64encode(key).decode('utf-8')
        else:
            return DtlError("Encryption algorithm unknown")


    def generate_salt(
            self,
      password: str,
    ) -> Union[DtlError, str]:
      """
      Generate a hexadecimal string usable for salting by an hash algorithm based on a simple password

      :param password: a simple password that can be used to generate a hexadecimal string appropriate for salting a hash
      :return: a hexadecimal string, if successful, or DtlError if failed
      """
      if not isinstance(password, str):
          return DtlError("Passwords need to be a string type!")
      salt = pbkdf2_hmac('sha512', password.encode('utf-8'), self.hardcoded_salt, 100000)

      return salt.hex()


class _AutomationClient:
    """
    Client to interact with the Automations
    """

    def __init__(self, http_client: _HttpClient, ontology: _OntologyClient):
        self.http_client = http_client
        self.classifier = _ClassifierClient(http_client, ontology)
        self.regex = _RegexClient(http_client)
        self.password = _PasswordClient()
