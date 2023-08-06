__version__ = '0'
__build_stamp__ = 0

from .executor import (
    BaseError,
    DeserializeError,
    InvalidRequest,
    MethodNotFound,
    InvalidArguments,
    InternalError,

    method,
    MethodExecutor,
    Result,
)

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

try:
    __import__("iprpc.aioapp")
except ImportError:
    pass

try:
    __import__("iprpc.aiohttp")
except ImportError:
    pass
