import asyncio
import inspect
import json
import traceback
from collections.abc import Iterable, Mapping
from functools import wraps
from types import MethodType
from typing import Any, Callable, Dict, List, Optional, Type

from jsonschema import FormatChecker as JSONFormatChecker
from jsonschema import validate as json_validate
from jsonschema.exceptions import SchemaError as JSONSchemaError
from jsonschema.exceptions import ValidationError as JSONValidationError
from pydantic import BaseConfig, BaseModel, ValidationError, create_model
from pydantic.json import ENCODERS_BY_TYPE, pydantic_encoder

__all__ = [
    'BaseError',
    'DeserializeError',
    'InvalidRequest',
    'MethodNotFound',
    'InvalidArguments',
    'InternalError',
    'method',
    'MethodExecutor',
    'Result',
]


class _PydanticConfig(BaseConfig):
    arbitrary_types_allowed = True


class BaseError(Exception):
    code = -1
    message = ''

    def __init__(
        self, parent: Optional[Exception] = None, trace: Optional[str] = None
    ) -> None:
        self.parent = parent
        self.trace = trace

    def __str__(self):
        return '%s[%s]: %s%s' % (
            self.__class__.__name__,
            self.code,
            self.message,
            ' (%s)' % self.parent if self.parent else '',
        )


class DeserializeError(BaseError):
    code = -32700
    message = 'Parse error'


class InvalidRequest(BaseError):
    code = -32600
    message = 'Invalid Request'


class MethodNotFound(BaseError):
    code = -32601
    message = 'Method not found'


class InvalidArguments(BaseError):
    code = -32602
    message = 'Invalid params'


class InternalError(BaseError):
    code = -32603
    message = 'Internal Error'


class MethodCaller:
    def __init__(self, func):

        self.func = func
        self._model: Optional[Type[BaseModel]] = None
        self._analyse_arguments(func)

        self._validators: Dict[str, dict] = {}
        if hasattr(func, '__validators__'):
            self._validators = func.__validators__

    def _analyse_arguments(self, func):
        is_method = isinstance(func, MethodType)
        while hasattr(func, '__wrapped__'):
            func = func.__wrapped__
        self.required_params: List[str] = []
        self.optional_params: Dict[str, Any] = {}
        ispec = inspect.getfullargspec(func)
        self.is_kwargs = True if ispec.varkw is not None else False
        args = ispec.args
        self_name = None
        if is_method:
            self_name = args.pop(0)  # rm self
        args_cnt = len(args)
        if ispec.defaults is not None:
            defaults_cnt = len(ispec.defaults)
        else:
            defaults_cnt = 0
        for i in range(args_cnt - defaults_cnt):
            self.required_params.append(args[i])
        for i in range(args_cnt - defaults_cnt, args_cnt):
            di = i - args_cnt + defaults_cnt
            self.optional_params[args[i]] = ispec.defaults[di]
        kwargs = ispec.kwonlyargs
        kwargs_cnt = len(kwargs)
        if ispec.kwonlydefaults is not None:
            kwdefaults_cnt = len(ispec.kwonlydefaults)
        else:
            kwdefaults_cnt = 0
        for i in range(kwargs_cnt - kwdefaults_cnt):
            self.required_params.append(kwargs[i])
        for i in range(kwargs_cnt - kwdefaults_cnt, kwargs_cnt):
            self.optional_params[kwargs[i]] = ispec.kwonlydefaults[kwargs[i]]

        if len(ispec.annotations) > 0:
            opt = self.optional_params

            self._model = create_model(
                'Model',
                __config__=_PydanticConfig,
                **{
                    k: (v, ... if k not in opt else opt[k])
                    for k, v in ispec.annotations.items()
                    if k != 'return' and k != self_name
                },
            )

    def call(self, args: Dict[str, Any], const_args: Dict[str, Any] = None):
        if const_args is None:
            const_args = {}
        _args = self._validate_arguments(args, const_args)
        return self.func(**_args)

    def _validate_arguments(
        self, args: Dict[str, Any], const_args: Dict[str, Any]
    ) -> Dict[str, Any]:
        self._validate_required_arguments(args, const_args)
        _args = dict(**args, **const_args)

        for arg_name, arg_rule in self._validators.items():
            if arg_name in _args:
                val = _args[arg_name]
            else:
                val = self.optional_params[arg_name]

            try:
                json_validate(
                    schema=arg_rule,
                    instance=val,
                    format_checker=JSONFormatChecker(),
                )
            except JSONValidationError as err:
                raise InvalidArguments(
                    Exception('%s: %s' % (arg_name, err.message))
                ) from err
            except JSONSchemaError as err:
                raise UserWarning('Invalid JSON Schema definition: %s' % err)

        if self._model:
            try:
                model = self._model(**_args)
                for key in model.__fields__.keys():
                    _args[key] = getattr(model, key)

            except ValidationError as err:
                es: List[str] = []
                for e in err.errors():
                    loc = '.'.join(str(l) for l in e['loc'])
                    es.append('%s in %s' % (e['msg'], loc))
                raise InvalidArguments(Exception('; '.join(es)))

        return _args

    def _validate_required_arguments(
        self, args: Dict[str, Any], const_args: Dict[str, Any]
    ):
        req = self.required_params.copy()
        for sarg_name in const_args.keys():
            req.remove(sarg_name)
        for arg in args.keys():
            if arg in req:
                req.remove(arg)
            elif arg in self.optional_params:
                pass
            elif self.is_kwargs:
                pass
            else:
                raise InvalidArguments(
                    Exception('Got an unexpected argument: %s' % arg)
                )
        if len(req) > 0:
            raise InvalidArguments(
                Exception(
                    'Missing %s required argument(s):  %s'
                    '' % (len(req), ', '.join(req))
                )
            )


