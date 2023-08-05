from aiohttp import web


class Resource(web.View):
    pass


def prepare(f):
    if not hasattr(f, "swagger"):
        m = {"operationId": f.__qualname__.lower()}
        setattr(f, "swagger", m)


class RouteTableDef(web.RouteTableDef):
    # pylint: disable=arguments-differ
    def get(self, path, *args, **kwargs):
        def wrapper(f):
            prepare(f)
            f.swagger["method"] = "get"
            f.swagger["path"] = path

            return super(RouteTableDef, self).get(path, *args, **kwargs)(f)

        return wrapper

    def resource(self, path, *args, swagger=True, **kwargs):
        def wrapper(cls):
            if swagger:
                prepare(cls)
                cls.swagger["path"] = path
            return self.view(path, *args, **kwargs)(cls)

        return wrapper
