from aiohttp import web_log


class AccessLogger(web_log.AccessLogger):
    def log(self, request, response, time):
        if request.path.endswith("health"):
            return
        if "static" in request.path:
            return
        super(AccessLogger, self).log(request, response, time)
