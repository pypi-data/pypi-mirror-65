import datetime
import json
import traceback
from functools import wraps
from typing import List, Optional, Type, Union

import aiohttp
import pytest
from aiohttp import web
from pydantic import BaseModel, StrictInt

import iprpc

ErrType = Type[iprpc.BaseError]


def format_errors(errors: List[Union[BaseException, str]]) -> str:
    res = []
    for err in errors:
        if isinstance(err, BaseException):
            fmt = '%s%s: %s' % (
                ''.join(traceback.format_tb(err.__traceback__)),
                err.__class__.__name__,
                err,
            )
            res.append(fmt)
        else:
            res.append(err)
    return ('\n\n%s\n\n' % ('-' * 70)).join(res)


def mkapp(handler):
    errors = []

    caller = iprpc.MethodExecutor(handler)

    async def home_handler(request: web.Request):
        try:
            req_bytes = await request.read()
            result = await caller.call(
                req_bytes, encoding=request.charset or 'utf-8'
            )
            if result.error is not None:
                errors.append(result.error)
                return web.Response(
                    text=json.dumps(
                        {
                            'code': result.error.code,
                            'message': result.error.message,
                            'details': str(result.error.parent),
                        }
                    ),
                    content_type='application/json',
                )
            else:
                return web.Response(
                    text=json.dumps({'code': 0, 'result': result.result}),
                    content_type='application/json',
                )

        except Exception as err:
            errors.append(err)
            raise

    app = web.Application()
    app.router.add_post('/', home_handler)

    def assert_no_errors():
        assert len(errors) == 0, format_errors(errors)

    def assert_has_error(err):
        assert len(errors) == 1, format_errors(errors)
        assert isinstance(errors[0], err), format_errors(errors)

    app.assert_no_errors = assert_no_errors
    app.assert_has_error = assert_has_error
    return app


async def exec(
    aiohttp_server, handler, request: bytes, error: Optional[ErrType]
):
    server = await aiohttp_server(mkapp(handler()))
    async with aiohttp.ClientSession() as sess:
        resp = await sess.post(server.make_url('/'), data=request)

        if error is None:
            server.app.assert_no_errors()
        else:
            server.app.assert_has_error(error)

        js = await resp.json()
        assert isinstance(js, dict), str(js)
        assert 'code' in js, str(js)
        if error is None:
            assert js['code'] == 0, str(js)
        else:
            assert js['code'] == error.code, str(js)
        return js


async def test_error_deserialization(aiohttp_server):
    class TestHandler:
        pass

    await exec(aiohttp_server, TestHandler, b'{1}', iprpc.DeserializeError)


async def test_error_missing_method(aiohttp_server):
    class TestHandler:
        pass

    await exec(
        aiohttp_server, TestHandler, b'{"params":{}}', iprpc.InvalidRequest
    )


async def test_error_invalid_method(aiohttp_server):
    class TestHandler:
        pass

    await exec(
        aiohttp_server, TestHandler, b'{"method":[1]}', iprpc.InvalidRequest
    )


async def test_error_invalid_params(aiohttp_server):
    class TestHandler:
        pass

    await exec(
        aiohttp_server,
        TestHandler,
        b'{"method":"test","params":[1,2]}',
        iprpc.InvalidRequest,
    )


async def test_error_private_attr(aiohttp_server):
    class TestHandler:
        def __init__(self):
            self.abc = 1

    await exec(
        aiohttp_server,
        TestHandler,
        b'{"method":"abc","params":{}}',
        iprpc.MethodNotFound,
    )


async def test_sync(aiohttp_server):
    class TestHandler:
        @iprpc.method()
        def hello(self, a: int):
            return a + 1

    data = await exec(
        aiohttp_server,
        TestHandler,
        b'{"method": "hello", "params": {"a": 1}}',
        None,
    )
    assert 'result' in data, str(data)
    assert data['result'] == 2, str(data)


