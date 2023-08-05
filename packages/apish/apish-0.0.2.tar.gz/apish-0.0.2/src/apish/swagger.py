from functools import wraps
from aiohttp import web

from apish.resource import prepare

_METHODS = ["get", "post", "patch", "put", "delete"]


def for_endpoint(endpoint):
    if hasattr(endpoint, "swagger"):
        return endpoint.swagger
    return {}


def for_resource(resource):
    result = {}
    for method in _METHODS:
        if hasattr(resource, method):
            result[method] = for_endpoint(getattr(resource, method))
    return result


def info(app):
    result = app.metadata.info.copy()
    result["title"] = app.metadata.title
    if app.metadata.description is not None:
        result["description"] = app.metadata.description
    return result


def for_app(app):
    result = {"openapi": "3.0.0", "info": info(app), "paths": {}}
    for route in app.router.routes():
        if hasattr(route.handler, "swagger"):
            path = route.handler.swagger["path"]
            result["paths"][path] = for_resource(route.handler)
    return result


def summary(text):
    def wrapper(f):
        prepare(f)
        f.swagger["summary"] = text

        @wraps(f)
        def fn(*args, **kwargs):
            return f(*args, **kwargs)

        return fn

    return wrapper
