from aiohttp import web
from aiohttp.web_routedef import hdrs

from apish import swagger
from apish.logger import AccessLogger
from apish.resource import Resource, RouteTableDef


routes = RouteTableDef()


@routes.resource("", swagger=False)
class SwaggerUI(Resource):
    async def get(self):
        return web.Response(text=self.request.app.swagger_ui, content_type="text/html")


@routes.resource("/swagger.json", swagger=False)
class Swagger(Resource):
    async def get(self):
        return web.json_response(self.request.app.swagger)


@routes.resource("/info")
class Info(Resource):
    @swagger.summary("View information about the service")
    async def get(self):
        return web.json_response(self.request.app.info)


@routes.resource("/health")
class Health(Resource):
    @swagger.summary("Check if service is healthy")
    async def get(self):
        return web.json_response(await self.request.app.health())


class App(web.Application):

    _STATIC_PATH = "/static"

    class _RouteDefWrapper(web.AbstractRouteDef):
        def __init__(self, root, route):
            self.root = root
            self.route = route

        def register(self, router):
            r = self.route
            if r.method in hdrs.METH_ALL:
                reg = getattr(router, "add_" + r.method.lower())
                reg(self.root + r.path, r.handler, **r.kwargs)
            else:
                router.add_route(r.method, self.root + r.path, r.handler, **r.kwargs)

    def __init__(self, metadata, env, *, root=None, **kwargs):
        super().__init__(**kwargs)
        self.env = env
        self.tasks = {}
        self.root = root or f"/{metadata.name}/api"
        self.metadata = metadata
        self.__swagger = None
        self.__swagger_ui = None

        self.add_routes(routes)
        self.router.add_static(self.root + self._STATIC_PATH, "resources/dist/")

    @property
    def swagger(self):
        if self.__swagger is None:
            self.__swagger = swagger.for_app(self)
        return self.__swagger

    @property
    def swagger_ui(self):
        if self.__swagger_ui is None:
            with open("resources/dist/index.html") as h:
                html = h.read()
                html = html.replace("##STATIC_PATH##", self.root + self._STATIC_PATH)
                html = html.replace("##SWAGGER_URL##", self.root + "/swagger.json")
                self.__swagger_ui = html
        return self.__swagger_ui

    @property
    def info(self):
        return {
            "namespace": self.metadata.namespace,
            "name": self.metadata.name,
            "version": self.metadata.version,
        }

    async def health(self):
        # pylint: disable=no-self-use
        return {"status": "ok"}

    def start(self, config):
        web.run_app(self, access_log_class=AccessLogger, **config)

    def add_routes(self, routes):
        """Add routes prefixed by the root URL."""

        def wrap():
            for r in routes:
                yield self._RouteDefWrapper(self.root, r)

        super(App, self).add_routes(wrap())
