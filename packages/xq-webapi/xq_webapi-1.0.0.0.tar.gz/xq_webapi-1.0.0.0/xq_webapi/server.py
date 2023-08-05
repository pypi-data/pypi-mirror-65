# -*- coding: utf-8 -*-

__author__ = 'XQ'

import importlib
from tornado import ioloop, httpserver, web
from xq_webapi.handler import BaseHandler
from xq_webapi import api


class APIHandler(BaseHandler):
    def execute(self, params):
        services = APIServer.get_actions()
        _service_name = self.request.path
        _service = services.get(_service_name)
        if _service is None:
            raise 'API服务 "%s"不存在' % _service_name
        _module = importlib.import_module(_service['module'])
        _class = _service.get("class")
        if _class is None:
            _owner = _module
        else:
            cls = getattr(_module, _class)
            _owner = cls()
        _params = _service.get("params", [])
        useless = set([_key for _key in params]) - set(_params)
        for _key in useless:
            del params[_key]
        data = getattr(_owner, _service["method"])(**params)
        return {"success": True, "data": data}


class APIServer:
    __routes = [("/.*", APIHandler)]
    __services = {}
    __interceptor = None
    __cookie_secret = None  # "P2eXxGwBQKeuzwEUQsrZxDOGfgiE2EhUlzKzaY/agSQ="

    @classmethod
    def interceptor(cls, interceptor):
        cls.__interceptor = interceptor

    @classmethod
    def cookie_secret(cls, cookie_secret):
        cls.__cookie_secret = cookie_secret

    @classmethod
    def get_action(cls, name):
        return cls.__services.get(name)

    @classmethod
    def get_actions(cls):
        return cls.__services

    @classmethod
    def add_service(cls, module, meta):
        action = meta.get("action")
        service_path = "/%s/%s" % (module, action)
        cls.__services[service_path] = meta

    @classmethod
    def add_route(cls, route, handler):
        cls.__routes.append((route, handler))

    @classmethod
    def add_action(cls, module, action, method):
        cls.add_service(module, {"action": action, "method": method})

    @classmethod
    def load_actions(cls):
        modules = api.get_modules()
        for module, actions in modules.items():
            for action in actions:
                cls.add_service(module, action)

    @classmethod
    def start(cls, port=80):
        cls.load_actions()
        application = web.Application(cls.__routes, gzip=True, autoescape=None,
                                      cookie_secret=cls.__cookie_secret)
        http_server = httpserver.HTTPServer(application, xheaders=True)
        http_server.listen(port)
        ioloop.IOLoop.instance().start()
