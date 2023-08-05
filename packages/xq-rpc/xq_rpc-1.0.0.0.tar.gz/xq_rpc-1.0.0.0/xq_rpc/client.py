# -*- coding: utf-8 -*-

__author__ = 'XQ'

import grpc
import json
from xq_rpc import rpc_pb2

class RPCClient:
    @classmethod
    def execute(cls, address, path, params):
        with grpc.insecure_channel(address) as channel:
            proxy = channel.unary_unary(
                "/%s" % path,
                request_serializer=rpc_pb2.RPCRequest.SerializeToString,
                response_deserializer=rpc_pb2.RPCResponse.FromString,
            )
            response = proxy(rpc_pb2.RPCRequest(params=json.dumps(params)))
            return json.loads(response.message)


if __name__ == '__main__':
    a = RPCClient.execute("127.0.0.1:50000",'user_info/get',{"id":"aasad"})
    print(a)