def method(
    name: Optional[str] = None, validators: Optional[Dict[str, dict]] = None
):
    def dec(f):
        if name is not None:
            f.__rpc_name__ = name
        else:
            f.__rpc_name__ = f.__name__

        if validators is not None:
            f.__validators__ = validators
            unknown = set(validators.keys()) - set(f.__code__.co_varnames)
            if unknown:
                raise UserWarning(
                    'Found validator(s) for nonexistent argument(s): %s'
                    '' % ', '.join(unknown)
                )

        @wraps(f)
        def wrapper(*args, **kwrags):
            return f(*args, **kwrags)

        return wrapper

    return dec


class Result:
    def __init__(
        self,
        result: Any,
        error: Optional[BaseError],
        method: Optional[str],
        params: Optional[dict],
    ) -> None:
        self.result = result
        self.error = error
        self.method = method
        self.params = params


class MethodExecutor:
    def __init__(
        self,
        handler: object,
        *,
        method_key: str = 'method',
        params_key: Optional[str] = 'params',
    ):
        self.handler = handler
        self._method_key = method_key
        self._params_key = params_key
        self._callers: Dict[Callable, MethodCaller] = {}
        self._methods: Dict[str, Callable] = {}
        for key in dir(self.handler):
            if callable(getattr(self.handler, key)):
                fn = getattr(self.handler, key)
                if hasattr(fn, '__rpc_name__'):
                    if fn.__rpc_name__ in self._methods:
                        raise UserWarning(
                            'Method %s duplicated' '' % fn.__rpc_name__
                        )
                    self._methods[fn.__rpc_name__] = fn
                    self._callers[fn] = MethodCaller(fn)

    async def call(
        self,
        request: bytes,
        encoding: str = 'UTF-8',
        const_args: Optional[Dict[str, Any]] = None,
    ) -> Result:
        method: Optional[str] = None
        params: Optional[dict] = None
        try:
            try:
                body = json.loads(request, encoding=encoding)
            except (TypeError, ValueError) as err:
                raise DeserializeError(err) from err

            if not isinstance(body, dict):
                raise InvalidRequest()
            if self._method_key not in body:
                raise InvalidRequest()

            method = body.pop(self._method_key)

            if self._params_key is None:
                params = body
            else:
                params = body.get(self._params_key, {})

            if not method:
                raise InvalidRequest()
            if not isinstance(method, str):
                raise InvalidRequest()
            if not isinstance(params, dict):
                raise InvalidRequest()

            return await self.call_parsed(method, params, const_args)
        except BaseError as err:
            err.trace = traceback.format_exc()
            return Result(None, err, method, params)
        except Exception as err:
            return Result(
                None,
                InternalError(err, trace=traceback.format_exc()),
                method,
                params,
            )

    async def call_parsed(
        self,
        method: str,
        params: dict,
        const_args: Optional[Dict[str, Any]] = None,
    ) -> Result:
        try:
            if method not in self._methods:
                raise MethodNotFound()
            fn = self._methods[method]

            if fn not in self._callers:
                self._callers[fn] = MethodCaller(fn)
            ex = self._callers[fn]

            result = ex.call(params, const_args)
            if asyncio.iscoroutine(result):
                result = await result

            return Result(self._serialize_result(result), None, method, params)
        except BaseError as err:
            err.trace = traceback.format_exc()
            return Result(None, err, method, params)
        except Exception as err:
            return Result(
                None,
                InternalError(err, trace=traceback.format_exc()),
                method,
                params,
            )

    @classmethod
    def _serialize_result(cls, result: Any) -> Any:
        if isinstance(result, BaseModel):
            return cls._serialize_result(result.dict())
        if isinstance(result, (int, float, str, bool, type(None))):
            return result
        if isinstance(result, Mapping):
            res_dict = {}
            for key, value in result.items():
                res_dict[key] = cls._serialize_result(value)
            return res_dict
        if isinstance(result, Iterable):
            res_list = []
            for item in result:
                res_list.append(cls._serialize_result(item))
            return res_list

        for enc_type, enc_func in ENCODERS_BY_TYPE.items():
            if isinstance(result, enc_type):
                return enc_func(result)

        return pydantic_encoder(result)
