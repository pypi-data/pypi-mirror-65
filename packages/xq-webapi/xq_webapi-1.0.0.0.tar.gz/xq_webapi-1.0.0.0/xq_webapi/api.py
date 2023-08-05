# -*- coding: utf-8 -*-

__author__ = 'XQ'

from xq_common.decorator import Decorator

__route = Decorator()
__api = Decorator()

route = __route.module
module = __api.module
action = __api.action

get_routes = __api.get_modules
get_modules = __api.get_modules
