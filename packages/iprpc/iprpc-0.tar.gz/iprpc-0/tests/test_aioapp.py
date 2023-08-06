import asyncio
import gc

from aioapp import Application, Span
from aioapp_http import Handler, Server
from aiohttp import ClientSession, web
from pytest import fixture
from yarl import URL

from iprpc import method
from iprpc.aioapp import rpc_handler


class TestApi:
    @method()
    async def meth1(self, ctx: Span, arg1) -> None:
        return arg1


@fixture()
def event_loop():
    asyncio.set_event_loop_policy(asyncio.DefaultEventLoopPolicy())
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    gc.collect()
    loop.close()


@fixture()
def loop(event_loop):
    return event_loop


@fixture()
async def srv(loop, unused_tcp_port):
    api = TestApi()

    class TestHandler(Handler):
        async def prepare(self) -> None:
            rpc_handler(api, self.server)
            self.server.error_handler = self.error_handler

        async def error_handler(self, ctx: Span, request, error: Exception):
            print('*' * 88)
            print(error)
            self.app.log_err(error)
            if isinstance(error, web.HTTPException):
                return error
            return web.HTTPInternalServerError()  # pragma: no cover

    app = Application(loop)
    app.add('srv', Server('127.0.0.1', unused_tcp_port, TestHandler))
    app.url = URL('http://127.0.0.1:%d/' % unused_tcp_port)
    await app.run_prepare()
    yield app
    await app.run_shutdown()


async def test_aioapp(srv):
    async with ClientSession() as sess:
        resp = await sess.post(
            srv.url, data=b'{"method":"meth1","params":{"arg1": 1}}'
        )
        assert resp.status == 200, await resp.read()
        js = await resp.json()
        assert js['code'] == 0, await resp.read()
        assert js['result'] == 1, await resp.read()
