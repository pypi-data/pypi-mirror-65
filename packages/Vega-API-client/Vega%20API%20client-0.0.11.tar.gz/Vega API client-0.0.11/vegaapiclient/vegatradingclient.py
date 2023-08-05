from .api import API
from .grpc import VegaTradingClient as grpcTradingClient
from .rest import VegaTradingClient as restTradingClient


class VegaTradingClient(object):

    def __init__(
        self,
        api: API,
        url: str
    ):
        if api == API.GRPC:
            self._impl = grpcTradingClient(url)
        elif api == API.REST:
            self._impl = restTradingClient(url)
        else:
            raise Exception("API not implemented")

    def __getattr__(self, funcname):
        return getattr(self._impl, funcname)
