# -*- coding: utf-8 -*-

__author__ = 'XQ'

import json
from tornado.gen import coroutine
from tornado.web import RequestHandler
from tornado.concurrent import run_on_executor
from concurrent.futures import ThreadPoolExecutor

class BaseHandler(RequestHandler):
    executor = ThreadPoolExecutor(max_workers=200)

    def __init__(self, application, request, **kwargs):
        super(BaseHandler, self).__init__(application, request, **kwargs)

    @coroutine
    def get(self):
        """
        get请求
        :return:
        """
        try:
            params = {key: value[0] for key, value in self.request.arguments.items()}
            data = yield self.asynchronous_execute(params)
            if data:
                self.write(data)
        except Exception as error:
            raise error
        finally:
            self.finish()

    @coroutine
    def post(self):
        """
        post 请求
        :return:
        """
        try:
            params = json.loads(self.request.body, strict=False)
            data = yield self.asynchronous_execute(params)
            if data:
                self.write(data)
        except Exception as error:
            raise error
        finally:
            self.finish()

    @run_on_executor
    def asynchronous_execute(self, params):
        try:
            # self.get_context()
            return self.execute(params)
        except Exception as error:
            # self.db.rollback()
            raise error
        finally:
            # self.db.remove()
            pass

    def execute(self, params):
        pass