async def test_internal_exec_cache(aiohttp_server):
    class TestHandler:
        def __init__(self):
            self.c = 0

        @iprpc.method()
        def hello(self):
            self.c += 1
            return self.c

        @iprpc.method()
        def hello2(self):
            self.c += 1
            return self.c

    app = mkapp(TestHandler())
    server = await aiohttp_server(app)
    async with aiohttp.ClientSession() as sess:
        resp = await sess.post(
            server.make_url('/'), data=b'{"method": "hello", "params": {}}'
        )
        data = await resp.json()
        assert data['result'] == 1

        resp = await sess.post(
            server.make_url('/'), data=b'{"method": "hello2", "params": {}}'
        )
        data = await resp.json()
        assert data['result'] == 2

        resp = await sess.post(
            server.make_url('/'), data=b'{"method": "hello2", "params": {}}'
        )
        data = await resp.json()
        assert data['result'] == 3

        resp = await sess.post(
            server.make_url('/'), data=b'{"method": "hello", "params": {}}'
        )
        data = await resp.json()
        assert data['result'] == 4

        app.assert_no_errors()


async def test_custom_name(aiohttp_server):
    class TestHandler:
        @iprpc.method(name='RunHello')
        def hello(self, a: int):
            return a + 1

    data = await exec(
        aiohttp_server,
        TestHandler,
        b'{"method": "RunHello", "params": {"a": 1}}',
        None,
    )
    assert 'result' in data, str(data)
    assert data['result'] == 2, str(data)


async def test_normal(aiohttp_server):
    class TestHandler:
        @iprpc.method()
        async def hello(self, a: int):
            return a + 1

    data = await exec(
        aiohttp_server,
        TestHandler,
        b'{"method": "hello", "params": {"a": 1}}',
        None,
    )
    assert 'result' in data, str(data)
    assert data['result'] == 2, str(data)


async def test_method_not_found(aiohttp_server):
    class TestHandler:
        pass

    await exec(
        aiohttp_server, TestHandler, b'{"method": "no"}', iprpc.MethodNotFound
    )


async def test_missing_arg1(aiohttp_server):
    class TestHandler:
        @iprpc.method()
        async def hello(self, arg1):
            pass

    res = await exec(
        aiohttp_server,
        TestHandler,
        b'{"method": "hello", "params": {}}',
        iprpc.InvalidArguments,
    )
    assert 'arg1' in res['details'], res


async def test_missing_arg2(aiohttp_server):
    class TestHandler:
        @iprpc.method()
        async def hello(self, *, arg1):
            pass

    res = await exec(
        aiohttp_server,
        TestHandler,
        b'{"method": "hello", "params": {}}',
        iprpc.InvalidArguments,
    )
    assert 'arg1' in res['details'], res


async def test_missing_arg3(aiohttp_server):
    class TestHandler:
        @iprpc.method(validators={"arg1": {"type": "string"}})
        async def hello(self, *, arg1):
            pass

    res = await exec(
        aiohttp_server,
        TestHandler,
        b'{"method": "hello", "params": {"arg1": 1}}',
        iprpc.InvalidArguments,
    )
    assert 'arg1' in res['details'], res


async def test_missing_arg4(aiohttp_server):
    class TestHandler:
        @iprpc.method()
        async def hello(self, *, arg1):
            pass

    res = await exec(
        aiohttp_server,
        TestHandler,
        b'{"method": "hello", "params": {"arg2": 1}}',
        iprpc.InvalidArguments,
    )
    assert 'arg2' in res['details'], res


async def test_complicated_arg(aiohttp_server):
    class TestHandler:
        @iprpc.method(validators={"a": {"type": "integer"}})
        async def hello(self, a, b, c=30, *, d, e=5):
            return [a, b, c, d, e]

    res = await exec(
        aiohttp_server,
        TestHandler,
        b'{"method": "hello", ' b'"params": {"a": 1, "b": 2, "c": 3, "d": 4}}',
        None,
    )
    assert res['result'] == [1, 2, 3, 4, 5], str(res)


async def test_complicated_decorator(aiohttp_server):
    calls = []

    def some_decorator(fn):
        @wraps(fn)
        def wrapper(*args, **kwargs):
            calls.append((args, kwargs))
            return fn(*args, **kwargs)

        return wrapper

    class TestHandler:
        @some_decorator
        @iprpc.method()
        @some_decorator
        async def hello(self, a, b, c=30, *, d, e=5):
            return [a, b, c, d, e]

    res = await exec(
        aiohttp_server,
        TestHandler,
        b'{"method": "hello", ' b'"params": {"a": 1, "b": 2, "c": 3, "d": 4}}',
        None,
    )
    assert res['result'] == [1, 2, 3, 4, 5], str(res)
    assert len(calls) == 2, str(calls)
    assert isinstance(calls[0][0][0], TestHandler), str(calls)
    assert isinstance(calls[1][0][0], TestHandler), str(calls)
    assert calls[0][1] == {'a': 1, 'b': 2, 'c': 3, 'd': 4}, str(calls)
    assert calls[1][1] == {'a': 1, 'b': 2, 'c': 3, 'd': 4}, str(calls)


