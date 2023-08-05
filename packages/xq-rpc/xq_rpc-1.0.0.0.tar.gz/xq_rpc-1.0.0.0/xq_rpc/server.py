# -*- coding: utf-8 -*-

__author__ = 'XQ'

import json
import grpc
import importlib
from concurrent import futures
from xq_rpc import rpc, rpc_pb2


class RPCServer:
    __server = None
    __services = {}

    @classmethod
    def get_action(cls, name):
        return cls.__services.get(name)

    @classmethod
    def get_actions(cls):
        return cls.__services

    @classmethod
    def server(cls):
        if cls.__server is None:
            cls.__server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
        return cls.__server

    @classmethod
    def add_service(cls, module, meta, prefix=""):
        module = "%s%s" % ((prefix + "." if prefix else ""), module)
        action = meta.get("action")
        service_path = "/%s/%s" % (module, action)
        cls.__services[service_path] = meta
        method_handlers = {
            action: grpc.unary_unary_rpc_method_handler(
                cls.__execute,
                request_deserializer=rpc_pb2.RPCRequest.FromString,
                response_serializer=rpc_pb2.RPCResponse.SerializeToString,
            )
        }
        generic_handler = grpc.method_handlers_generic_handler(module, method_handlers)
        server = cls.server()
        server.add_generic_rpc_handlers((generic_handler,))

    @classmethod
    def add_action(cls, module, action, method, prefix=""):
        cls.add_service(module, {"action": action, "method": method}, prefix)

    @classmethod
    def __execute(cls, request, context):
        service_name = context._rpc_event.call_details.method.decode('utf-8')
        service = cls.get_action(service_name)
        if service is None:
            raise 'RPC服务 "%s"不存在' % service_name
        method = service.get("method")
        if isinstance(method, str):
            module = service.get("module")
            if not module or not method:
                raise 'RPC服务 "%s" 定义不完整' % service_name
            _module = importlib.import_module(module)
            _class = service.get("class")
            if _class is None:
                _owner = _module
            else:
                _owner = getattr(_module, _class)()
            method = getattr(_owner, method)
        result = method(request.params and json.loads(request.params))
        return rpc_pb2.RPCResponse(message=json.dumps(result))

    @classmethod
    def load_actions(cls):
        modules = rpc.get_modules()
        for module, actions in modules.items():
            for action in actions:
                RPCServer.add_service(module, action)

    @classmethod
    def start(cls, port=50000):
        cls.load_actions()
        server = cls.server()
        server.add_insecure_port("[::]:%s" % port)
        server.start()
