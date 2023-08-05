import datetime
import os
from urllib.parse import urlparse
import logging

import grpc
from grpc._cython import cygrpc

from ..grpc_gen import milvus_pb2_grpc
from ..grpc_gen import milvus_pb2 as grpc_types
from .abstract import ConnectIntf, CollectionSchema, IndexParam, PartitionParam, TopKQueryResult, TableInfo
from .prepare import Prepare
from .types import MetricType, Status
from .check import (
    int_or_str,
    is_legal_host,
    is_legal_port,
)

from .hooks import BaseSearchHook
from .client_hooks import SearchHook
from .exceptions import ParamError, NotConnectError
from ..settings import DefaultConfig as config
from . import __version__

LOGGER = logging.getLogger(__name__)


class GrpcHandler(ConnectIntf):
    def __init__(self, host=None, port=None, **kwargs):
        self._channel = None
        self._stub = None
        self._uri = None
        self.status = None

        # client hook
        self._search_hook = SearchHook()
        self._search_file_hook = SearchHook()

        # set server uri if object is initialized with parameter
        _uri = kwargs.get("uri", None)
        self._uri = (host or port or _uri) and self._set_uri(host, port, uri=_uri)

    def __str__(self):
        attr_list = ['%s=%r' % (key, value)
                     for key, value in self.__dict__.items() if not key.startswith('_')]
        return '<Milvus: {}>'.format(', '.join(attr_list))

    def __enter__(self):
        self._setup()

        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        del self._channel
        del self._stub

    def _setup(self):
        """
        Create a grpc channel and a stub

        :raises: NotConnectError

        """

        if not self._channel:
            self._set_channel()

        try:
            # check if server is ready
            ft = grpc.channel_ready_future(self._channel)
            ft.result(timeout=1)
            ft.__del__()
        except grpc.FutureTimeoutError:
            del self._channel
            raise NotConnectError('Fail connecting to server on {}. Timeout'.format(self._uri))
        except grpc.RpcError as e:
            del self._channel
            raise NotConnectError("Connect error: <{}>".format(e))
        # Unexpected error
        except Exception as e:
            raise NotConnectError("Error occurred when trying to connect server:\n"
                                  "\t<{}>".format(str(e)))

        self._stub = milvus_pb2_grpc.MilvusServiceStub(self._channel)
        self.status = Status()

    def _set_uri(self, host, port, **kwargs):
        """
        Set server network address

        :raises: ParamError

        """
        if host is not None:
            _port = port if port is not None else config.GRPC_PORT
            _host = host
        elif port is None:
            try:
                _uri = kwargs.get("uri", None)
                # Ignore uri check here
                # if not is_legal_uri(_uri):
                #     raise ParamError("uri {} is illegal".format(_uri))
                #
                # If uri is empty (None or '') use default uri instead
                # (the behavior may change in the future)
                # _uri = urlparse(_uri) if _uri is not None else urlparse(config.GRPC_URI)
                _uri = urlparse(_uri) if _uri else urlparse(config.GRPC_URI)
                _host = _uri.hostname
                _port = _uri.port
            except (AttributeError, ValueError, TypeError) as e:
                raise ParamError("uri is illegal: {}".format(e))
        else:
            raise ParamError("Param is not complete. Please invoke as follow:\n"
                             "\t(host = ${HOST}, port = ${PORT})\n"
                             "\t(uri = ${URI})\n")

        if not is_legal_host(_host) or not is_legal_port(_port):
            raise ParamError("host or port is illeagl")

        return "{}:{}".format(str(_host), str(_port))

    def _set_channel(self):
        """
        Set grpc channel. Use default server uri if uri is not set.
        """
        if self._channel:
            del self._channel

        # set transport unlimited
        self._channel = grpc.insecure_channel(
            self._uri,
            # self._uri or config.GRPC_ADDRESS,
            options=[(cygrpc.ChannelArgKey.max_send_message_length, -1),
                     (cygrpc.ChannelArgKey.max_receive_message_length, -1)]
        )

    def set_hook(self, **kwargs):
        """
        specify client hooks.
        The client hooks are used in methods which interact with server.
        Use key-value method to set hooks. Supported hook setting currently is as follow.

            search hook,
            search-in-file hook

        """

        # config search hook
        _search_hook = kwargs.get('search', None)
        if _search_hook:
            if not isinstance(_search_hook, BaseSearchHook):
                raise ParamError("search hook must be a subclass of `BaseSearchHook`")

            self._search_hook = _search_hook

        _search_file_hook = kwargs.get('search_in_file', None)
        if _search_file_hook:
            if not isinstance(_search_file_hook, BaseSearchHook):
                raise ParamError("search hook must be a subclass of `BaseSearchHook`")

            self._search_file_hook = _search_file_hook

    @property
    def server_address(self):
        """
        Server network address
        """
        return self._uri

    def connect(self, host=None, port=None, uri=None, timeout=1):

        """
        Connect method should be called before any operations.
        Server will be connected after connect return OK

        :type  host: str
        :type  port: str
        :type  uri: str
        :type  timeout: float
        :param host: (Optional) host of the server, default host is 127.0.0.1
        :param port: (Optional) port of the server, default port is 19530
        :param uri: (Optional) only support tcp proto now, default uri is

                `tcp://127.0.0.1:19530`

        :param timeout: (Optional) connection timeout, default timeout is 3000ms

        :return: Status, indicate if connect is successful
        :rtype: Status
        
        :raises: NotConnectError
        """
        if self.connected():
            return Status(message="You have already connected {} !".format(self._uri),
                          code=Status.CONNECT_FAILED)

        # TODO: Here may cause bug: IF user has already connected a server but server is down,
        # client may connect to a new server. It's a undesirable behavior.

        if (host or port or uri) or not self._uri:
            # if self._uri and self._uri != self._set_uri(host, port, uri=uri):
            #     return Status(message="The server address is set as {}, "
            #                           "you cannot connect other server".format(self._uri),
            #                   code=Status.CONNECT_FAILED)
            self._uri = self._set_uri(host, port, uri=uri)

        if self._channel:
            del self._channel
            self._channel = None

        self._set_channel()

        try:
            # check if server is ready
            ft = grpc.channel_ready_future(self._channel)
            ft.result(timeout=timeout)
            ft.__del__()
        except grpc.FutureTimeoutError:
            del self._channel
            self._channel = None
            raise NotConnectError('Fail connecting to server on {}. Timeout'.format(self._uri))
        except grpc.RpcError as e:
            del self._channel
            self._channel = None
            raise NotConnectError("Connect error: <{}>".format(e))
        # Unexpected error
        except Exception as e:
            raise NotConnectError("Error occurred when trying to connect server:\n"
                                  "\t<{}>".format(str(e)))

        self._stub = milvus_pb2_grpc.MilvusServiceStub(self._channel)
        self.status = Status()
        return self.status

    def connected(self):
        """
        Check if client is connected to the server

        :return: if client is connected
        :rtype: bool
        """
        if not self._stub or not self._channel:
            return False
        try:
            ft = grpc.channel_ready_future(self._channel)
            ft.result(timeout=2)
            ft.__del__()
            return True
        except (grpc.FutureTimeoutError, grpc.RpcError):
            return False

    def disconnect(self):
        """
        Disconnect with the server and distroy the channel

        :return: Status, indicate if disconnect is successful
        :rtype: Status
        """
        # After closeing, a exception stack trace is printed from a background thread and
        # no exception is thrown in the main thread, issue is under test and not done yet
        # checkout https://github.com/grpc/grpc/issues/18995
        # Also checkout Properly Specify Channel.close Behavior in Python:
        # https://github.com/grpc/grpc/issues/19235
        if not self.connected():
            raise NotConnectError('Please connect to the server first!')

        # closing channel by calling interface close() will result in grpc interval error
        self._channel.__del__()

        # try:
        #     self._channel.close()
        # except Exception as e:
        #     LOGGER.error(e)
        #     return Status(code=Status.CONNECT_FAILED, message='Disconnection failed')

        self.status = None
        self._channel = None
        self._stub = None

        return Status(message='Disconnect successfully')

    def server_version(self, timeout=10):
        """
        Provide server version

        :return:
            Status: indicate if operation is successful

            str : Server version

        :rtype: (Status, str)
        """
        return self._cmd(cmd='version', timeout=timeout)

    def server_status(self, timeout=10):
        """
        Provide server status

        :return:
            Status: indicate if operation is successful

            str : Server version

        :rtype: (Status, str)
        """
        return self._cmd(cmd='status', timeout=timeout)

    def _cmd(self, cmd, timeout=10):
        cmd = Prepare.cmd(cmd)
        try:
            rf = self._stub.Cmd.future(cmd)
            response = rf.result(timeout=timeout)
            rf.__del__()
            if response.status.error_code == 0:
                return Status(message='Success!'), response.string_reply

            return Status(code=response.status.error_code, message=response.status.reason), None
        except grpc.FutureTimeoutError as e:
            LOGGER.error(e)
            return Status(Status.UNEXPECTED_ERROR, message='Request timeout'), None
        except grpc.RpcError as e:
            LOGGER.error(e)
            return Status(e.code(), message='Error occurred. {}'.format(e.details())), None

    def create_table(self, table_name, dimension, index_file_size, metric_type, param, timeout=10):
        """
        Create table

        :type  param: dict or TableSchema
        :param param: Provide table information to be created

                `example param={'table_name': 'name',
                                'dimension': 16,
                                'index_file_size': 1024 (default)，
                                'metric_type': Metric_type.L2 (default)
                                }`

                `OR using Prepare.table_schema to create param`

        :param timeout: timeout, The unit is seconds
        :type  timeout: double

        :return: Status, indicate if operation is successful
        :rtype: Status
        """

        table_schema = Prepare.table_schema(table_name, dimension, index_file_size, metric_type, param)

        try:
            rf = self._stub.CreateTable.future(table_schema)
            status = rf.result(timeout=timeout)
            rf.__del__()
            # status = self._stub.CreateTable.future(table_schema).result(timeout=timeout)
            if status.error_code == 0:
                return Status(message='Create collection successfully!')

            LOGGER.error(status)
            return Status(code=status.error_code, message=status.reason)
        except grpc.FutureTimeoutError as e:
            LOGGER.error(e)
            return Status(Status.UNEXPECTED_ERROR, message='Request timeout')
        except grpc.RpcError as e:
            LOGGER.error(e)
            return Status(e.code(), message='Error occurred: {}'.format(e.details()))

    def has_table(self, table_name, timeout=10):
        """

        This method is used to test table existence.

        :param table_name: table name is going to be tested.
        :type  table_name: str
        :param timeout: time waiting for server response
        :type  timeout: int

        :return:
            Status: indicate if vectors inserted successfully
            bool if given table_name exists

        """

        table_name = Prepare.table_name(table_name)

        try:
            rf = self._stub.HasTable.future(table_name)
            reply = rf.result(timeout=timeout)
            rf.__del__()
            # reply = self._stub.HasTable.future(table_name).result(timeout=timeout)
            if reply.status.error_code == 0:
                return Status(), reply.bool_reply

            return Status(code=reply.status.error_code,
                          message=reply.status.reason), False
        except grpc.FutureTimeoutError as e:
            LOGGER.error(e)
            return Status(code=Status.UNEXPECTED_ERROR, message="request timeout"), False
        except grpc.RpcError as e:
            LOGGER.error(e)
            return Status(code=e.code(), message=e.details()), False

    def describe_table(self, table_name, timeout=10):
        """
        Show table information

        :type  table_name: str
        :param table_name: which table to be shown

        :returns: (Status, table_schema)
            Status: indicate if query is successful
            table_schema: return when operation is successful
        :rtype: (Status, TableSchema)
        """

        table_name = Prepare.table_name(table_name)

        try:
            rf = self._stub.DescribeTable.future(table_name)
            response = rf.result(timeout=timeout)
            rf.__del__()

            if response.status.error_code == 0:
                table = CollectionSchema(
                    collection_name=response.table_name,
                    dimension=response.dimension,
                    index_file_size=response.index_file_size,
                    metric_type=MetricType(response.metric_type)
                )

                return Status(message='Describe table successfully!'), table

            LOGGER.error(response.status)
            return Status(code=response.status.error_code, message=response.status.reason), None

        except grpc.FutureTimeoutError as e:
            LOGGER.error(e)
            return Status(Status.UNEXPECTED_ERROR, message='Request timeout'), None
        except grpc.RpcError as e:
            LOGGER.error(e)
            return Status(e.code(), message='Error occurred. {}'.format(e.details())), None

    def count_table(self, table_name, timeout=30):
        """
        obtain vector number in table

        :type  table_name: str
        :param table_name: target table name.

        :returns:
            Status: indicate if operation is successful

            res: int, table row count
        """

        table_name = Prepare.table_name(table_name)

        try:
            rf = self._stub.CountTable.future(table_name)
            response = rf.result(timeout=timeout)
            rf.__del__()
            # response = self._stub.CountTable.future(table_name).result(timeout=timeout)
            if response.status.error_code == 0:
                return Status(message='Success!'), response.table_row_count

            return Status(code=response.status.error_code, message=response.status.reason), None
        except grpc.FutureTimeoutError as e:
            LOGGER.error(e)
            return Status(Status.UNEXPECTED_ERROR, message='Request timeout'), None
        except grpc.RpcError as e:
            LOGGER.error(e)
            return Status(e.code(), message='Error occurred. {}'.format(e.details())), None

    def show_tables(self, timeout=10):
        """
        Show all tables information in database

        :return:
            Status: indicate if this operation is successful

            tables: list of table names, return when operation
                    is successful
        :rtype:
            (Status, list[str])
        """

        cmd = Prepare.cmd('show_tables')
        try:
            rf = self._stub.ShowTables.future(cmd)
            response = rf.result(timeout=timeout)
            rf.__del__()
            if response.status.error_code == 0:
                return Status(message='Show tables successfully!'), \
                       [name for name in response.table_names if len(name) > 0]
            return Status(response.status.error_code, message=response.status.reason), []
        except grpc.FutureTimeoutError:
            return Status(Status.UNEXPECTED_ERROR, message="Request timeout"), []
        except grpc.RpcError as e:
            LOGGER.error(e)
            return Status(e.code(), message='Error occurred. {}'.format(e.details())), []

    def show_table_info(self, table_name, timeout=10):
        request = grpc_types.TableName(table_name=table_name)

        try:
            rf = self._stub.ShowTableInfo.future(request)
            response = rf.result(timeout=timeout)
            rf.__del__()
            rpc_status = response.status

            if rpc_status.error_code == 0:
                return Status(), TableInfo(response)

            return Status(rpc_status.error_code, rpc_status.reason), None
        except grpc.FutureTimeoutError:
            return Status(Status.UNEXPECTED_ERROR, message="Request timeout"), None
        except grpc.RpcError as e:
            return Status(Status.UNEXPECTED_ERROR, e.details()), None

    def preload_table(self, table_name, timeout=None):
        """
        Load table to cache in advance

        :type table_name: str
        :param table_name: table to preload

        :returns:
            Status:  indicate if invoke is successful
        """

        table_name = Prepare.table_name(table_name)

        try:
            rf = self._stub.PreloadTable.future(table_name)
            status = rf.result(timeout=timeout)
            rf.__del__()
            return Status(code=status.error_code, message=status.reason)
        except grpc.FutureTimeoutError as e:
            LOGGER.error(e)
            return Status(Status.UNEXPECTED_ERROR, message='Request timeout')
        except grpc.RpcError as e:
            return Status(code=e.code(), message='Error occurred. {}'.format(e.details()))

    def drop_table(self, table_name, timeout=20):
        """
        Delete table with table_name

        :type  table_name: str
        :param table_name: Name of the table being deleted

        :return: Status, indicate if operation is successful
        :rtype: Status
        """

        table_name = Prepare.table_name(table_name)

        try:
            rf = self._stub.DropTable.future(table_name)
            status = rf.result(timeout=timeout)
            rf.__del__()
            if status.error_code == 0:
                return Status(message='Delete collection successfully!')
            return Status(code=status.error_code, message=status.reason)
        except grpc.FutureTimeoutError as e:
            LOGGER.error(e)
            return Status(Status.UNEXPECTED_ERROR, message='Request timeout')
        except grpc.RpcError as e:
            LOGGER.error(e)
            return Status(e.code(), message='Error occurred: {}'.format(e.details()))

    def insert(self, table_name, records, ids=None, partition_tag=None, params=None, timeout=None, **kwargs):
        """
        Add vectors to table

        :param ids: list of id
        :type  ids: list[int]

        :type  table_name: str
        :param table_name: table name been inserted

        :type  records: list[list[float]]

                `example records: [[1.2345],[1.2345]]`

                `OR using Prepare.records`

        :param records: list of vectors been inserted

        :type partition_tag: str or None.
            If partition_tag is None, vectors will be inserted into table rather than partitions.

        :param partition_tag: the tag string of table

        :type

        :type  timeout: int
        :param timeout: time waiting for server response

        :returns:
            Status: indicate if vectors inserted successfully
            ids: list of id, after inserted every vector is given a id
        :rtype: (Status, list(int))
        """
        insert_param = kwargs.get('insert_param', None)

        if insert_param and not isinstance(insert_param, grpc_types.InsertParam):
            raise ParamError("The value of key 'insert_param' is invalid")

        body = insert_param if insert_param \
            else Prepare.insert_param(table_name, records, partition_tag, ids, params)

        try:
            rf = self._stub.Insert.future(body)
            response = rf.result(timeout=timeout)
            rf.__del__()

            if response.status.error_code == 0:
                return Status(message='Add vectors successfully!'), list(response.vector_id_array)

            return Status(code=response.status.error_code, message=response.status.reason), []
        except grpc.RpcError as e:
            LOGGER.error(e)
            return Status(e.code(), message='Error occurred. {}'.format(e.details())), []
        except grpc.FutureTimeoutError as e:
            LOGGER.error(e)
            return Status(code=Status.UNEXPECTED_ERROR, message="Request timeout"), []

    def get_vector_by_id(self, table_name, v_id, timeout=10):
        request = grpc_types.VectorIdentity(table_name=table_name, id=v_id)

        try:
            rf = self._stub.GetVectorByID.future(request)
            response = rf.result(timeout=timeout)
            rf.__del__()
            status = response.status
            if status.error_code == 0:
                status = Status(message="Obtain vector successfully")
                return status, \
                       list(response.vector_data.float_data) or bytes(response.vector_data.binary_data)

            return Status(code=status.error_code, message=status.reason), []
        except grpc.FutureTimeoutError as e:
            LOGGER.error(e)
            return Status(Status.UNEXPECTED_ERROR, message='Request timeout'), []
        except grpc.RpcError as e:
            LOGGER.error(e)
            return Status(e.code(), message='Error occurred: {}'.format(e.details())), []

    def get_vector_ids(self, table_name, segment_name, timeout=10):
        request = grpc_types.GetVectorIDsParam(table_name=table_name, segment_name=segment_name)

        try:
            rf = self._stub.GetVectorIDs.future(request)
            response = rf.result(timeout=timeout)
            rf.__del__()

            if response.status.error_code == 0:
                vec = list(response.vector_id_array)
                return Status(), vec
            return Status(response.status.error_code, response.status.reason), []
        except grpc.FutureTimeoutError as e:
            LOGGER.error(e)
            return Status(Status.UNEXPECTED_ERROR, message="Request timeout"), []
        except grpc.RpcError as e:
            LOGGER.error(e)
            return Status(e.code(), message="Error occurred: {}".format(e.details())), []

    def create_index(self, table_name, index_type=None, params=None, timeout=None):
        """
        build vectors of specific table and create vector index

        :param table_name: table used to crete index.
        :type table_name: str
        :param index: index params
        :type index: dict

            index_param can be None

            `example (default) param={'index_type': IndexType.FLAT,
                            'nlist': 16384}`

        :param timeout: grpc request timeout.

            if `timeout` = -1, method invoke a synchronous call, waiting util grpc response
            else method invoke a asynchronous call, timeout work here

        :type  timeout: int

        :return: Status, indicate if operation is successful
        """
        index_param = Prepare.index_param(table_name, index_type, params)
        try:
            # status = self._stub.CreateIndex.future(index_param).result(timeout=timeout)
            status = self._stub.CreateIndex(index_param)

            if status.error_code == 0:
                return Status(message='Build index successfully!')

            return Status(code=status.error_code, message=status.reason)
        except grpc.FutureTimeoutError as e:
            LOGGER.error("| Client | gRPC Timeout Error:" + str(e))
            return Status(Status.UNEXPECTED_ERROR, message='Request timeout')
        except grpc.RpcError as e:
            LOGGER.error("| Client | gRPC RPC Error:" + str(e))
            return Status(e.code(), message='Error occurred. {}'.format(e.details()))

    def describe_index(self, table_name, timeout=10):
        """
        Show index information of designated table

        :type table_name: str
        :param table_name: table name been queried

        :returns:
            Status:  indicate if query is successful
            IndexSchema:

        """

        table_name = Prepare.table_name(table_name)

        try:
            rf = self._stub.DescribeIndex.future(table_name)
            index_param = rf.result(timeout=timeout)
            rf.__del__()

            status = index_param.status

            if status.error_code == 0:
                return Status(message="Successfully"), \
                       IndexParam(index_param.table_name,
                                  index_param.index_type,
                                  index_param.extra_params)

            return Status(code=status.error_code, message=status.reason), None
        except grpc.FutureTimeoutError as e:
            LOGGER.error(e)
            return Status(code=Status.UNEXPECTED_ERROR, message='Request timeout'), None
        except grpc.RpcError as e:
            LOGGER.error(e)
            return Status(e.code(), message='Error occurred. {}'.format(e.details())), None

    def drop_index(self, table_name, timeout=10):
        """
        drop index from index file

        :param table_name: target table name.
        :type table_name: str

        :return:
            Status: indicate if operation is successful

        ：:rtype: Status
        """

        table_name = Prepare.table_name(table_name)
        try:
            rf = self._stub.DropIndex.future(table_name)
            status = rf.result(timeout=timeout)
            rf.__del__()
            # status = self._stub.DropIndex.future(table_name).result(timeout=timeout)
            return Status(code=status.error_code, message=status.reason)
        except grpc.FutureTimeoutError as e:
            LOGGER.error(e)
            return Status(Status.UNEXPECTED_ERROR, message='Request timeout')
        except grpc.RpcError as e:
            LOGGER.error(e)
            return Status(e.code(), message='Error occurred. {}'.format(e.details()))

    def create_partition(self, table_name, partition_tag, timeout=10):
        """
        create a specific partition under designated table. After done, the meta file in
        milvus server update partition information, you can perform actions about partitions
        with partition tag.

        :param table_name: target table name.
        :type  table_name: str

        :param partition_name: name of target partition under designated table.
        :type  partition_name: str

        :param partition_tag: tag name of target partition under designated table.
        :type  partition_tag: str

        :param timeout: time waiting for response.
        :type  timeout: int

       :return:
            Status: indicate if operation is successful

        """
        request = Prepare.partition_param(table_name, partition_tag)

        try:
            rf = self._stub.CreatePartition.future(request)
            response = rf.result(timeout=timeout)
            rf.__del__()
            return Status(code=response.error_code, message=response.reason)
        except grpc.FutureTimeoutError as e:
            LOGGER.error(e)
            return Status(code=Status.UNEXPECTED_ERROR, message='Request timeout.')
        except grpc.RpcError as e:
            LOGGER.error(e)
            return Status(e.code(), message='Error occurred. {}'.format(e.details()))

    def show_partitions(self, table_name, timeout=10):
        """
        Show all partitions under designated table.

        :param table_name: target table name.
        :type  table_name: str

        :param timeout: time waiting for response.
        :type  timeout: int

        :return:
            Status: indicate if operation is successful
            partition_list:

        """
        request = Prepare.table_name(table_name)

        try:
            rf = self._stub.ShowPartitions.future(request)
            response = rf.result(timeout=timeout)
            rf.__del__()
            # response = self._stub.ShowPartitions.future(request).result(timeout=timeout)
            status = response.status
            if status.error_code == 0:
                partition_list = [PartitionParam(table_name, p) for p in response.partition_tag_array]
                return Status(), partition_list

            return Status(code=status.error_code, message=status.reason), []
        except grpc.FutureTimeoutError as e:
            LOGGER.error(e)
            return Status(code=Status.UNEXPECTED_ERROR, message="request timeout"), []
        except grpc.RpcError as e:
            LOGGER.error(e)
            return Status(e.code(), message='Error occurred. {}'.format(e.details())), []

    def drop_partition(self, table_name, partition_tag, timeout=10):
        """
        Drop specific partition under designated table.

        :param table_name: target table name.
        :type  table_name: str

        :param partition_tag: tag name of specific partition
        :type  partition_tag: str

        :param timeout: time waiting for response.
        :type  timeout: int

        :return:
            Status: indicate if operation is successful

        """
        request = grpc_types.PartitionParam(table_name=table_name, tag=partition_tag)

        try:
            rf = self._stub.DropPartition.future(request)
            response = rf.result(timeout=timeout)
            rf.__del__()
            # response = self._stub.DropPartition.future(request).result(timeout=timeout)
            return Status(code=response.error_code, message=response.reason)
        except grpc.FutureTimeoutError as e:
            LOGGER.error(e)
            return Status(code=Status.UNEXPECTED_ERROR, message="request timeout")
        except grpc.RpcError as e:
            LOGGER.error(e)
            return Status(e.code(), message='Error occurred. {}'.format(e.details()))

    def search(self, table_name, top_k, query_records, partition_tags=None, params=None, **kwargs):
        """
        Search similar vectors in designated table

        :param table_name: target table name
        :type  table_name: str

        :param top_k: number of vertors which is most similar with query vectors
        :type  top_k: int

        :param nprobe: cell number of probe
        :type  nprobe: int

        :param query_records: vectors to query
        :type  query_records: list[list[float32]]

        :param partition_tags: tags to search
        :type  partition_tags: list

        :return
            Status: indicate if search successfully
            result: query result

        :rtype: (Status, TopKQueryResult)

        """

        iden = params.pop("identity", None)
        request = Prepare.search_param(table_name, top_k, query_records, partition_tags, params, identity=iden)

        try:
            self._search_hook.pre_search()
            print("[{}] | [{}] | [{}] | [milvus] Start search ...".format(datetime.datetime.now(), os.getpid(), iden))
            ft = self._stub.Search.future(request)
            print("[{}] | [{}] | [{}] | [milvus] Obtain search result ...".format(datetime.datetime.now(), os.getpid(), iden))
            response = ft.result()
            ft.__del__()
            print("[{}] | [{}] | [{}] | [milvus] Search done.".format(datetime.datetime.now(), os.getpid(), iden))
            self._search_hook.aft_search()

            if self._search_hook.on_response():
                return response

            if response.status.error_code != 0:
                return Status(code=response.status.error_code,
                              message=response.status.reason), []

            resutls = self._search_hook.handle_response(response)
            return Status(message='Search vectors successfully!'), resutls

        except grpc.RpcError as e:
            LOGGER.error(e)
            status = Status(code=e.code(), message='Error occurred: {}'.format(e.details()))
            return status, []

    # def search_by_id(self, table_name, top_k, nprobe, id_, partition_tag_array):
    #
    #     request = Prepare.search_by_id_param(table_name, top_k, nprobe,
    #                                          id_, partition_tag_array)
    #
    #     try:
    #         response = self._stub.SearchByID(request)
    #         if response.status.error_code == 0:
    #             return Status(message='Search vectors successfully!'), TopKQueryResult(response)
    #
    #         return Status(code=response.status.error_code, message=response.status.reason), None
    #     except grpc.RpcError as e:
    #         LOGGER.error(e)
    #         status = Status(code=e.code(), message='Error occurred: {}'.format(e.details()))
    #         return status, None

    def search_in_files(self, table_name, file_ids, query_records, top_k, params):
        """
        Query vectors in a table, in specified files.

        The server store vector data into multiple files if the size of vectors
        exceeds file size threshold. It is supported to search in several files
        by specifying file ids. However, these file ids are stored in db in server,
        and python sdk doesn't apply any APIs get them at client. It's a specific
        method used in shards. Obtain more detail about milvus shards, see
        <a href="https://github.com/milvus-io/milvus/tree/0.6.0/shards">

        :type  table_name: str
        :param table_name: table name been queried

        :type  file_ids: list[str] or list[int]
        :param file_ids: Specified files id array

        :type  query_records: list[list[float]]
        :param query_records: all vectors going to be queried

        :param query_ranges: Optional ranges for conditional search.
            If not specified, search in the whole table

        :type  top_k: int
        :param top_k: how many similar vectors will be searched

        :returns:
            Status:  indicate if query is successful
            results: query result

        :rtype: (Status, TopKQueryResult)
        """

        file_ids = list(map(int_or_str, file_ids))
        infos = Prepare.search_vector_in_files_param(
            table_name, query_records, top_k, file_ids, params
        )

        try:
            self._search_file_hook.pre_search()
            response = self._stub.SearchInFiles(infos)
            self._search_file_hook.aft_search()

            if self._search_file_hook.on_response():
                return response

            if response.status.error_code != 0:
                return Status(code=response.status.error_code,
                              message=response.status.reason), []

            return Status(message='Search vectors successfully!'), \
                   self._search_file_hook.handle_response(response)
        except grpc.RpcError as e:
            LOGGER.error(e)
            status = Status(code=e.code(), message='Error occurred. {}'.format(e.details()))
            return status, []

    def __delete_vectors_by_range(self, table_name, start_date=None, end_date=None, timeout=10):
        """
        Delete vectors by range. The data range contains start_time but not end_time
        This method is deprecated, not recommended for users.

        This API is deprecated.

        :type  table_name: str
        :param table_name: str, date, datetime

        :type  start_date: str, date, datetime
        :param start_date:

        :type  end_date: str, date, datetime
        :param end_date:

        :return:
            Status:  indicate if invoke is successful
        """

        if not self.connected():
            raise NotConnectError('Please connect to the server first')

        delete_range = Prepare.delete_param(table_name, start_date, end_date)

        try:
            status = self._stub.DeleteByDate.future(delete_range).result(timeout=timeout)
            return Status(code=status.error_code, message=status.reason)
        except grpc.FutureTimeoutError as e:
            LOGGER.error(e)
            return Status(Status.UNEXPECTED_ERROR, message='Request timeout')
        except grpc.RpcError as e:
            LOGGER.error(e)
            return Status(e.code(), message='Error occurred. {}'.format(e.details()))

    def delete_by_id(self, table_name, id_array, timeout=None):
        request = Prepare.delete_by_id_param(table_name, id_array)

        try:
            rf = self._stub.DeleteByID.future(request)
            status = rf.result(timeout=timeout)
            rf.__del__()
            # status = self._stub.DeleteByID.future(request).result(timeout=timeout)
            return Status(code=status.error_code, message=status.reason)
        except grpc.FutureTimeoutError as e:
            LOGGER.error(e)
            return Status(Status.UNEXPECTED_ERROR, message='Request timeout')
        except grpc.RpcError as e:
            LOGGER.error(e)
            return Status(e.code(), message='Error occurred. {}'.format(e.details()))

    def flush(self, table_name_array):
        request = Prepare.flush_param(table_name_array)

        try:
            response = self._stub.Flush(request)
            return Status(code=response.error_code, message=response.reason)
        except grpc.RpcError as e:
            LOGGER.error(e)
            return Status(e.code(), message='Error occurred. {}'.format(e.details()))

    def compact(self, table_name, timeout):
        request = Prepare.compact_param(table_name)

        try:
            response = self._stub.Compact(request)
            return Status(code=response.error_code, message=response.reason)
        except grpc.RpcError as e:
            LOGGER.error(e)
            return Status(e.code(), message='Error occurred. {}'.format(e.details()))

    def set_config(self, parent_key, child_key, value):
        cmd = "set_config {}.{} {}".format(parent_key, child_key, value)
        return self._cmd(cmd)

    def get_config(self, parent_key, child_key):
        cmd = "get_config {}.{}".format(parent_key, child_key)
        return self._cmd(cmd)
