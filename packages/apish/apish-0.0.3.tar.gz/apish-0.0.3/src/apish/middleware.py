from aiohttp import web


# TOOD: Figure out the exact shape of the error, and make it easy for clients to
# return their own errors in the same shape.  See
# https://opensource.zalando.com/restful-api-guidelines/#http-status-codes-and-errors
@web.middleware
async def handle_exceptions(request, handler):
    try:
        return await handler(request)
    except web.HTTPException as exc:
        data = {"status": exc.status_code, "title": exc.reason, "detail": exc.text}
        return web.json_response(data, status=exc.status_code)
    except Exception as exc:  # pylint: disable=broad-except
        data = {"status": 500, "title": str(exc)}
        if hasattr(exc, "to_dict"):
            # pylint: disable=no-member
            data["detail"] = exc.to_dict()
        return web.json_response(data, status=500)
