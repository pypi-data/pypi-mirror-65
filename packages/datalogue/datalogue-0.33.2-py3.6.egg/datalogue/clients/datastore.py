from typing import List, Dict, Union, Optional, Set
from uuid import UUID
from pyarrow import csv, Table

from datalogue.clients.http import _HttpClient, HttpMethod, MultiPartData, MultiPartFile
from datalogue.models.schema import AbstractDataSchema, Schema, SchemaNode
from datalogue.models.datastore import Datastore, _datastore_from_payload, FileFormat, Cell, _cell_from_payload, NodeClassification
from datalogue.models.transformations.classify import Classifier
from datalogue.errors import DtlError
from datalogue.utils import _parse_list, ResponseStream
from datalogue.anduin.client import _AnduinClient
from datalogue.clients.ontology import _OntologyClient
from datalogue.anduin.models.stream import StreamStatus
from functools import reduce


class _DatastoreClient:
    """
    Client to interact with the Datastores objects
    """

    def __init__(self, http_client: _HttpClient):
        self.http_client = http_client
        self.service_uri = "/scout"

    def create(self, datastore: Datastore) -> Union[DtlError, Datastore]:
        """
        Creates a data source

        :param datastore: data source to be created
        :return: string with error message if failed, the data source otherwise
        """
        res = self.http_client.make_authed_request(
            self.service_uri + "/datastores", HttpMethod.POST, datastore._as_payload())

        if isinstance(res, DtlError):
            return res

        return _datastore_from_payload(res)

    def get(self, datastore_id: UUID) -> Union[DtlError, Datastore]:
        """
        From the provided id, get the corresponding Datastore

        :param datastore_id: id of the datastore to be retrieved
        :return:
        """

        res = self.http_client.make_authed_request(self.service_uri + "/datastores/" + str(datastore_id), HttpMethod.GET)

        if isinstance(res, DtlError):
            return res

        datastore_resp = _datastore_from_payload(res)
        if isinstance(datastore_resp, DtlError):
            return datastore_resp

        return self.__load_datastore_with_class_info(datastore_resp)

    def update(self, datastore: Datastore) -> Union[DtlError, Datastore]:
        """
        Updates the backend with the new status of the existing datastore

        :param datastore: to be persisted
        :return:
        """

        res = self.http_client.make_authed_request(
            self.service_uri + "/datastores/" + str(datastore.id),
            HttpMethod.PUT,
            datastore._as_payload()
        )

        if isinstance(res, DtlError):
            return res

        return _datastore_from_payload(res)

    def list(self, page: int = 1, item_per_page: int = 25) -> Union[DtlError, List[Datastore]]:
        """
        List all the datastores that are saved

        TODO pagination

        :param page: page to be retrieved (ignored)
        :param item_per_page: number of items to be put in a page (ignored)
        :return: Returns a List of all the available datastores or an error message as a string
        """

        res = self.http_client.make_authed_request(self.service_uri + "/datastores", HttpMethod.GET)

        if isinstance(res, DtlError):
            return res

        datastore_list = _parse_list(_datastore_from_payload)(res)
        if isinstance(datastore_list, DtlError):
            return datastore_list
        
        datastore_list_with_class_info = []
        for datastore_resp in datastore_list:
            datastore_resp_with_class_info = self.__load_datastore_with_class_info(datastore_resp)
            if isinstance(datastore_resp_with_class_info, DtlError):
                return datastore_resp_with_class_info
            datastore_list_with_class_info.append(datastore_resp_with_class_info)
        return datastore_list_with_class_info

    def search(self,
        names: List[str] = [],
        labels: List[str] = [],
        classes: List[str] = [],
        samples: List[str] = [],
        page: int = 1,
        item_per_page: int = 25)-> Union[DtlError, List[Datastore]]:
        """
        Search existing datastores for a given different fields. If nothing is defined for any field,
        it returns every datastore (basically matches all)

        :param names: a list of datastore names
        :param labels: a list of column labels
        :param classes: a list of classes that columns are classified
        :param samples: a list values that samples might contain
        :param page: page to be retrieved
        :param item_per_page: number of items to be put in a page
        :return: Returns a List of all the available datastores or an error message as a string
        """

        queries = {}

        if len(names) > 0:
            queries["name"] = names

        if len(labels) > 0:
            queries["schema.nodes.label"] = labels

        if len(classes) > 0:
            #TODO Should we consider userOntology?
            queries["schema.nodes.ontology.tag"] = classes

        if len(samples) > 0:
            queries["samples.nodes.value"] = samples

        if len(queries) > 0:
            payload = {
                "queries": queries,
                "page": page,
                "size": item_per_page,
                "type": "datastore"
            }

            res = self.http_client.make_authed_request(self.service_uri + "/v2/search", HttpMethod.POST, payload)
            if isinstance(res, DtlError):
                return res

            return _parse_list(_datastore_from_payload)(res)
        else:
            #If there is not query, we will bring everything
            payload = {
                "query": "*",
                "page": page,
                "size": item_per_page,
                "type": "datastore"
            }

            res = self.http_client.make_authed_request(self.service_uri + "/search", HttpMethod.POST, payload)
            return _parse_list(_datastore_from_payload)(res)

    def get_schema(self, datastore_id: UUID) -> Union[DtlError, AbstractDataSchema]:
        """
        From the provided id, get the corresponding Datastore schema

        :param datastore_id: id of the datastore to be retrieved
        :return:
        """
        res = self.http_client.make_authed_request(self.service_uri + "/datastores/" + str(datastore_id) + "/schema", HttpMethod.GET)
        if isinstance(res, DtlError):
            return res

        schema = Schema._from_payload(res).data_schema
        if isinstance(schema, DtlError):
            return schema

        schema = self.__load_ads_with_class_info(schema)
        return schema

    def __load_datastore_with_class_info(self, datastore: Datastore) -> Union[DtlError, Datastore]:
        if datastore.ads is None and (datastore.schema_nodes is None or len(datastore.schema_nodes) is 0):
            return datastore

        if datastore.ads is not None or datastore.schema_nodes is not None:
            # 1. Get schema nodes from either Datastore or from ADS
            schema_nodes = []
            if datastore.schema_nodes is not None:
                schema_nodes = datastore.schema_nodes
            elif datastore.ads is not None: 
                schema_nodes = list(map(lambda node_def: node_def.node, datastore.ads.get_nodes()))

            # 2. Load the dictionary for set of class_id
            class_id_path_dict =  self.__load_paths_of_class_ids(schema_nodes)
            if isinstance(class_id_path_dict, DtlError):
                return class_id_path_dict

            # 3. Update ADS and List of SchemaNode respectively
            if datastore.ads is not None:
                datastore.ads = self.__fill_ads(datastore.ads, class_id_path_dict)
            
            if datastore.schema_nodes is not None:
                datastore.schema_nodes = self.__fill_schema_nodes(datastore.schema_nodes, class_id_path_dict)

            if datastore.schema_classes is not None:
                for schema_class in datastore.schema_classes:
                    class_path = class_id_path_dict.get(schema_class.class_id)
                    if class_path is None:
                        # There is no class or user does not have Read permissions
                        schema_class.class_name = "Permission denied"
                        schema_class.class_path = ["Permission denied"]
                    elif len(class_path) > 0:
                        schema_class.class_name = class_path[-1]
                        schema_class.class_path = class_path
                    else:
                        schema_class.class_path = class_path

        return datastore

    def __load_ads_with_class_info(self, schema: AbstractDataSchema) -> Union[DtlError, AbstractDataSchema]:
        schema_nodes = list(map(lambda node_def: node_def.node, schema.get_nodes()))
        class_id_path_dict = self.__load_paths_of_class_ids(schema_nodes)

        if isinstance(class_id_path_dict, DtlError):
            return class_id_path_dict

        return self.__fill_ads(schema, class_id_path_dict)

    def __fill_ads(self, schema: AbstractDataSchema, class_id_path_dict: Dict[UUID, List[str]]) -> Union[DtlError, AbstractDataSchema]:
        schema_nodes = list(map(lambda node_def: node_def.node, schema.get_nodes()))
        for schema_node in schema_nodes:
            classifications = schema_node.classifications
            for classification in classifications:
                class_path = class_id_path_dict.get(classification.class_id)
                if class_path is None:
                    # There is no class or user does not have Read permissions
                    classification.class_name = "Permission denied"
                    classification.class_path = ["Permission denied"]
                elif len(class_path) > 0:
                    classification.class_name = class_path[-1]
                    classification.class_path = class_path
                else:
                    classification.class_path = class_path

        return schema

    def __load_schema_nodes_with_class_info(self, schema_nodes: List[SchemaNode]) -> Union[DtlError, List[SchemaNode]]:
        class_id_path_dict = self.__load_paths_of_class_ids(schema_nodes)
        return self.__fill_schema_nodes(schema_nodes, class_id_path_dict)

    def __fill_schema_nodes(self, schema_nodes: List[SchemaNode], class_id_path_dict: Dict[UUID, List[str]]) -> Union[DtlError, List[SchemaNode]]:        
        for schema_node in schema_nodes:
            classifications = schema_node.classifications
            for classification in classifications:
                class_path = class_id_path_dict.get(classification.class_id)
                if class_path is None:
                    # There is no class or user does not have Read permissions
                    classification.class_name = "Permission denied"
                    classification.class_path = ["Permission denied"]
                elif len(class_path) > 0:
                    classification.class_name = class_path[-1]
                    classification.class_path = class_path
                else:
                    classification.class_path = class_path
        return schema_nodes

    def __load_paths_of_class_ids(self, schema_nodes: List[SchemaNode]) -> Union[DtlError, Dict[str, List[str]]]:
        class_id_set = set([])
        for schema_node in schema_nodes:
            classifications = schema_node.classifications
            for classification in classifications:
                class_id_set.add(classification.class_id)

        res = []
        if len(class_id_set) > 0:
            res = self.http_client.make_authed_request(
                f'/yggy/entities?page=1&size={len(class_id_set)}',
                HttpMethod.PUT,
                list(map(lambda x: str(x), class_id_set)))

            if isinstance(res, DtlError):
                return res

        class_id_path_dict = {}
        for classInfo in res:
            class_id = UUID(classInfo["id"])
            class_path = classInfo["path"]
            class_id_path_dict[class_id] = class_path

        return class_id_path_dict

    def print(self, datastore_id: UUID, full_path: bool = False) -> Union[DtlError, None]:
        """
        TEMPORARILY DISABLED.
        From the provided id, get the corresponding Datastore schema

        :param datastore_id: id of the datastore to be retrieved
        :return:
        """
        print("Feature currently disabled, please contact Datalogue.")
        # res = self.http_client.make_authed_request(self.service_uri + "/datastores/" + str(datastore_id) + "/schema", HttpMethod.GET)
        # if isinstance(res, DtlError):
        #     if res.message.__contains__("Route not found"):
        #         res.message = "Invalid ID, please verify that your data store exists with dtl.datastore.list()"
        #     return res
        # schema = Schema._from_payload(res)
        # schema.print(full_path)

    def delete(self, datastore_id: UUID) -> Union[DtlError, bool]:
        """
        Deletes the given Datastore

        :param datastore_id: id of the datastore to be deleted
        :return: true if successful, false otherwise
        """

        res = self.http_client.make_authed_request(
            self.service_uri + "/datastores/" + str(datastore_id), HttpMethod.DELETE)

        if isinstance(res, DtlError):
            return res
        else:
            return True

    def download(self, datastore_id: UUID, file_format: FileFormat, path: str, limit: Optional[int] = None) -> Union[DtlError, str]:
        """
        Downloads the resource in a file

        :param datastore_id: id of the resource to download
        :param file_format: File format of the downloaded resource
        :param path: location to save the file
        :param limit: limit the number of elements to be downloaded
        :return: An error or the path to the downloaded file
        """

        params = {
            "fileFormat": file_format.value,
        }

        if limit is not None:
            if not isinstance(limit, int) or limit < 0:
                return DtlError("limit should be a positive integer")

            params["limit"] = limit

        res = self.http_client.make_authed_request(
            self.service_uri + "/datastores/" + str(datastore_id) + "/download",
            HttpMethod.GET, params=params, stream=True
        )

        if isinstance(res, DtlError):
            return res

        with open(path, 'wb') as f:
            for chunk in res.iter_content(chunk_size=1024 * 32):
                if chunk:  # filter out keep-alive new chunks
                    f.write(chunk)

        return path

    def load_arrow_table(self, datastore_id: UUID, limit: Optional[int] = None, batch_size: int = 1024) -> \
            Union[DtlError, Table]:
        """
        Loads the resource in an in memory arrow buffer.
        This can be used either with Nvidia RAPIDS or pandas

        pandas:
        df = dtl.client.datastore.load_arrow_table(datastore_id).to_pandas()

        :param datastore_id: if of the resource to load
        :param limit: elements to be loaded in the frame
        :param batch_size: size of the batch to be retrieved at a time from the collection
        :return:
        """

        params = {
            "fileFormat": FileFormat.Csv.value
        }

        if limit is not None:
            if not isinstance(limit, int) or limit < 0:
                return DtlError("limit should be a positive integer")

            params["limit"] = limit

        res = self.http_client.make_authed_request(
            self.service_uri + "/datastores/" + str(datastore_id) + "/download",
            HttpMethod.GET, params=params, stream=True
        )

        if isinstance(res, DtlError):
            return res

        stream = ResponseStream(res.iter_content(batch_size))

        return csv.read_csv(stream)

    def upload(self, datastore_id: UUID, file_format: FileFormat, path: str, params: dict = {}) -> Union[DtlError, None]:
        """
        Enable to upload a file to the specified resource through the platform

        :param datastore_id: id of the resource to upload the data through
        :param file_format: format of the file to be uploaded
        :param path: location of the file to upload on disk
        :return:
        """

        with open(path, 'rb') as f:
            files = [MultiPartFile("content", f)]

            data = [
                MultiPartData("file-format", file_format.value),
                MultiPartData("params", "{}"),
            ]

            res = self.http_client.post_multipart_data(
                self.service_uri + "/datastores/" + str(datastore_id) + "/upload",
                files, data
            )

            if isinstance(res, DtlError):
                return res
    
    def classify_fields(self, datastore_id: UUID, classifier_id: Union[str, UUID]) -> Union[DtlError, UUID]:
        """
        Classify the fields of a datastore. Classifications will be found within the ‘classifications’ property of
         each SchemaNode of the datastore.

        :param datastore_id: the id of the datastore to classify the fields of
        :param classifier: the classifier to apply classes to the data points, which will be used to calculate the
         classes of the fields
        :return: the job id of the pipeline classifying the datastore fields
        """

        req_params = {}
        req_params['classifier'] = str(classifier_id)
        res = self.http_client.make_authed_request(
            self.service_uri + "/datastores/" + str(datastore_id) + "/classify",
            HttpMethod.POST,
            params=req_params)

        if isinstance(res, DtlError):
            return res

        return UUID(res["jobId"])

    def add_classifications(self, datastore_id: UUID, classifications: List[NodeClassification]) -> Union[DtlError, List[SchemaNode]]:
        """
        Apply classes to specified fields (append, not override)

        :param datastore_id: the id of the datastore to add classes to
        :param classifications: a list of NodeClassifications, representing the fields to add classes to, and the classes to add
        :return: a list of altered SchemaNodes if successful, or DtlError if failed
        """

        res = self.http_client.make_authed_request(
                self.service_uri + "/datastores/" + str(datastore_id)+ "/classifications/add",
                HttpMethod.PUT,
                list(map(lambda x: x._as_payload(), classifications)))

        if isinstance(res, DtlError):
            return res

        updated_schema_nodes = _parse_list(SchemaNode._schema_node_from_payload)(res)
        if isinstance(updated_schema_nodes, DtlError):
            return updated_schema_nodes

        return self.__load_schema_nodes_with_class_info(updated_schema_nodes)

    def remove_classifications(self, datastore_id: UUID, classifications: List[NodeClassification]) -> Union[DtlError, List[SchemaNode]]:
        """
        Remove classes from specified fields.

        :param datastore_id: the id of the datastore to remove classes from
        :param classifications: a list of NodeClassifications, representing the fields from which classes should be removed, and the classes  to remove from those fields
        :return: a list of altered SchemaNodes if successful, or DtlError if failed
        """

        res = self.http_client.make_authed_request(
                self.service_uri + "/datastores/" + str(datastore_id)+ "/classifications/remove",
                HttpMethod.PUT,
                list(map(lambda x: x._as_payload(), classifications)))

        if isinstance(res, DtlError):
            return res

        updated_schema_nodes = _parse_list(SchemaNode._schema_node_from_payload)(res)
        if isinstance(updated_schema_nodes, DtlError):
            return updated_schema_nodes

        return self.__load_schema_nodes_with_class_info(updated_schema_nodes)

    def override_classifications(self, datastore_id: UUID, classifications: List[NodeClassification]) -> Union[DtlError, List[SchemaNode]]:
        """
        Remove all classes from specified fields, and then apply new classes to those fields.

        :param datastore_id: the id of the datastore whose fields should be overridden
        :param classifications: a list of NodeClassifications, representing the fields that should be cleared and the new classes for  those fields
        :return: a list of altered SchemaNodes if successful, or DtlError if failed
        """

        res = self.http_client.make_authed_request(
                self.service_uri + "/datastores/" + str(datastore_id)+ "/classifications/replace",
                HttpMethod.PUT,
                list(map(lambda x: x._as_payload(), classifications)))

        if isinstance(res, DtlError):
            return res

        updated_schema_nodes = _parse_list(SchemaNode._schema_node_from_payload)(res)
        if isinstance(updated_schema_nodes, DtlError):
            return updated_schema_nodes

        return self.__load_schema_nodes_with_class_info(updated_schema_nodes)