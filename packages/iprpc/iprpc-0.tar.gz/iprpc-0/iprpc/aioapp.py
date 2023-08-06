import datetime
import decimal
import json
from functools import partial

from aioapp import Span
from aioapp_http import Server
from aiohttp import web
from yarl import URL

import iprpc

__all__ = ['rpc_handler']


def _json_encoder(obj):
    if isinstance(obj, URL):
        return str(obj)
    if isinstance(obj, decimal.Decimal):
        return float(obj)
    if isinstance(obj, datetime.datetime):
        return obj.isoformat()
    if isinstance(obj, datetime.date):
        return obj.strftime('%Y-%m-%d')
    if isinstance(obj, datetime.time):
        return obj.strftime('%H:%M:%S.%f%z')
    if isinstance(obj, datetime.timedelta):
        return obj.total_seconds()
    if isinstance(obj, bytes):
        try:
            return obj.decode('UTF8')
        except Exception:
            return str(obj)
    return repr(obj)


def json_encode(data):
    return json.dumps(data, default=_json_encoder)


def rpc_handler(
    api_handler: object,
    server: Server,
    path: str = '/',
    method: str = 'POST',
    debug: bool = False,
):
    executor = iprpc.MethodExecutor(api_handler)
    server.add_route(method, path, partial(_request_handler, executor, debug))


async def _request_handler(
    executor: iprpc.MethodExecutor,
    debug: bool,
    ctx: Span,
    request: web.Request,
) -> web.Response:
    data = await request.read()
    ctx.annotate(str(data))
    result = await executor.call(
        data, request.charset, const_args={'ctx': ctx}
    )
    ctx.name('call:%s' % result.method)
    if result.error is not None:
        resp = {
            "code": result.error.code,
            "message": result.error.message,
            "details": str(result.error.parent),
        }
        if result.result is not None:
            resp['result'] = result.result

        if debug:
            resp['trace'] = result.error.trace
    else:
        resp = {"code": 0, "message": 'OK', 'result': result.result}
    body = json_encode(resp).encode()
    ctx.annotate(body)
    return web.Response(body=body, content_type='application/json')
