import grpc

from logging import Logger
from typing import Callable, Any, get_type_hints

from google.protobuf.message import Message
from grpc import ServicerContext as Context


GRPCService = Callable[[Any, Any, Any], Any]


class ExitGRPCCallWithCode(Exception):
    def __init__(self, ctx: Context, status_code, details: str = ""):
        ctx.set_code(status_code)
        ctx.set_details(details)
        super().__init__()


def catch_exceptions(func: GRPCService, logger: Logger = None) -> GRPCService:
    def wrapper(instance, req: Message, ctx: Context) -> Message:
        try:
            res = func(instance, req, ctx)
            return res

        except ExitGRPCCallWithCode:
            return Message()

        except Exception as e:
            if logger is not None:
                logger.error(e)

            ctx.set_code(grpc.StatusCode.INTERNAL)
            ctx.set_details("Unknown error happened during processing request.")

            return Message()

    return wrapper
