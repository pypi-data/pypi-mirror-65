from .api import API
from .grpc import VegaTradingDataClient as grpcTradingDataClient
from .rest import VegaTradingDataClient as restTradingDataClient


class VegaTradingDataClient(object):

    def __init__(
        self,
        api: API,
        url: str
    ):
        if api == API.GRPC:
            self._impl = grpcTradingDataClient(url)
        elif api == API.REST:
            self._impl = restTradingDataClient(url)
        else:
            raise Exception("API not implemented")

    def __getattr__(self, funcname):
        return getattr(self._impl, funcname)
