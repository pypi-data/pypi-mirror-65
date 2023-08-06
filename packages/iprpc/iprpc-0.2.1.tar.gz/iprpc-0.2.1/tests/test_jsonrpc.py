import json

from iprpc import JsonRpcExecutor, method


async def test_success():
    class H:
        @method()
        async def echo(self, text: str) -> str:
            return 'echo: %s' % text

    ex = JsonRpcExecutor(H())
    res = await ex.execute(
        b'{"jsonrpc": "2.0",'
        b' "method": "echo", "params": {"text": "123"}, "id": 10}'
    )
    assert json.loads(res) == {
        "jsonrpc": "2.0",
        "id": 10,
        "result": "echo: 123",
    }


async def test_err_parse_1():
    class H:
        pass

    ex = JsonRpcExecutor(H())
    res = await ex.execute(b'eeeee')
    assert json.loads(res) == {
        "jsonrpc": "2.0",
        "id": None,
        "error": {"message": "Parse error", "code": -32700},
    }


async def test_err_invalid_req_1():
    class H:
        pass

    ex = JsonRpcExecutor(H())
    res = await ex.execute(b'{"method": "echo","params": {"text": "1"}}')
    assert json.loads(res) == {
        "jsonrpc": "2.0",
        "id": None,
        "error": {"message": "Invalid Request", "code": -32600},
    }


async def test_err_invalid_req_2():
    class H:
        pass

    ex = JsonRpcExecutor(H())
    res = await ex.execute(b'{"params": []}')
    assert json.loads(res) == {
        "jsonrpc": "2.0",
        "id": None,
        "error": {"message": "Invalid Request", "code": -32600},
    }


async def test_error():
    class H:
        @method()
        async def echo(self, text: str) -> str:
            raise Exception('Ex')

    ex = JsonRpcExecutor(H())
    res = await ex.execute(
        b'{"jsonrpc": "2.0",'
        b' "method": "echo", "params": {"text": "123"}, "id": 10}'
    )
    assert json.loads(res) == {
        'error': {'code': -32000, 'message': 'Ex'},
        'id': 10,
        'jsonrpc': '2.0',
    }


async def test_error_with_data():
    class H:
        @method()
        async def echo(self, text: str) -> str:
            raise Exception('Ex', 'some data')

    ex = JsonRpcExecutor(H())
    res = await ex.execute(
        b'{"jsonrpc": "2.0",'
        b' "method": "echo", "params": {"text": "123"}, "id": 10}'
    )
    assert json.loads(res) == {
        'error': {'code': -32000, 'data': 'some data', 'message': 'Ex'},
        'id': 10,
        'jsonrpc': '2.0',
    }


async def test_error_method():
    class H:
        pass

    ex = JsonRpcExecutor(H())
    res = await ex.execute(
        b'{"jsonrpc": "2.0",'
        b' "method": "echo", "params": {"text": "123"}, "id": 10}'
    )
    assert json.loads(res) == {
        'error': {'code': -32601, 'message': 'Method not found'},
        'id': 10,
        'jsonrpc': '2.0',
    }


async def test_error_params():
    class H:
        @method()
        async def echo(self, text: str, a: int) -> str:
            raise Exception('Ex')

    ex = JsonRpcExecutor(H())
    res = await ex.execute(
        b'{"jsonrpc": "2.0",' b' "method": "echo", "params": {}, "id": 10}'
    )
    assert json.loads(res) == {
        'error': {
            'code': -32602,
            'data': {'info': 'Missing 2 required argument(s):  text, a'},
            'message': 'Invalid params',
        },
        'id': 10,
        'jsonrpc': '2.0',
    }


async def test_notification():
    class H:
        @method()
        async def echo(self, text: str) -> str:
            return text

    ex = JsonRpcExecutor(H())
    res = await ex.execute(
        b'{"jsonrpc": "2.0",' b' "method": "echo", "params": {"text": "123"}}'
    )
    assert res == b''


async def test_batch():
    class H:
        @method()
        async def echo(self, text: str) -> str:
            return 'echo: %s' % text

        @method()
        async def err(self) -> None:
            raise Exception('some error', {'pay': 'load'})

    ex = JsonRpcExecutor(H())
    res = await ex.execute(
        b'[{"jsonrpc": "2.0", '
        b'"method": "echo", "params": {"text": "1"}, "id": 1},'
        b'{"jsonrpc": "2.0", '
        b'"method": "err", "params": {}, "id": 3},'
        b'{"jsonrpc": "2.0", '
        b'"method": "echo", "params": {"text": "2"}, "id": 2}]'
    )
    assert json.loads(res) == [
        {"jsonrpc": "2.0", "id": 1, "result": "echo: 1"},
        {
            "jsonrpc": "2.0",
            "id": 3,
            "error": {
                "message": "some error",
                "code": -32000,
                "data": {"pay": "load"},
            },
        },
        {"jsonrpc": "2.0", "id": 2, "result": "echo: 2"},
    ]


async def test_batch_notification():
    class H:
        @method()
        async def echo(self, text: str) -> str:
            return 'echo: %s' % text

        @method()
        async def err(self) -> None:
            raise Exception('some error', {'pay': 'load'})

    ex = JsonRpcExecutor(H())
    res = await ex.execute(
        b'[{"jsonrpc": "2.0", "method": "echo", "params": {"text": "1"}},'
        b'{"jsonrpc": "2.0", "method": "err", "params": {}}]'
    )
    assert res == b''


async def test_batch_complicated():
    class H:
        @method()
        async def echo(self, text: str) -> str:
            return 'echo: %s' % text

        @method()
        async def err(self) -> None:
            raise Exception('some error', {'pay': 'load'})

    ex = JsonRpcExecutor(H())
    res = await ex.execute(
        b'[{"jsonrpc": "2.0", '
        b'"method": "echo", "params": {"text": "1"},"id":"1"},'
        b'{"jsonrpc": "2.0", '
        b'"method": "echo", "params": {"text": "2"}},'
        b'{"jsonrpc": "2.0", '
        b'"method": "echo", "params": {"text": "3"},"id":3},'
        b'{"foo": "boo"},'
        b'{"jsonrpc": "2.0", '
        b'"method": "err", "params": {}},'
        b'{"jsonrpc": "2.0", '
        b'"method": "notfound1", "params": {}},'
        b'{"jsonrpc": "2.0", '
        b'"method": "notfound2", "params": {},"id":7},'
        b'{"jsonrpc": "2.0", '
        b'"method": "echo", "params": {"text": "8"},"id":8}]'
    )

    assert json.loads(res) == [
        {"jsonrpc": "2.0", "id": "1", "result": "echo: 1"},
        {"jsonrpc": "2.0", "id": 3, "result": "echo: 3"},
        {
            "jsonrpc": "2.0",
            "id": None,
            "error": {"message": "Invalid Request", "code": -32600},
        },
        {
            "jsonrpc": "2.0",
            "id": 7,
            "error": {"message": "Method not found", "code": -32601},
        },
        {"jsonrpc": "2.0", "id": 8, "result": "echo: 8"},
    ]
