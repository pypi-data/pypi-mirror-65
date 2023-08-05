from functools import wraps

from apish.resource import prepare

_METHODS = ["get", "post", "patch", "put", "delete"]


def info(app):
    result = app.metadata.info.copy()
    result["title"] = app.metadata.title
    if app.metadata.description is not None:
        result["description"] = app.metadata.description
    return result


def for_endpoint(endpoint, tags):
    result = {}
    if hasattr(endpoint, "swagger"):
        result["operationId"] = endpoint.swagger["operationId"]
        if "summary" in endpoint.swagger:
            result["summary"] = endpoint.swagger["summary"]
        if tags is not None:
            result["tags"] = tags
        if "body" in endpoint.swagger:
            result["requestBody"] = {
                "required": True,
                "content": {"application/json": {"schema": endpoint.swagger["body"]}},
            }
        result["responses"] = {200: {"description": "OK"}}
        if "responses" in endpoint.swagger:
            for (status_code, response) in endpoint.swagger["responses"].items():
                result["responses"][status_code] = response
    return result


def for_resource(resource):
    result = {}
    tags = resource.swagger.get("tags")
    for method in _METHODS:
        if hasattr(resource, method):
            result[method] = for_endpoint(getattr(resource, method), tags)
    return result


def for_app(app):
    result = {
        "openapi": "3.0.0",
        "info": info(app),
        "servers": [{"url": app.root}],
        "paths": {},
    }
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


def request_body(schema, **kwargs):
    def wrapper(f):
        prepare(f)
        kwargs["content"] = schema
        f.swagger["request_body"] = kwargs
        return f

    return wrapper


def response(status_code, schema, **kwargs):
    def wrapper(f):
        prepare(f)
        kwargs["content"] = {"application/json": {"schema": schema}}
        f.swagger.setdefault("responses", {})[status_code] = kwargs
        return f

    return wrapper