async def test_proger_error_validator(aiohttp_server):
    with pytest.raises(UserWarning):

        class TestHandler:
            @iprpc.method(validators={"a": {"type": "integer"}})
            async def hello(self):
                return


async def test_proger_error_method(aiohttp_server):
    with pytest.raises(UserWarning):

        class TestHandler:
            @iprpc.method()
            async def hello(self):
                return

            @iprpc.method(name='hello')
            async def hello2(self):
                return

        iprpc.MethodExecutor(TestHandler())


async def test_internval_error(aiohttp_server):
    class TestHandler:
        @iprpc.method()
        async def hello(self):
            raise Exception(1)

    await exec(
        aiohttp_server,
        TestHandler,
        b'{"method": "hello", "params": {}}',
        iprpc.InternalError,
    )


async def test_api_error(aiohttp_server):
    class TestHandler:
        @iprpc.method()
        async def hello(self):
            raise iprpc.InvalidArguments()

    await exec(
        aiohttp_server,
        TestHandler,
        b'{"method": "hello", "params": {}}',
        iprpc.InvalidArguments,
    )


async def test_kwargs(aiohttp_server):
    class TestHandler:
        @iprpc.method()
        async def hello(self, k, **kwargs):
            return {"k": k, **kwargs}

    data = await exec(
        aiohttp_server,
        TestHandler,
        b'{"method": "hello", "params": {"k": "v", "a": "b"}}',
        None,
    )

    assert 'result' in data, str(data)
    assert data['result'] == {"k": "v", "a": "b"}, str(data)


async def test_struct(aiohttp_server):
    class TestHandler:
        @iprpc.method()
        async def sum(self, a: float, b: float) -> float:
            return a + b

    caller = iprpc.MethodExecutor(
        TestHandler(), method_key='name', params_key=None
    )
    result = await caller.call(b'{"name":"sum","a":3,"b":4}')
    assert result.result == 7

    caller = iprpc.MethodExecutor(
        TestHandler(), method_key='name', params_key='args'
    )
    result = await caller.call(b'{"name":"sum","args":{"a":4,"b":5}}')
    assert result.result == 9

    caller = iprpc.MethodExecutor(
        TestHandler(), method_key='name', params_key='args'
    )
    result = await caller.call(b'{"method":"sum","params":{"a":4,"b":5}}')
    assert result.result is None
    assert isinstance(result.error, iprpc.InvalidRequest)


async def test_annotations_success(aiohttp_server):
    class Complicated(BaseModel):
        count: StrictInt

    class TestHandler:
        @iprpc.method()
        async def test(wrongself: 'TestHandler', arg: int) -> dict:
            return {"arg": arg}

        @iprpc.method()
        async def hello(
            self,
            c: Complicated,
            i: List[Optional[StrictInt]],
            j=0,
            k: bool = False,
        ):
            return {"i": i, 'j': j, 'k': k}

    data = await exec(
        aiohttp_server,
        TestHandler,
        b'{"method": "test", "params": {"arg": 123}}',
        None,
    )
    assert data['result'] == {'arg': 123}

    data = await exec(
        aiohttp_server,
        TestHandler,
        b'{"method": "hello", "params": {"i": [1, null, 2], '
        b'"c": {"count": 1}}}',
        None,
    )

    assert data['result'] == {'i': [1, None, 2], 'j': 0, 'k': False}


async def test_annotations_complicated(aiohttp_server):
    class Complicated(BaseModel):
        count: StrictInt

    class TestHandler:
        @iprpc.method()
        async def hello(
            self,
            c: Complicated,
            i: List[Optional[StrictInt]],
            j=0,
            k: bool = False,
        ):
            return {"i": i, 'j': j, 'k': k}

    data = await exec(
        aiohttp_server,
        TestHandler,
        b'{"method": "hello", "params": {"i": [1, null, 2], '
        b'"c": {"count": false}}}',
        iprpc.InvalidArguments,
    )

    assert 'c.count' in data['details']


async def test_serialize_inh_result():
    class D(datetime.datetime):
        pass

    assert (
        '2020-01-02T03:04:05.000123'
        == iprpc.MethodExecutor._serialize_result(D(2020, 1, 2, 3, 4, 5, 123))
    )
