import os
from itertools import cycle
from numbers import Number

import grpc
from mtbpy import mtb_command_rpc_pb2
from mtbpy import mtb_command_rpc_pb2_grpc


class mtb_instance(object):
    def __init__(self):
        address = "127.0.0.1:{0}".format(os.getenv("MTB_RPC_PORT"))
        self.channel = grpc.insecure_channel(address, options=[
            ("grpc.max_receive_message_length", -1)
        ])
        try:
            grpc.channel_ready_future(self.channel).result(timeout=5)
        except grpc.FutureTimeoutError:
            raise RuntimeError(
                "Error connecting to Minitab at {0}".format(address))
        self.rpc_stub = mtb_command_rpc_pb2_grpc.MtbCommandStub(self.channel)

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.channel.close()

    def get_column(self, column_name):
        request = mtb_command_rpc_pb2.VariableRequest()
        request.var_type = mtb_command_rpc_pb2.VariableType.VAR_COLUMN
        request.var_id = column_name
        try:
            response = self.rpc_stub.GetVariable(request)
        except grpc.RpcError as e:
            if e.code() != grpc.StatusCode.NOT_FOUND:
                raise
        else:
            if response.found:
                if len(response.numeric_data) > 0:
                    return response.numeric_data
                elif len(response.text_data) > 0:
                    return response.text_data

    def get_constant(self, constant_name):
        request = mtb_command_rpc_pb2.VariableRequest()
        request.var_type = mtb_command_rpc_pb2.VariableType.VAR_CONSTANT
        request.var_id = constant_name
        try:
            response = self.rpc_stub.GetVariable(request)
        except grpc.RpcError as e:
            if e.code() != grpc.StatusCode.NOT_FOUND:
                raise
        else:
            if response.found:
                if len(response.numeric_data) > 0:
                    return response.numeric_data[0]
                elif len(response.text_data) > 0:
                    return response.text_data[0]

    def get_matrix(self, matrix_name):
        request = mtb_command_rpc_pb2.VariableRequest()
        request.var_type = mtb_command_rpc_pb2.VariableType.VAR_MATRIX
        request.var_id = matrix_name
        try:
            response = self.rpc_stub.GetVariable(request)
        except grpc.RpcError as e:
            if e.code() != grpc.StatusCode.NOT_FOUND:
                raise
        else:
            if response.found and len(response.numeric_data) > 0:
                lists = [[] for i in range(response.m)]
                for d, m in zip(response.numeric_data, cycle(range(response.m))):
                    lists[m].append(d)
                return lists

    def add_message(self, content):
        request = mtb_command_rpc_pb2.AddMessageRequest()
        request.content = content
        self.rpc_stub.AddMessage(request)

    def set_note(self, content):
        request = mtb_command_rpc_pb2.SetCommandNoteRequest()
        request.content = content
        self.rpc_stub.SetCommandNote(request)

    def set_command_title(self, content):
        request = mtb_command_rpc_pb2.SetCommandTitleRequest()
        request.content = content
        try:
            self.rpc_stub.SetCommandTitle(request)
        except grpc.RpcError as e:
            if e.code() != grpc.StatusCode.INVALID_ARGUMENT:
                raise

    def add_image(self, path):
        image_data = None
        with open(path, "rb") as f:
            image_data = f.read()
        self.add_image_bytes(image_data)

    def add_image_bytes(self, bytes):
        request = mtb_command_rpc_pb2.AddImageRequest()
        request.image_data = bytes
        self.rpc_stub.AddImage(request)

    def add_table(self, columns, headers=[], title="", footnote=""):
        request = mtb_command_rpc_pb2.AddTableRequest()
        if isinstance(title, str):
            request.title = title
        if isinstance(footnote, str):
            request.footnote = footnote

        for column in columns:
            data = request.columns.add()
            if len(column) == 0:
                # empty column, but still need to 'set' the oneof
                data.numeric_data.data[:] = []
                continue
            if isinstance(column[0], Number):
                data.numeric_data.data[:] = map(float, column)
            elif isinstance(column[0], str):
                data.text_data.data[:] = map(str, column)
            else:
                raise TypeError(
                    "Table data values must be of type str or a subclass of `numbers.Number`.")

        request.headers[:] = map(str, headers)

        self.rpc_stub.AddTable(request)
