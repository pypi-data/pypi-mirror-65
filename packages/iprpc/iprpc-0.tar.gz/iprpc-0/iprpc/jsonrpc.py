import asyncio
from collections import defaultdict
from typing import Any, Dict, List, Optional, Union

from tinyrpc import exc as rpc_exc
from tinyrpc.protocols import jsonrpc as rpc
from tinyrpc.protocols.jsonrpc import FixedErrorMessageMixin

from .executor import (
    BaseError,
    DeserializeError,
    InternalError,
    InvalidArguments,
    InvalidRequest,
    MethodExecutor,
    MethodNotFound,
)


class JsonRpcError(FixedErrorMessageMixin, Exception):

    jsonrpc_error_code = -32000
    message = 'Server error'

    def __init__(
        self, message: Optional[str] = None, data: Any = None, **kwargs: Any
    ) -> None:
        self.kwargs: dict = defaultdict(lambda: "")
        self.kwargs.update(kwargs)

        if message is not None:
            self.message = message
        if data is not None:
            self.data = data

        self.message = str(self.message).format_map(self.kwargs)

        super().__init__()


class JsonRpcExecutor:
    def __init__(
        self, handler: object, loop: Optional[asyncio.AbstractEventLoop] = None
    ) -> None:
        self.handler = handler
        self.ex = MethodExecutor(
            self.handler, method_key='method', params_key='params'
        )
        self.loop = loop or asyncio.get_event_loop()
        # self.dumps = json.dumps
        self._protocol = rpc.JSONRPCProtocol()

    async def execute(self, request: bytes) -> bytes:
        try:
            req = self._parse_request(request)
        except rpc_exc.RPCError as e:
            return e.error_respond().serialize()

        resp: Optional[Union[rpc.RPCBatchResponse, rpc.RPCResponse]]

        if isinstance(req, rpc.JSONRPCBatchRequest):
            resp = await self._exec_batch(req)
        elif isinstance(req, rpc.JSONRPCRequest):
            resp = await self._exec_single(req)
        else:  # pragma: no cover
            raise NotImplementedError

        if resp is None:
            return b''

        return resp.serialize()

    def _parse_request(
        self, request: bytes
    ) -> Union['rpc.JSONRPCRequest', 'rpc.JSONRPCBatchRequest']:
        return self._protocol.parse_request(request)

    async def _exec_batch(
        self, req: rpc.JSONRPCBatchRequest
    ) -> Optional[rpc.RPCBatchResponse]:
        resp = req.create_batch_response()
        batch = []

        for req_item in req:
            if isinstance(req_item, rpc.InvalidRequestError):
                batch.append(self._exec_err(req_item))
            else:
                batch.append(
                    self._exec(req_item.method, req_item.args, req_item.kwargs)
                )

        results = await asyncio.gather(
            *batch, loop=self.loop, return_exceptions=True
        )

        if resp is None:
            return None

        for i in range(len(req)):
            if isinstance(req[i], rpc.InvalidRequestError):
                resp.append(req[i].error_respond())
            elif req[i].one_way:
                pass
            elif isinstance(results[i], BaseException):
                resp.append(req[i].error_respond(results[i]))
            else:
                resp.append(req[i].respond(results[i]))

        return resp

    async def _exec_single(
        self, req: rpc.JSONRPCRequest
    ) -> Optional[rpc.RPCResponse]:
        try:
            res = await self._exec(req.method, req.args, req.kwargs)
            return req.respond(res)
        except Exception as e:
            return req.error_respond(e)
        finally:
            if req.one_way:
                return None

    async def _exec(self, method: str, args: List, kwargs: Dict) -> Any:
        # TODO by position parameters
        if len(args) > 0:  # pragma: no cover
            raise NotImplementedError(
                'Parameters by position are not supported yet'
            )

        res = await self.ex.call_parsed(method, kwargs)
        if res.error:
            raise self._map_exc(res.error)

        return res.result

    async def _exec_err(self, err: Exception) -> None:
        raise self._map_exc(err)

    @staticmethod
    def _map_exc(ex: Exception) -> Exception:
        if isinstance(ex, BaseError):
            kwargs = {}
            if ex.parent:
                kwargs['data'] = {"info": str(ex.parent)}
            if isinstance(ex, DeserializeError):
                return rpc.JSONRPCParseError(**kwargs)
            elif isinstance(ex, InvalidRequest):
                return rpc.JSONRPCInvalidRequestError(**kwargs)
            elif isinstance(ex, MethodNotFound):
                return rpc.JSONRPCMethodNotFoundError(**kwargs)
            elif isinstance(ex, InvalidArguments):
                return rpc.JSONRPCInvalidParamsError(**kwargs)
            elif ex.parent:
                return ex.parent
            elif isinstance(ex, InternalError):
                return rpc.JSONRPCInternalError(**kwargs)
        return ex
