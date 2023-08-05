from abc import ABC, abstractmethod
import sys


class LambdaFunction(ABC):
    def __init__(self):
        pass

    @classmethod
    def get_handler(cls, *args, **kwargs):
        def handler(event, context):
            return cls(*args, **kwargs).run(event, context)

        return handler

    @abstractmethod
    def run(self, event, context):
        raise NotImplementedError


def lambdahandler(func):
    # Creates dynamic handler in caller's module called MyCallingClassHandler
    module = func.__module__
    handler_name = f"{func.__name__}Handler"
    setattr(sys.modules[module], handler_name, func.get_handler())
    return func
